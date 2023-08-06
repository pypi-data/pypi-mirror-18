#!/usr/bin/env python3

from copy import deepcopy
import argparse
import hashlib
import os
import pickle
import re
import logging

from colorama import Fore, Style, init
from pprint import pprint
from pymediainfo import MediaInfo
from tqdm import tqdm
import video_utils

HTML_FILENAME = "tv_report.html"
log = logging.getLogger()

init()


def cprint(colour, message):
    colours = {
            "green": Fore.GREEN,
            "blue": Fore.BLUE,
            "red": Fore.RED,
            "yellow": Fore.YELLOW
            }
    print(colours[colour] + str(message) + Style.RESET_ALL)


def parse_per_season_statistics(filemap):
    statistics = {}
    for show in filemap:
        statistics[show] = {}
        log.info("Working in directory: %s" % show)
        for filename, metadata in filemap[show].items():
            log.info("Parsing per-season statistics for %s" % filename)
            season = video_utils.parseTVEpisode(filename)['season']
            if season not in statistics[show]:
                statistics[show][season] = {"episodes": 0, "size": 0, "quality": {}, "format": {}}
            statistics[show][season]["episodes"] += 1
            statistics[show][season]["size"] += metadata["size"]

            for stat in ["quality", "format"]:
                if not metadata[stat] in statistics[show][season][stat]:
                    statistics[show][season][stat][metadata[stat]] = 0
                statistics[show][season][stat][metadata[stat]] += 1

    return statistics


def parse_per_show_statistics(filemap):
    statistics = {}
    for show in filemap:
        for filename, metadata in filemap[show].items():
            if show not in statistics:
                statistics[show] = {"episodes": 0, "size": 0, "quality": {}, "format": {}}
            statistics[show]["episodes"] += 1
            statistics[show]["size"] += metadata["size"]

            for stat in ["quality", "format"]:
                if not metadata[stat] in statistics[show][stat]:
                    statistics[show][stat][metadata[stat]] = 0
                statistics[show][stat][metadata[stat]] += 1

    return statistics


def parse_global_statistics(show_statistics):
    statistics = {"episodes": 0, "size": 0, "format": {}, "quality": {}}
    for metadata in show_statistics.values():
        statistics["episodes"] += metadata["episodes"]
        statistics["size"] += metadata["size"]
        for stat in ["quality", "format"]:
            for item in metadata[stat]:
                if item not in statistics[stat]:
                    statistics[stat][item] = 0
                statistics[stat][item] += metadata[stat][item]
    return statistics


def get_codec_colour(codec):
    if codec == "x265":
        return "green"
    return "red"


def get_quality_colour(quality):
    if quality == "1080p":
        return "green"
    if quality == "720p":
        return "yellow"
    return "red"


def print_metadata(metadata, indent=0):
    indent = ' ' * indent
    cprint("blue", "%sEpisodes: %s" % (indent, metadata["episodes"]))
    cprint("blue", "%sQuality:" % indent)
    for quality, count in metadata["quality"].items():
        colour = get_quality_colour(quality)
        cprint(colour, "%s  %s: %s (%s)" % (indent, quality, count, '{:.1%}'.format(count / metadata["episodes"])))

    cprint("blue", "%sCodec:" % indent)
    for formatString, count in metadata["format"].items():
        codec = video_utils.getCodecFromFormat(formatString, "pretty")
        colour = get_codec_colour(codec)
        cprint(colour, "%s  %s: %s (%s)" % (indent, codec, count, '{:.1%}'.format(count / metadata["episodes"])))


def print_season_totals(season_statistics):
    print("SEASON TOTALS:")
    for show, show_metadata in season_statistics.items():
        cprint("green", "  %s" % show)
        for season, season_metadata in show_metadata.items():
            print("    Season %s" % season)
            print_metadata(season_metadata, indent=6)
        print()


def print_show_totals(show_statistics):
    print("SHOW TOTALS:")
    for show, metadata in show_statistics.items():
        cprint("green", "  %s" % show)
        print_metadata(metadata, indent=4)
        print()


def print_global_totals(global_statistics):
    print("GLOBAL TOTALS:")
    print_metadata(global_statistics, indent=2)


def save_html(show_statistics, global_statistics, html_filename):
    with open(html_filename, "w") as f:
        f.write('<html><head><title>TV Shows codec report</title><style> \
                 #shows {font-family: "Trebuchet MS", Arial, Helvetica, sans-serif; border-collapse: collapse; width: 100%; } \
                 #shows td {border: 1px solid \
                 #ddd; padding: 8px; text-align: right} \
                 #shows td.left {text-align: left} \
                 #shows td.center {text-align: center} \
                 #shows th {border: 1px solid #ddd; padding: 8px; text-align: center; padding-top: 12px; padding-bottom: 12px; background-color: #4CAF50; color: white; } \
                 #shows tr:nth-child(even){background-color: #f2f2f2;} \
                 #shows tr:hover {background-color: #ddd;}</style> \
                 <script type="text/javascript" src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script></head>')
        f.write('<html><body><table class="sortable" id="shows"><tr><th>Show</th><th>Codec progress</th><th>Quality progress</th><th>Size (GB)</th><th>Episodes</th><th>1080p</th><th>720p</th><th>SD</th><th>Unknown</th><th>x265</th><th>x264</th><th>Other</th></tr>')

        for show, metadata in show_statistics.items():
            f.write(metadata_to_table_row(show, metadata))

        f.write('<tfoot><tr>%s%s%s%s%s%s%s%s%s%s%s%s</tr></tfoot>' % (
            html_cell("TOTALS"),
            html_cell(html_progress(global_statistics["format"]["HEVC"] if "HEVC" in global_statistics["codec"] else 0, global_statistics["episodes"])),
            html_cell(html_progress(global_statistics["quality"]["1080p"] if "1080p" in global_statistics["quality"] else 0, global_statistics["episodes"])),
            html_cell("%3.1f %s" % (global_statistics["size"] / 1024 / 1024 / 1024, "GiB")),
            html_cell(global_statistics["episodes"]),
            html_cell(global_statistics["quality"]["1080p"] if "1080p" in global_statistics["quality"] else 0),
            html_cell(global_statistics["quality"]["720p"] if "720p" in global_statistics["quality"] else 0),
            html_cell(global_statistics["quality"]["SD"] if "SD" in global_statistics["quality"] else 0),
            html_cell(global_statistics["quality"]["Unknown"] if "Unknown" in global_statistics["quality"] else 0),
            html_cell(video_utils.getCodecFromFormat(global_statistics["format"]["HEVC"], codecType="pretty") if "HEVC" in global_statistics["format"] else 0),
            html_cell(video_utils.getCodecFromFormat(global_statistics["format"]["AVC"], codecType="pretty") if "AVC" in global_statistics["format"] else 0),
            html_cell(global_statistics["format"]["Other"] if "Other" in global_statistics["format"] else 0)))
        f.write('</table></body></html>')


def html_cell(data):
    return "<td>%s</td>" % data


def html_progress(value, maximum):
    return '<progress value="%s" max="%s"/>' % (value, maximum)


# TODO: loop through valid formats so this doesn't need to be udpated again
def metadata_to_table_row(show, metadata):
    out = "<tr>"
    out += html_cell(os.path.basename(show))
    out += html_cell(html_progress(metadata["format"]["HEVC"] if "x265" in metadata["format"] else 0, metadata["episodes"]))
    out += html_cell(html_progress(metadata["quality"]["1080p"] if "1080p" in metadata["quality"] else 0, metadata["episodes"]))
    out += html_cell("%3.1f %s" % (metadata["size"] / 1024 / 1024 / 1024, "GiB"))
    out += html_cell(metadata["episodes"])
    out += html_cell(metadata["quality"]["1080p"] if "1080p" in metadata["quality"] else 0)
    out += html_cell(metadata["quality"]["720p"] if "720p" in metadata["quality"] else 0)
    out += html_cell(metadata["quality"]["SD"] if "SD" in metadata["quality"] else 0)
    out += html_cell(metadata["quality"]["Unknown"] if "Unknown" in metadata["quality"] else 0)
    out += html_cell(metadata["format"]["HEVC"] if "x265" in metadata["format"] else 0)
    out += html_cell(metadata["format"]["AVC"] if "x264" in metadata["format"] else 0)
    out += html_cell(metadata["format"]["Other"] if "Other" in metadata["format"] else 0)
    out += "</tr>"
    return out


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose",
                        help="Print more verbose messages",
                        default=0,
                        action="count")
    parser.add_argument("-i", "--ignore-cache",
                        help="Ignore the cache and rebuild it",
                        action="store_true")
    parser.add_argument("-o", "--output-only",
                        help="Just read the cache but don't update it at all",
                        default=False,
                        action="store_true")
    parser.add_argument("--html",
                        help="Save a html version of the report out to the current folder as %s" % HTML_FILENAME,
                        default=False,
                        action="store_true")
    parser.add_argument("directory",
                        help="The directory to read files from",
                        action="store")

    args = parser.parse_args()

    if args.verbose == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)


    directory = os.path.realpath(args.directory)
    data_file_name = hashlib.md5(bytes(directory, 'ascii')).hexdigest()
    data_file_path = os.path.join(os.path.expanduser("~"), ".tv_report_data")
    data_file = os.path.join(data_file_path, data_file_name)

    if not os.path.exists(data_file_path):
        os.mkdir(data_file_path)

    filemap = video_utils.getFileMap(directory, update=not args.output_only, useCache=not args.ignore_cache)

    log.debug("Complete map of files:")
    log.debug(filemap)

    show_statistics = parse_per_show_statistics(filemap)
    season_statistics = parse_per_season_statistics(filemap)
    global_statistics = parse_global_statistics(show_statistics)

    if log.level <= logging.DEBUG:
        cprint("green", "Show statistics:")
        pprint(show_statistics)
        cprint("green", "Season statistics:")
        pprint(season_statistics)
        cprint("green", "Global statistics:")
        pprint(global_statistics)

    print('\n')
    print_season_totals(season_statistics)
    print()
    print_show_totals(show_statistics)
    print()
    print_global_totals(global_statistics)

    if args.html:
        save_html(show_statistics, global_statistics, HTML_FILENAME)


if __name__ == "__main__":
    main()

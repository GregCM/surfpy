#!/usr/bin/python3
import sys
import subprocess
from urllib.parse import urlencode


def print_help():
    global fallback_engine
    m = "".join(
         ["Usage:\n$ surfpy [engine tag] [your search terms]\n",
          "$ surfpy -l (or --list) lists your tags and descriptions and",
          " exits.\n",
          "$ surfpy -h (or --help) prints this help and exits.\n",
          "$ surfpy --print-only will print the string to stdout without"
          " passing it to the browser.\n",
          "$ surfpy -b [browser] uses [browser] instead of the browser"
          " defined in the options.\n",
          "$ surfpy --dmenu launches dmenu for interactive tag selection.\n",
          "\nIf the engine tag is not defined in the options all\n",
          "the arguments will be passed to a fallback search\n",
          "engine defined in the options."])
    print(m)
    print("\nCurrent fallback engine:\n{}\t\t{}"
          .format(fallback_engine, avail_eng[fallback_engine][2]))


def list_engines():
    for i in avail_eng:
        if len(i) > 7:
            print("%s\t%s" % (i, avail_eng[i][2]))
        else:
            print("%s\t\t%s" % (i, avail_eng[i][2]))


# Options:
# --------
# insert the command for your preferred browser here.
browser = "surf"
# set the fallback engine tag you want to use.
fallback_engine = "ddg"
# set additional arguments for dmenu, like font selection or color options.
dmenu_arguments = ""

# Search engines:
# Insert your custom search engines here
# following the syntax of the other ones. Format as follows...
# _________________________________________________________________________
#
# "tag":["engine url with trailing '?' ", " search prefix ", "description"],
# _________________________________________________________________________

# TODO: replace "search prefix" with use-type && corresponding dict
avail_eng = {"ddg": ["https://www.duckduckgo.com/?", "q",
                     "DuckDuckGo"],
             "yt": ["https://www.youtube.com/results?", "search_query",
                    "YouTube"],
             "awiki": ["https://wiki.archlinux.org/index.php?", "search",
                       "Arch Wiki"],
             "apkg": ["https://archlinux.org/packages", "search",
                      "Arch Packages"],
             "aur": ["https://aur.archlinux.org/packages", "search",
                     "AUR"],
             "git": ["https://github.com/login", "login",
                     "GitHub"],
             "gitcm": ["https://github.com/GregCM", "login",
                       "GregHub"]}
# End of options.
# ----------------

print_only = False
input_list = sys.argv[1::]

if "--list" in sys.argv[:2:] or "-l" in sys.argv[:2:]:
    list_engines()
    sys.exit(0)

if "--help" in sys.argv[:2:] or "-h" in sys.argv or len(sys.argv[:2:]) < 2:
    print_help()
    sys.exit(0)

if "-b" in sys.argv:
    browser_index = sys.argv.index("-b")+1
    browser = sys.argv[browser_index]
    input_list.remove("-b")
    input_list.remove(browser)

if "--print-only" in sys.argv:
    input_list.remove("--print-only")
    print_only = True

# "the way of the future"(TM)
if ("--dmenu" in sys.argv) and (len(sys.argv[:2:]) < 3):
    input_list.remove("--dmenu")
    dmenu_tags = ''
    for tag in avail_eng:
        dmenu_tags += tag + '\n'
    dmenu_command = ("echo \"{}\" | dmenu -p 'Go:' {}"
                     .format(dmenu_tags, dmenu_arguments))

    try:
        input_list = subprocess.check_output(
            dmenu_command,
            stderr=subprocess.STDOUT,
            shell=True).strip().split()

    except subprocess.CalledProcessError:
        sys.exit(0)

if "--dmenu" in sys.argv:
    input_list.remove("--dmenu")
    dmenu_tags = ''
    for tag in avail_eng:
        dmenu_tags += tag + '\n'
    dmenu_command = ("echo \"{}\" | dmenu -p 'Go:' {}"
                     .format(dmenu_tags, dmenu_arguments))

    try:
        input_list = subprocess.check_output(
            dmenu_command,
            stderr=subprocess.STDOUT,
            shell=True).strip().split()

    except subprocess.CalledProcessError:
        sys.exit(0)

if input_list[0] in avail_eng:
    search_engine = input_list[0]
    search_string = " ".join(input_list[1::])

else:
    search_engine = fallback_engine
    search_string = " ".join(str(input_list))

engine_url = avail_eng[search_engine][0]
search_prefix = avail_eng[search_engine][1]
query_url = engine_url + urlencode({search_prefix: search_string})

if print_only:
    print(query_url)
else:
    subprocess.Popen([browser, query_url])

sys.exit(0)

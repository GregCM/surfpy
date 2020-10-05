# Surfpy #
Surfpy is a simple python script to quickly search things on the web from
the command line.<br/>
It is similar to surfraw, but with much less features.

Configuration is done in the script itself and adding new tags is very easy.<br/>

## "the way of the future"(TM) ##

Main Use Case is for suckless/surf call to custom-built dmenu, as follows:

    /* SETPROP(readprop, setprop, prompt)*/
    #define SETPROP(r, s, p) { \
            .v = (const char *[]){ "/bin/sh", "-c", \
                 "prop=\"$(printf '%b' \"$(xprop -id $1 $2 " \
                 "| sed \"s/^$2(STRING) = //;s/^\\\"\\(.*\\)\\\"$/\\1/\")\" " \
      >>>>>      "| ./surfpy.py --dmenu)\" && xprop -id $1 -f $3 8s -set... (etc.)
                 "surf-setprop", winid, r, s, p, NULL \
            } \
    }

## TODO ##
- subprocess watcher for browser instances
    - bait and switch (replace current browser windows with new ones consisting of the script output)
- combined searchbar & addressbar behavior
- incorporation into surf
    - dwm colorscheme consistency

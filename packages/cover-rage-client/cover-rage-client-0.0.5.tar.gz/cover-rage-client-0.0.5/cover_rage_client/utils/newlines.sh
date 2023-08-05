#!/bin/bash
git diff -U0 HEAD~1 HEAD | $1 show_path=1 show_hunk=0 show_header=0 | egrep "[^\0]+\.(py)\:[0-9]+\:\+" | cut -d ':' -f1,2

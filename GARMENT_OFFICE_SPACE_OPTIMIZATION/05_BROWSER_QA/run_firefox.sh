#!/bin/sh
# Firefox run of test_simple_viewer.js: Firefox release build + puppeteer-core (WebDriver BiDi) in a virtual X display,
# Mesa llvmpipe as the software WebGL 2 renderer.  FIREFOX_BIN=<firefox binary> PPTR_MODULES=<dir with puppeteer-core> sh run_firefox.sh URL OUT_DIR
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
XV=$!
sleep 2
DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 NODE_PATH="$PPTR_MODULES" node "$(dirname "$0")/test_simple_viewer.js" "$1" "$2" firefox
RC=$?
kill $XV
exit $RC

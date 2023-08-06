====================
Automatedscreenshots 
====================

set values for: 
===============
    export SCREENSHOT_USER=''
    export SCREENSHOT_PASSWORD=''
    export SCREENSHOT_SERVER_URL=''

Capture a screen shot and get the URL:
======================================
    from automatedscreenshots import Builder
    b = Builder('http://www.google.com/')
    b.capture()
    print(b.image_url)

Get info about a screen shot:
=============================
    from automatedscreenshots import Builder
    b = Builder('http://www.google.com/')
    print(b.info())

Search for a URL:
=================
    from automatedscreenshots import Builder
    b = Builder('http://www.google.com/')
    print(b.search())

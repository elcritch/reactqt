#!/usr/bin/env python3

import sys, os, collections
from pathlib import Path

import webbrowser

htmlName = "trees.html"
baseHtml = Path(__file__).parent / "www" / htmlName
baseHtmlUrl = "file://"+baseHtml.as_posix()

# chrome = webbrowser.get("chrome")
webbrowser.open_new(baseHtmlUrl)


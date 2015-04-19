#!/usr/bin/env python3

import sys, os, collections
from pathlib import Path

from PySide.QtCore import QObject, Slot, Signal
from PySide.QtGui import QApplication
from PySide.QtWebKit import QWebView, QWebSettings
from PySide.QtNetwork import QNetworkRequest

class BasicHub(QObject):
 
    def __init__(self):
        super().__init__()
 
    @Slot(str)
    def display(self, config):
        print(config)
        self.on_client_event.emit("Howdy!")
 
    @Slot(str)
    def disconnect(self, config):
        print(config)
 
    on_client_event = Signal(str)
    on_actor_event = Signal(str)
    on_connect = Signal(str)
    on_disconnect = Signal(str)


class BasicApplication(QWebView):
    
    def __init__(self):
        super().__init__()
        
        self.baseHtml = Path(__file__).parent / "www" / "basic.html"
        self.hub = BasicHub()
        
    def init(self):
        self.loadFinished.connect(self.onLoad)
        self.load(self.baseHtml.as_posix())
        self.show()
    
    def onLoad(self):
                
        # This is the body of a web browser tab
        self.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        
        # This is the actual context/frame a webpage is running in.
        # Other frames could include iframes or such.
        self.myFrame = self.page().mainFrame()
        
        # ATTENTION here's the magic that sets a bridge between Python to HTML
        self.myFrame.addToJavaScriptWindowObject("hub", self.hub)
        
        # Tell the HTML side, we are open for business
        self.myFrame.evaluateJavaScript("ApplicationIsReady()")



def main():
    
    #Kickoff the QT environment
    app = QApplication(sys.argv)

    reactApp = BasicApplication()
    reactApp.init()

    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()


#!/usr/bin/env python3

import sys, os, collections
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import QNetworkRequest

Signal = pyqtSignal
Slot = pyqtSlot


class ExampleScript(object):

    def __call__(self, input):
        return {"result": 1.2, "input": input}

class DataContainer(QObject):

    def __init__(self, data):
        self.data = data


class ReactHub(QObject):
    
    def __init__(self):
        super().__init__()
        self.exampleExecutor = ExampleScript()
 
    @Slot(str)
    def run(self, input, data):
        print("Executing input", signalName, input)
        
        if hasattr(self, signalName):
            signal = getattr(self, signalName)
            signal.emit(DataContainer(data))
    
    on_client_event = Signal(str)
    signal_test = Signal(DataContainer)


class ReactApplication(QWebView):
    
    def __init__(self, htmlName="empty.html"):
        super(ReactApplication, self).__init__()
        
        self.baseHtml = Path(__file__).parent / "www" / htmlName
        print("Base Html:",self.baseHtml)
        self.hub = ReactHub()
        
    def init(self):
        self.loadFinished.connect(self.onLoad)
        self.load(QUrl("file://"+self.baseHtml.as_posix()))
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
        # self.myFrame.evaluateJavaScript("ApplicationIsReady()")

        self.myFrame.evaluateJavaScript("""
        """)


def main():
    
    #Kickoff the QT environment
    app = QApplication(sys.argv)

    # reactApp = ReactApplication("empty.html")
    # reactApp = ReactApplication("timer.html")
    reactApp = ReactApplication("trees.html")
    reactApp.init()

    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()


import subprocess
import time
import os.path
import sys

class BrowserActivator:
    def __init__(self, contentPath):
        self.contentPath = contentPath
        self.firefoxPid = self.executeCommand('xdotool search --name "Mozilla Firefox"').strip()

    def executeCommand(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        return stdout

    def getFileName(self, fileExtension):
        filename = self.executeCommand('xdotool getwindowname ' + str(self.firefoxPid)).strip()
        filename = filename.split('-')[0].strip() + fileExtension
        print(filename)
        return filename

    def isSaveStarted(self):
        dirname = self.getFileName('_files')
        return os.path.isdir(dirname)

    def isSaveCompleted(self):
        filename = self.getFileName('.html')
        return os.path.isfile(self.contentPath + filename)

    def getTitleUpdaterJSCode(self):
        return '''t = setInterval(function() {document.title = document.getElementsByClassName('_item--item-selected--3LMMf')[0].children[0].title;}, 100);'''

    def init(self):
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)
        print('xdotool windowactivate --sync ' + str(self.firefoxPid) + ' type "' + self.getTitleUpdaterJSCode() + '"')
        self.executeCommand('xdotool windowactivate --sync ' + str(self.firefoxPid) + ' type "' + self.getTitleUpdaterJSCode() + '"')
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "Return"')
        time.sleep(3)
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)

    def perform(self):
        print(self.firefoxPid)
        self.init()
        inProgress = False
        while(True):
            if inProgress:
                print("Saving in progress")
                if self.isSaveCompleted():
                    print("File saved")
                    inProgress = False
                else:
                    time.sleep(1)
            else:
                print("Beginning Save")
                time.sleep(5)
                self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "ctrl+s"')
                time.sleep(1)
                self.executeCommand('save_as=$(xdotool search --name "Save As") && xdotool windowactivate $save_as key --clearmodifiers "Return"')
                time.sleep(2)
                inProgress = True

if __name__ == '__main__':
    key = raw_input("Press Enter Key to begin")
    browserActivator = BrowserActivator('../Content/')
    browserActivator.perform()

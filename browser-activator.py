import subprocess
import time
import os.path
import sys

class BrowserActivator:
    def __init__(self, contentPath):
        self.contentPath = contentPath
        self.firefoxPid = self.executeCommand('xdotool search --name "Mozilla Firefox"').strip()

    def executeCommand(self, cmd):
        print("Executing: ", cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        stdout, stderr = p.communicate()
        return stdout

    def getFileName(self, fileExtension):
        filename = self.executeCommand('xdotool getwindowname ' + str(self.firefoxPid)).strip()
        filename = '-'.join(filename.split('-')[:-1]).strip() + fileExtension
        filename = filename.replace('/', '_')
        print(filename)
        return filename

    def isSaveStarted(self):
        dirname = self.getFileName('_files')
        return os.path.isdir(dirname)

    def isSaveCompleted(self):
        filename = self.getFileName('.html')
        print("Checking if exists: ", (self.contentPath + filename))
        return os.path.isfile(self.contentPath + filename)

    def getTitleUpdaterJSCode(self):
        return '''t = setInterval(function() {document.title = document.getElementsByClassName('_item--item-selected--3LMMf')[0].children[0].title;}, 100);'''

    def getTriggerNextPageJSCode(self):
        return '''jQuery(window).keypress(function (e) { var keyCode = e.which; console.log(e, keyCode, e.which); if (keyCode == 110) { console.log('You pressed N!'); document.getElementsByClassName('_main--footer-container--3vC-_')[0].children[0].click(); }}); '''

    def getJSCode(self):
        return self.getTitleUpdaterJSCode() + ";" + self.getTriggerNextPageJSCode()

    def init(self):
        if raw_input("Initialize JS Scripts? (y/n): ") == 'n':
            return
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)
        print('xdotool windowactivate --sync ' + str(self.firefoxPid) + ' type "' + self.getJSCode() + '"')
        self.executeCommand('xdotool windowactivate --sync ' + str(self.firefoxPid) + ' type "' + self.getJSCode() + '"')
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "Return"')
        time.sleep(5)
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)

    def triggerNextPage(self):
        self.executeCommand('xdotool windowactivate ' + str(self.firefoxPid) + ' key --clearmodifiers "n"')

    def perform(self):
        print(self.firefoxPid)
        self.init()
        inProgress = False
        while(True):
            if inProgress:
                print("Saving in progress")
                if self.isSaveCompleted():
                    print("File saved")
                    self.triggerNextPage()
                    time.sleep(3)
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
    contentPath = sys.argv[1] + '/' # ../Content
    browserActivator = BrowserActivator(contentPath)
    browserActivator.perform()

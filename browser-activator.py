import subprocess
import time
import os.path
import argparse

class BrowserActivator:
    def __init__(self, contentPath, browser):
        self.contentPath = contentPath
        self.browserPid = self.executeCommand('xdotool search --name "' + browser + '"').strip()

    def executeCommand(self, cmd):
        print("Executing: ", cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        stdout, stderr = p.communicate()
        return stdout

    def getFileName(self, fileExtension):
        filename = self.executeCommand('xdotool getwindowname ' + str(self.browserPid)).strip()
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

    def getTitleUpdaterJSCode(self, querySelectorForSelectedItem):
        return "t = setInterval(function() {document.title = document.getElementsByClassName('" + querySelectorForSelectedItem + "')[0].children[0].title;}, 100);"

    def getTriggerNextPageJSCode(self, querySelectorForNextButton):
        return "jQuery(window).keypress(function (e) { var keyCode = e.which; console.log(e, keyCode, e.which); if (keyCode == 110) { console.log('You pressed N!'); document.getElementsByClassName('" + querySelectorForNextButton + "')[0].children[0].click(); }});"

    def getJSCode(self, querySelectorForSelectedItem, querySelectorForNextButton):
        return self.getTitleUpdaterJSCode(querySelectorForSelectedItem) + ";" + self.getTriggerNextPageJSCode(querySelectorForNextButton)

    def init(self, querySelectorForSelectedItem, querySelectorForNextButton):
        if raw_input("Initialize JS Scripts? (y/n): ") == 'n':
            return
        self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)
        print('xdotool windowactivate --sync ' + str(self.browserPid) + ' type "' + self.getJSCode(querySelectorForSelectedItem, querySelectorForNextButton) + '"')
        self.executeCommand('xdotool windowactivate --sync ' + str(self.browserPid) + ' type "' + self.getJSCode(querySelectorForSelectedItem, querySelectorForNextButton) + '"')
        self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "Return"')
        time.sleep(5)
        self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "ctrl+shift+i"')
        time.sleep(3)

    def triggerNextPage(self):
        self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "n"')

    def perform(self, querySelectorForSelectedItem, querySelectorForNextButton):
        print(self.browserPid)
        self.init(querySelectorForSelectedItem, querySelectorForNextButton)
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
                self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "ctrl+s"')
                time.sleep(1)
                self.executeCommand('save_as=$(xdotool search --name "Save As") && xdotool windowactivate $save_as key --clearmodifiers "Return"')
                time.sleep(2)
                inProgress = True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatically Navigate through and Save Complete Web pages')
    parser.add_argument('-p', action='store', dest='contentPath', help='Directory where web pages will be saved. If not specified, then all web pages are expected to be saved in a directory named "Content" present in the current working directory', default='./Content')
    parser.add_argument('-b', action='store', dest='browser', help='Browser which will be automatically controlled. Uses Mozilla Firefox by default', default='Mozilla Firefox')
    parser.add_argument('-t', action='store', dest='querySelectorForSelectedItem', help='Query selector corresponding to the selected item in the DOM of the web page, which will be used as the name of the saved web page', default='_item--item-selected--3LMMf')
    parser.add_argument('-n', action='store', dest='querySelectorForNextButton', help='Query selector corresponding to the next button in the DOM of the web page, which will be used to automatically navigate to the next page after the current page has been saved', default='_main--footer-container--3vC-_')
    args = parser.parse_args()

    contentPath = args.contentPath + '/' 
    browserActivator = BrowserActivator(contentPath, args.browser)
    browserActivator.perform(args.querySelectorForSelectedItem, args.querySelectorForNextButton)

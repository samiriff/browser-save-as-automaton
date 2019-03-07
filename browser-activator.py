import subprocess
import time
import os.path
import argparse

class BrowserActivator:
    '''
    Manages the entire task of detecting an open browser window, injecting the appropriate JS scripts to control and 
    navigate through a given web-page in order to automatically save it to a local directory
    '''

    def __init__(self, contentPath, browser):
        '''
        Constructor that initializes the path to the directory where the web pages are being saved
        and the browser which is being controlled.
        :param contentPath: string containing the path to the directory where the web pages are being saved
        :param browser: string containing the name of the browser that is being controlled
        '''
        self.contentPath = contentPath
        self.browserPid = self.executeCommand('xdotool search --name "' + browser + '"').strip()

    def executeCommand(self, cmd):
        '''
        Utility method to execute a command in shell and pipe the output to a string
        :param cmd: string containing the command to be executed
        :returns: output of executed command
        '''
        print("Executing: ", cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.wait()
        stdout, stderr = p.communicate()
        return stdout

    def getFileName(self, fileExtension):
        '''
        Gets the file name to be used while saving a webpage with the appropriate extension with the browser name and whitespaces stripped
        :param fileExtension: string containing the extension of the file (Eg., html)
        :returns: string containing file name
        '''
        filename = self.executeCommand('xdotool getwindowname ' + str(self.browserPid)).strip()
        filename = '-'.join(filename.split('-')[:-1]).strip() + fileExtension
        filename = filename.replace('/', '_')
        print(filename)
        return filename

    def isSaveCompleted(self):
        '''
        Checks if a web page has been saved completely, based on the fact that the corresponding html file is found in the contentPath directory 
        :returns: boolean indicating whether the web page has been saved
        '''
        filename = self.getFileName('.html')
        print("Checking if exists: ", (self.contentPath + filename))
        return os.path.isfile(self.contentPath + filename)

    def getTitleUpdaterJSCode(self, querySelectorForSelectedItem):
        '''
        Gets Javascript code that is capable of updating the title tag of the webpage with the name of a selected item, such that the browser window name is updated
        and will be used to save each web page under a unique name
        TODO: Make this method more extensible to cover other use-cases and selectors
        :param querySelectorForSelectedItem: string containing the CSS class name that can be used to identify the selected item
        :returns: string containg Javascript code
        '''
        return "t = setInterval(function() {document.title = document.getElementsByClassName('" + querySelectorForSelectedItem + "')[0].children[0].title;}, 100);"

    def getTriggerNextPageJSCode(self, querySelectorForNextButton):
        '''
        Gets Javascript code that is capable of triggering a click of the "Next" button on the webpage, to navigate to a subsequent page in the series after a web page has
        been saved
        TODO: Make this method more extensible to cover other use-cases and selectors
        :param querySelectorForNextButton: string containing the CSS class name that can be used to identify the next button
        :returns: string containg Javascript code
        '''
        return "jQuery(window).keypress(function (e) { var keyCode = e.which; console.log(e, keyCode, e.which); if (keyCode == 110) { console.log('You pressed N!'); document.getElementsByClassName('" + querySelectorForNextButton + "')[0].children[0].click(); }});"

    def getJSCode(self, querySelectorForSelectedItem, querySelectorForNextButton):
        '''
        Concatenates all the JS scripts together into one script so that they can be injected into the web page during initialization
        :param querySelectorForSelectedItem: string containing the CSS class name that can be used to identify the selected item
        :param querySelectorForNextButton: string containing the CSS class name that can be used to identify the next button
        :returns: string containing concatenated JS code
        '''
        return self.getTitleUpdaterJSCode(querySelectorForSelectedItem) + ";" + self.getTriggerNextPageJSCode(querySelectorForNextButton)

    def init(self, querySelectorForSelectedItem, querySelectorForNextButton):
        '''
        Performs some initialization tasks before starting the save-web-page loop. Initialization can be skipped, if required, based on a user-prompt.
        As part of initialization, the inspector tools of the browser is opened, the required JS code is copied over and the inspector tools is closed
        :param querySelectorForSelectedItem: string containing the CSS class name that can be used to identify the selected item
        :param querySelectorForNextButton: string containing the CSS class name that can be used to identify the next button
        '''
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
        '''
        Automatically triggers a key press of the 'n' key which will navigate the browser from the current web page to the next page that has to be saved
        '''
        self.executeCommand('xdotool windowactivate ' + str(self.browserPid) + ' key --clearmodifiers "n"')

    def perform(self, querySelectorForSelectedItem, querySelectorForNextButton):
        '''
        Initializes the first web page with the appropriate JS scripts and starts the cycle of saving each web page and navigating to the next web page once
        a web page has been saved completely.
        TODO: This is currently an infinite loop and requires human intervention to terminate. Need to figure out a way to automatically terminate when there 
        are no more pages left to save
        '''
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

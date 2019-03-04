import subprocess
import time
import os.path
import sys

def executeCommand(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout

def getFileName(firefoxPid, fileExtension):
    filename = executeCommand('xdotool getwindowname ' + str(firefoxPid)).strip()
    filename = filename.split('-')[0].strip() + fileExtension
    print(filename)
    return filename

def isSaveStarted(firefoxPid):
    dirname = getFileName(firefoxPid, '_files')
    return os.path.isdir(dirname)

def isSaveCompleted(firefoxPid):
    filename = getFileName(firefoxPid, '.html')
    return os.path.isfile(filename)

def getTitleUpdaterJSCode():
    return '''t = setInterval(function() {document.title = document.getElementsByClassName('_item--item-selected--3LMMf')[0].children[0].title;}, 100);'''

def init(firefoxPid):
    executeCommand('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
    time.sleep(3)
    print('xdotool windowactivate --sync ' + str(firefoxPid) + ' type "' + getTitleUpdaterJSCode() + '"')
    executeCommand('xdotool windowactivate --sync ' + str(firefoxPid) + ' type "' + getTitleUpdaterJSCode() + '"')
    executeCommand('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "Return"')
    time.sleep(3)
    executeCommand('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"')
    time.sleep(3)

def perform():    
    firefoxPid = executeCommand('xdotool search --name "Mozilla Firefox"').strip()
    print(firefoxPid)
    init(firefoxPid)
    inProgress = False
    while(True):
        if inProgress:            
            print("Saving in progress")
            if isSaveCompleted(firefoxPid):
	        print("File saved")
	        inProgress = False
            else:
                time.sleep(1)
        else:
            print("Beginning Save")
            time.sleep(5)
            executeCommand('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "ctrl+s"')
            time.sleep(1)
	    executeCommand('save_as=$(xdotool search --name "Save As") && xdotool windowactivate $save_as key --clearmodifiers "Return"')
	    time.sleep(2)
            inProgress = True

if __name__ == '__main__':
    key = raw_input("Press Enter Key to begin")
    perform()

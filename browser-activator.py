import subprocess
import time
import os.path

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
    return '''
    t = setInterval(function() {
      document.title = document.getElementsByClassName('_item--item-selected--3LMMf')[0].children[0].title;
    }, 100);
    '''

def init(firefoxPid):
    subprocess.call('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "ctrl+shift+i"', shell=True)
    time.sleep(3)
    subprocess.call('xdotool windowactivate --sync ' + str(firefoxPid) + ' type "' + getTitleUpdaterJSCode() + '"', shell=True)
    subprocess.call('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "Return"', shell=True)
    abc

def perform():    
    firefoxPid = executeCommand('xdotool search --name "Mozilla Firefox"').strip()
    print(firefoxPid)
    init(firefoxPid)
    inProgress = False
    while(True):
        if inProgress:
            if isSaveCompleted(firefoxPid):
	        print("File saved")
	        inProgress = False
            else:
                time.sleep(1)
        else:
            subprocess.call('xdotool windowactivate ' + str(firefoxPid) + ' key --clearmodifiers "ctrl+s"', shell=True)
            time.sleep(1)
	    subprocess.call('save_as=$(xdotool search --name "Save As") && xdotool windowactivate $save_as key --clearmodifiers "Return"', shell=True)
	    time.sleep(2)
            inProgress = True

if __name__ == '__main__':
    key = raw_input("Enter value")
    print("Input string = ", key)
    if key == 'n':
        perform()

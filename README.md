# Browser Save As Automaton

A simple utility to automatically navigate through a collection of pages of a dynamic website and save each web page completely (with CSS, JS, image files, etc.) on your local drive for offline use. 

This would be useful to download all content from a dynamic website when you are reaching the end of its subscription period. Note that the pages you are saving should have a "Next" button so that navigation to a subsequent page can be automated.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

 - Python 2.7 or above
 - Any Linux distribution in which the `xdotool` utility can be installed
 - xdotool
 - Any web browser to navigate website (Eg., Chrome, Firefox) with access to its developer tools

### Usage

 1. Login to the website you wish to save in your web browser of choice - BROWSER
 
 2. Navigate to the first page of the collection of pages you wish to save. Ensure that this page contains a "Next" button for navigation
 
 3.  Use inspector tools to find a suitable Query selector corresponding to the selected item in the DOM of the web page, which will be used as the name of the saved web page - QUERYSELECTORFORSELECTEDITEM

 4.  Use inspector tools to find a suitable Query selector corresponding to the next button in the DOM of the web page, which will be used to automatically navigate to the next page after the current page has been saved - QUERYSELECTORFORNEXTBUTTON
 
 5. If this page contains a youtube video that automatically plays, this might interfere with the JS code that automatically triggers the next button. Ensure that you click on some primitive page element other than the video before running the python code. 

  6. Ensure that the browser is currently saving files to the directory of your choice, i.e., CONTENTPATH
 
 6. Run the following command with the parameters you got above:
	```
	python browser-activator.py -p CONTENTPATH -b BROWSER -t QUERYSELECTORFORSELECTEDITEM -n QUERYSELECTORFORNEXTBUTTON
	```
7. To get more information on the usage, run the following command:
	```
	python browser-activator.py -h
	```
	```
	usage: browser-activator.py [-h] [-p CONTENTPATH] [-b BROWSER]
	                            [-t QUERYSELECTORFORSELECTEDITEM]
	                            [-n QUERYSELECTORFORNEXTBUTTON]

	Automatically Navigate through and Save Complete Web pages

	optional arguments:
	  -h, --help            show this help message and exit
	  -p CONTENTPATH        Directory where web pages will be saved. If not
	                        specified, then all web pages are expected to be saved
	                        in a directory named "Content" present in the current
	                        working directory
	  -b BROWSER            Browser which will be automatically controlled. Uses
	                        Mozilla Firefox by default
	  -t QUERYSELECTORFORSELECTEDITEM
	                        Query selector corresponding to the selected item in
	                        the DOM of the web page, which will be used as the
	                        name of the saved web page
	  -n QUERYSELECTORFORNEXTBUTTON
	                        Query selector corresponding to the next button in the
	                        DOM of the web page, which will be used to
	                        automatically navigate to the next page after the
	                        current page has been saved
	```

### Development

Clone the repository and modify `browser-activator.py` to suit your use-case.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Samir Sheriff** - *Initial work* - [samiriff](https://github.com/samiriff)

See also the list of [contributors](https://github.com/samiriff/browser-save-as-automaton/graphs/contributors) who participated in this project.

## License

This project is licensed under the Unlicense License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Inspired by https://github.com/abiyani/automate-save-page-as 

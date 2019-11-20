# hackernews.py

Please find below steps on how to get you up and running, with an overview of libraries used and why they were employed within the solution.  This project focuses on taking 'n' amount of articles (where 'n' is determined by user input) from [Hacker News](https://news.ycombinator.com/news) and parsing this data into a valid JSON string. Enjoy!

## Installation

1. Start by installing [Python3](https://www.python.org/) onto your local machine 
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 'beautifulsoup4' and 'requests' as shown below (don't worry if an error message is shown when installing requests, most times requests is installed alongside Python.)

```bash
pip install beautifulsoup4
pip install requests
```
3. Navigate to the project folder where the 'hackernews.py' script is located by launching your CLI and using the command 'cd' followed by the dir path to the folder containing your script. (examples are shown below - though these may vary)
```bash
Windows CMD:
C:\Users\admin>cd C:\Users\admin\Desktop\hackerNews

Linux/OSX
admin@ubuntu: ~$cd /Users/admin/Desktop/hackerNews
```
4. Run the script with Python by calling python followed by the script name 'hackernews.py' and the argument you wish to pass. (Examples shows argument -h / --help which displays arguments the script accepts)
```bash
Windows CMD:
C:\Users\admin\Desktop\hackerNews>python hackernews.py -h 

Linux/OSX
admin@ubuntu: ~/hackerNews$python hackernews.py --help
```
If the command '>Python hackernews.py -arg' (where arg is your desired argument) does not work, this might suggest you have multiple instances of Python installed on your device. Try the same command using 'Python3' instead and if issues persist, try [clicking me](https://stackoverflow.com/questions/13596505/python-not-working-in-command-prompt) for more insight (Remember, your Python folders should not start with 2 - but 3 ). 

If any further help is needed: 
- [Click me](https://docs.python.org/3/using/windows.html) for Python's official documentation on running within a Windows environment. 

- [Click me](https://docs.python-guide.org/starting/install3/linux/) for Python documentation on running within a Linux environment. 

- [Click me](https://docs.python.org/2/using/mac.html) for Python documentation on running within a OSX environment.


## Libraries Used
- Requests: An HTTP library for Python which allows us to send HTTP/1.1 requests without the need to manually add query strings to URLs, or to form-encode POST data. Used to retrieve website data from [https://news.ycombinator.com/news](https://news.ycombinator.com/news).
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Functioning as an HTML parser made easy to use due to its Pythonic idioms for iterating, searching, and modifying the parse tree of webpages - saving time during development.
- Argparse: Python's CLI argument parsing module allows the creation of arguments and argument exceptions.
- Sys: Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. Used to obtain argument value given by the user when the script is run.

- constant.py: File containing constants used for the project. Only contains single constant POSTS_ON_PAGE set to 30 - which is the number of posts on a HackerNews news page




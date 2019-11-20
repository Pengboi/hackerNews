# hackernews.py

Please find below steps on how to get you up and running, with an overview of libraries used and why they were employed within the solution. Enjoy!

## Installation

1. Start by installing [Python3](https://www.python.org/) onto your local machine 
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 'beautifulsoup4' and 'requests' as shown below

```bash
pip install beautifulsoup4
pip install requests
```
3. Navigate to the project folder where the script is located using your CLI (examples are shown below - though these may vary)
```bash
Windows CMD:
C:\Users\admin>cd C:\Users\admin\Desktop\hackerNews

Linux/OSX
admin@ubuntu: ~$cd /Users/admin/Desktop/hackerNews
```
4. Run the script with Python as shown below (examples shows argument -h / --help which displays arguments the script accepts)
```bash
Windows CMD:
C:\Users\admin\Desktop\hackerNews>python hackernews.py -h 

Linux/OSX
admin@ubuntu: ~/hackerNews$python hackernews.py --help
```




## Libraries Used
- Requests: An HTTP library for Python which allows us to send HTTP/1.1 requests without the need to manually add query strings to URLs, or to form-encode POST data. Used to retrieve website data from [https://news.ycombinator.com/news](https://news.ycombinator.com/news).
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Functioning as an HTML parser made easy to use due to its Pythonic idioms for iterating, searching, and modifying the parse tree of webpages - saving time during development.
- Argparse: Python's CLI argument parsing module allows the creation of arguments and argument exceptions.
- Sys: Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. Used to obtain argument value given by the user when the script is run.

- constant.py: File containing constants used for the project. Only contains single constant POSTS_ON_PAGE set to 30 - which is the number of posts on a HackerNews news page



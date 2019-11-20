#!/usr/bin/python3
"""
Below find a list of imported libraries employed in the development of the solution. A summative description of each
should be found below:
    requests      : HTTP library for Python which allows us to send HTTP/1.1 requests without the need to manually add
                    query strings to URLs, or to form-encode POST data
    BeautifulSoup : Access to library enabling us to simplify content obtained from a website, making it parsable to
                    ease the extract of information
    Argparse & Sys: Python's CLI argument parsing module in addition to sys allow the program to take CLI arguments
                    which are validated and used to determine behaviour of script.
    JSON          : Python's JSON module allows Python to encode objects as JSON scripts and decode JSON strings as
                    Python objects - used to create JSON string for STDOUT
    constant.py   : Script containing defined CONSTANTS for solution.
"""
import requests
from bs4 import BeautifulSoup
import argparse
import sys
import json
import constant


def check_arg(n):
    """
    Validates -p argument to determine if input is acceptable - throws Argument Type Error if validation is failed.
    :param  n:  contains -p/--posts user inputted argument value, which is validated below.
                if value is not a positive integer <= 100, user is displayed with argument type error in STDOUT
    :return n:  Once 'n' is validated, value is returned
    """
    try:
        n = int(n)
        if int(n) < 0:
            raise argparse.ArgumentTypeError("%s is an invalid integer." % n)
        if int(n) > 100:
            raise argparse.ArgumentTypeError("%s is too high. Max value = 100" % n)
        return int(n)
    except ValueError:
        raise argparse.ArgumentTypeError("%s not a valid number." % n)


def main():
    """
    Business Logic Module which is called when script is ran. Defines arguments, obtains and processes web data with
    help from other functions.
    :return: func - output_json : translates obtained data into JSON string.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--posts", type=check_arg, default="30",   # -P argument created. Calls check_arg with val
                        help="How many posts would you like to fetch?")  # as argument.
    arg = parser.parse_args()
    post_arg = int(sys.argv[2])                    # Contains -p/--post argument inputted by user when determined valid

    pages_needed = post_arg // constant.POSTS_ON_PAGE
    # If there is a remainder, another page will be needed to fulfil usr's request
    # i.e. -p 35 = 3 pages_needed with code above; Code below sees if 35MOD30 != 0, ensures sufficient pages_needed
    if post_arg % constant.POSTS_ON_PAGE != 0:
        pages_needed += 1

    headlines, links, scores, users, comments, ranking = [], [], [], [], [], []     # Lists to hold page data
    """
    For each page needed to fulfil request, page content is obtained and simplified with use of requests and BS libs.
    fetch_title_data called to obtain headlines, links and ranking of all posts on current page.
    fetch_subtext_data called to obtain scores, users and comment numbers of all posts on current page
    """
    for i in range(1, pages_needed + 1):
        page_url = requests.get("https://news.ycombinator.com/news?p=" + str(i))
        markup = page_url.content
        soup = BeautifulSoup(markup, "html.parser")

        fetch_title_data(soup, headlines, links, ranking)
        fetch_subtext_data(soup, scores, users, comments)

    # Determines how much excess content has been retrieved against pages_needed and removes most recent excess posts.
    excess_posts = (constant.POSTS_ON_PAGE * pages_needed) - post_arg
    headlines = headlines[:len(headlines) - excess_posts]
    links = links[:len(links) - excess_posts]
    scores = scores[:len(scores) - excess_posts]
    users = users[:len(users) - excess_posts]
    comments = comments[:len(comments) - excess_posts]
    ranking = ranking[:len(ranking) - excess_posts]

    return output_json(headlines, links, scores, users, comments, ranking)


def fetch_title_data(s, h, l, r):
    """
    Responsible for obtaining all relevant data contained in headings of all articles on current page
    :param s: BeautifulSoup object containing page data
    :param h: List associated with article headings
    :param l: List associated with article URIs
    :param r: List associated with article ranks
    """
    # Hackernews places heading and links in class "storylink", soup_titles contains all headings and links on web page
    soup_titles = s.find_all(attrs={"class": "storylink"})

    """
    Based on HTML standards employed by hacker news, For each element:
    in class 'storylink' -  heading is extracted and appended to list h
    with title 'href' - uri is extracted and appended to list l
    in class 'rank' - rank number is extracted and appended to list r
    """
    for title in soup_titles:
        try:
            headline = title.get_text().lstrip()
            if len(headline) > 256:     # If heading too long, shortened to 253 characters with '...' at end of string
                sys.stdout.write("The title of a post in your request has a long name. Name has been shortened.\n")
                headline = headline[:253] + "..."
                h.append(headline)
            else:
                h.append(headline)
        except AttributeError:      # If heading is non-existent for reasons beyond script control, AttributeError thrwn
            sys.stdout.write("A post in your request does not have a title. title 'BLANK' has been given.\n")
            h.append("BLANK")

        link = title.get('href')
        l.append(link)

    soup_ranks = s.find_all(attrs={"class": "rank"})
    for rank in soup_ranks:
        r.append(rank.get_text().replace('.', ''))      # Each rank string contains numeric characters only


def fetch_subtext_data(s, scr, u, c):
    """
    Responsible for obtaining all relevant data contained in sub-headings of all articles on current page
    :param s:   BeautifulSoup object containing page data
    :param scr: List associated with article score
    :param u:   List associated with article submission user
    :param c:   List associated with article comment count
    """
    # Hackernews places score, user & comment data of each article in class "subtext", soup_subtext contains all this
    soup_subtext = s.find_all(attrs={"class": "subtext"})
    """
    During production it was realised subtext elements are optional. Some posts do not have users/score/comments.
    For this reason, I implemented try/except operations in sections of code where operations were vulnerable to factors
    beyond my control. Though, most likely to occur with subtext data, try/except was also placed in heading data in
    fetch_title_data.
    For each article's subtext: score is obtained and appended to list scr
                                user is obtained and appended to list u
                                comment count is obtained and appended to list c
    """
    for subtext in soup_subtext:
        try:
            score = subtext.select_one("span.score").get_text()     # All score values are contained in span.class:score
            score = ''.join(char for char in score if char.isdigit())   # Non-numeric chars are removed from var score
            if not int(score) >= 0:     # If numeric value of score is invalid(not equal to or larger than 0):
                sys.stdout.write("A post in your request had an invalid score. Value '0' has been given.\n")
                scr.append(0)
            else:
                scr.append(score)
        except AttributeError:  # If article contains no comment value (as field is optional), value 0 is given
            sys.stdout.write("A post in your request does not have a score. Value '0' has been given.\n")
            scr.append(0)

        try:
            user = subtext.select_one("a.hnuser").get_text()    # All user values are contained in a.class:hnuser
            if len(user) > 256:  # If user's handle is < 256 chars, shortened to 253 then '...' added to end of string
                sys.stdout.write("The author of a post in your request has a long name. Name has been shortened.\n")
                user = user[:253] + "..."
                u.append(user)
            else:
                u.append(user)
        except AttributeError:  # If article contains no submission user value (optional field), value NOUSER is given
            sys.stdout.write("A post in your request does not have a user. Value 'NOUSER' has been given.\n")
            u.append("NOUSER")

        try:
            # All comment values are contained in the last <a> element of parent 'subtext' class element
            comment = subtext.find_all("a")[-1].get_text()
            # Comment fields contained # of comments followed by "xa0comments", below line removes HTML delimiter
            comment, sep, tail = comment.partition("xa0")
            comment = ''.join(char for char in comment if char.isdigit())  # Ensures any remaining chars are numeric
            if comment is "":   # If not numeric value is contained in comment <a>, suggesting no comments exist:
                sys.stdout.write("A post in your request has no comments. Value '0' has been given.\n")
                comment = 0
            c.append(comment)
        except AttributeError:  # If article contains no comments (incl. xa0comments delimiter), value 0 is given.
            sys.stdout.write("A post in your request has no comments. Value '0' has been given.\n")
            c.append(0)


def output_json(h, l, s, u, c, r):
    """
    Responsible for translating list data to valid JSON string - as specified in requirements.
    :param h: List associated with all article headings
    :param l: List associated with all article links
    :param s: List associated with all article scores
    :param u: List associated with all articles' submission users
    :param c: List associated with all articles' comment counts
    :param r: List associated wtih all articles' ranking
    :return: STDOUT of valid JSON String
    """
    json_string = ""
    for post in range(0, len(h)):   # Although size of list H is used, all lists should have identical size.
        heading_str = str(h[post])
        user_str = str(u[post])
        """
        During production, it was realised some articles contain the character ' " ' within the title, which caused
        issues with delimiters in JSON files. The IF statement ensures if the char " is detected, char ' is used instead
        For error prevention reasons, the same was assumed possible with usernames where '' is used instead of "
        """
        if '"' in heading_str:
            h[post] = heading_str.replace('"', "'")
        if '"' in user_str:
            u[post] = user_str.replace('"', "''")

        json_string = json_string +\
                      '{"title":"'     + str(h[post]) + '",' \
                       '"uri":"'        + str(l[post]) + '",'\
                       '"author":"'     + str(u[post]) + '",'\
                       '"points":"'     + str(s[post]) + '",'\
                       '"comments":"'   + str(c[post]) + '",'\
                       '"rank":"'       + str(r[post]) + '"},'

    # As last string of JSON is ',', this is removed and brackets '[]' are placed at start&end of string
    json_string = "[" + json_string[:-1] + "]"
    json_parsed = json.loads(json_string)   # Using JSON lib, JSON string created from var json_string
    return sys.stdout.write(json.dumps(json_parsed, indent=2))


if __name__ == '__main__':
    main()

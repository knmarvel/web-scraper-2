import argparse
import re
import requests
import sys
from html.parser import HTMLParser

emails = []
urls = []
phones = []


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href" or attr[0] == "src":
                if attr[1].startswith("mailto"):
                    emails.append(attr[1][7:])
                if attr[1].startswith("/") and not attr[1].startswith("//"):
                    urls.append(attr[1])

    def handle_data(self, data):
        email_finder(data)
        url_finder(data)
        phone_finder(data)


def argparser(*args, **kwargs):
    """parse a URL passed in as a command line argument"""
    parser = argparse.ArgumentParser(
        description="Perform transformation on input text.")
    parser.add_argument('url',
                        help='url of website to search')
    return parser.parse_args()


def text_retriever(webpage):
    """retrieves the text of the webpage at the specified url"""
    print("Reading website, this may take a minute")
    r = requests.get(webpage)
    print("Done reading website")
    return r.text


def info_finder(web_text):
    """ look for email addresses, URLs, and phone numbers
    included in the web text"""
    html_parser = MyHTMLParser()
    html_parser.feed(web_text)


def email_finder(web_text):
    e_re = r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
    emails_found = re.findall(e_re, web_text)
    if emails_found:
        if len(emails_found[0]) == 1:
            emails.append(emails_found[0])


def url_finder(web_text):
    u_re = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
    u_re += r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls_found = re.findall(u_re, web_text)
    if urls_found:
        urls.append(urls_found[0])


def rel_url_finder(web_text):
    u_re = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
    u_re += r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls_found = re.findall(u_re, web_text)
    if urls_found:
        urls.append(urls_found[0])


def phone_finder(web_text):
    """returns phone numbers found in web_text"""
    p_re = r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})'
    p_re += r'\W*([0-9]{4})(\se?x?t?(\d*))?'
    phones_found = re.findall(p_re, web_text)
    actual_phone = ""
    if phones_found:
        for phone in phones_found:
            if len(phone) <= 5:
                actual_phone = ("({}){}-{}".format(
                    phone[0], phone[1], phone[2]))
        phones.append(actual_phone)


def main(*args):
    webpage = argparser().url
    web_text = text_retriever(webpage)
    info_finder(web_text)
    if phones:
        print("Here are the phone numbers found in this website:")
        for phone in sorted(phones):
            print(phone)
    else:
        print("No phone numbers found.")
    if emails:
        deduped_emails = sorted(list(set(emails)))
        print("Here are the email addresses found in this website:")
        for email in deduped_emails:
            print(email)
    else:
        print("No emails found.")
    if urls:
        deduped_urls = sorted(list(set(urls)))
        print("Here are the urls found in this website:")
        for url in deduped_urls:
            if url.startswith("/"):
                url = webpage[:-1] + url
            print(url)
    else:
        print("No urls found.")


if __name__ == "__main__":
    main(sys.argv[1:])



In Activity: Simple Web Scraper, we used regular expressions to search the entire text of an HTML page for absolute URLs (those explicitly beginning with "http://" or "https://"). However, this misses lots of relative URLs linking to images or pages within the same domain. Let's extend the web scraper you've built so far to make sure it can also find relative URLs in <A HREF="..."> and <IMG SRC="..."> tags.

To help with this, use the HTMLparser (Links to an external site.)Links to an external site. from the standard library to explicitly recognize A and IMG tags, and access their HREF and SRC attributes. This will be in addition to the regex searches already used in your scraper. (If you prefer, you may use the Beautiful Soup library instead of HTMLparser at your discretion).

Note: you should deduplicate the urls, emails, and phone numbers found by your scraper. A set() can be an easy way to remove duplicates in a collection.




Today you'll write a command line program to scrape a single web page, extracting any URLs, email addresses, and phone numbers it contains.

    Use the argparse (Links to an external site.)Links to an external site. library to parse a URL passed in as a command line argument.
    Use the requests (Links to an external site.)Links to an external site. library to retrieve the text of the webpage at the specified URL.
    Use the re (Links to an external site.)Links to an external site. library to look for email addresses, URLs, and phone numbers included in the page.

Example command

$ python scraper.py http://kenzie.academy/

Example output


URLS:

http://graph.facebook.com/10155390232446072/picture?type=square
http://instagram.com/kenzieacademy
http://ogp.me/ns/website
  ...
https://www.facebook.com/tr?id=1694339123974624&ev=PageView&noscript=1
https://www.facebook.com/tr?id=261245144685629&ev=PageView&noscript=1
https://www.forbes.com/sites/allisondulinsalisbury/2019/01/25/staffing-company-and-coding-school-partner-to-provide-education-and-a-job-all-in-one/
https://www.googletagmanager.com/gtag/js?id=AW-829013385
https://www.googletagmanager.com/gtm.js?id=
  ...
https://www.kenzie.academy/program-cost?utm_source=v2homepage&utm_campaign=March2019update&utm_content=programcostbanner
https://www.kenzie.academy/software-engineering?utm_source=v2homepage&utm_campaign=March2019update&utm_content=seprogrampage
https://www.kenzie.academy/ux-engineer?utm_source=v2homepage&utm_campaign=March2019update&utm_content=uxprogrampage
https://www.linkedin.com/company/kenzie-academy/
https://youtu.be/BUPZXxkiHYM?loop=1 

EMAILS: 

info@kenzie.academy 

PHONE NUMBERS: 

None 

The ellipses ("...") in the above example denote sections of the output that have been omitted for brevity.
Note on parsing HTML

In general, regular expressions are not well suited for parsing HTML. In this case, the patterns you are looking for are relatively simple. Try using re.findall together with the regular expressions from:

    urlregex.com (Links to an external site.)Links to an external site.
    emailregex.com (Links to an external site.)Links to an external site.
    phoneregex.com (Links to an external site.)Links to an external site.

You may find you need to tweak the patterns a bit for your application. For example, if you're using re.findall to search for emails in a large block of text, your pattern shouldn't use the ^ and $ meta-characters to limit matches to the full string.

You should be able to get some useful initial results, but you may also see some spurious results due to regular expressions matching text within <script> blocks, for example.

You can experiment with using regular expressions to strip tags by doing things like:

re.sub(r"<[^>]*>", " ", text)

Before going too far down this path however, you may also find it worthwhile to explore the HTMLParser (Links to an external site.)Links to an external site. library, which can give you more robust options for navigating an HTML document.
Output

Your scraper doesn't have to conform to a specific output format, but running it with a command like:

python scraper.py http://kenzie.academy/

Should output some reasonably formatted text listing the URLs, email addresses, and phone numbers found in the page.
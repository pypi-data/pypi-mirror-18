# meds/kernel/begint.py
#
#

""" woorden die beginnen met ... """

from mads.url import get_url, strip_html


url = "http://www.woorden.org/begint.php?woord=%s" 

def begint(event):
    import bs4
    text = get_url(url % event._parsed.rest)
    if text:
        try: soup = bs4.BeautifulSoup(text, "lxml")
        except: soup = bs4.BeautifulSoup(text)
        res = ""
        for chunk in soup.findAll("a"):
            if isinstance(chunk, bs4.CData):
                res += str(chunk.content[0]) + " "
            else:
                res += str(chunk) + " "
        data = strip_html(res)
        event.reply(", ".join([x for x in data.split() if event._parsed.rest in x]))

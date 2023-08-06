# meds/kernel/eindigt.py
#
#

""" woorden die eindigen in ... """

from mads.url import get_url, strip_html

url = "http://www.woorden.org/eindigt.php?woord=%s" 

def eindigt(event):
    import bs4
    u = url % event._parsed.rest.strip()
    text = get_url(u)
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
        event.reply(", ".join([x for x in data.split() if event._parsed.rest in str(x)]))

# evrm/version.py
#
#

def version(event):
    from evrm import __version__, __txt__
    event.reply("EVRM #%s %s" % (__version__, __txt__))

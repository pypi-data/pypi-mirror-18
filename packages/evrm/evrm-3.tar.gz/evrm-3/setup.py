#!/usr/bin/env python3
#
#

import os
import sys
import os.path

def j(*args):
    if not args: return
    todo = list(map(str, filter(None, args)))
    return os.path.join(*todo)

if sys.version_info.major < 3:
    print("you need to run mads with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

target = "evrm"
upload = []

def uploadfiles(dir):
    upl = []
    if not os.path.isdir(dir):
        print("%s does not exist" % dir)
        os._exit(1)
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if not os.path.isdir(d):
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl

def uploadlist(dir):
    upl = []

    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)

    return upl

setup(
    name='evrm',
    version='3',
    url='https://bitbucket.org/thatebart/evrm',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="antipsychotica - akathisia - katatonie - sedering - shocks - lethale katatonie !!!".upper(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["mads",],
    scripts=["bin/evrm-docs", "bin/evrm"],
    packages=['evrm', ],
    long_description='''EVRM

In 2012 heb ik het Europeese Hof voor de Rechten van de Mens aangeschreven om een klacht tegen Nederland in te dienen.
De klacht betrof het afwezig zijn van verpleging in het nieuwe ambulante behandeltijdperk van de GGZ.
Uitspraak is niet-ontvankelijk.
Het EVRM is voor de GGZ patient een doodlopende weg.

Het is pas na tussenkomst van de koningin mogelijk om aangifte te kunnen.
De Hoge Raad concludeert dat het geen verantwoordelijkheid heeft.
Het verwijst vervolgens naar het IGZ, die geen structurele onzorgvuldigheid in de afhandeling van klachten bij GGZ-NHN constrateert.
De IGZ heeft erkent verantwoordelijk te zijn voor ambulante zorg, zowel voor vrijwillig als onder de BOPZ behandelde patienten, zie quote.
De GGZ patient als slachtoffer word de rechtsgang naar de strafrechter geblokkeerd.

Het is niet mogelijk voor de koningin om verdere tussenkomst te verlenen vanwege ministeriele verantwoordelijkheid.
De Minister van VWS ontkent problemen met de extramuralisering van Nederland.

CONTACT

| Bart Thate
| botfather on #dunkbots irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com

| MADS is sourcecode released onder een MIT compatible license.
| MADS is een event logger.

''',
   data_files=[("docs", ["docs/conf.py","docs/index.rst"]),
               (j('docs', 'jpg'), uploadlist(j("docs","jpg"))),
               (j('docs', 'txt'), uploadlist(j("docs", "txt"))),
               (j('docs', '_templates'), uploadlist(j("docs", "_templates")))
              ],
   package_data={'': ["*.crt"],
                 },
   classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)

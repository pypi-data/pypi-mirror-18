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
    version='2',
    url='https://bitbucket.org/thatebart/evrm',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="antipsychotica - akathisia - katatonie - sedering - shocks - lethale katatonie !!!".upper(),
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["mads",],
    scripts=["bin/evrm-docs", "bin/evrm"],
    packages=['evrm', "muds"],
    long_description='''"Hoezo schadelijk?"

Antipsychotica zijn levenbedreigend, toedienen brengt de kans op sterven:

| Antipsychotica zijn giftig, zie :ref:`toxic <toxic>`
| Antipsychotica zijn giftig, zie de bijsluiter van bijv. :ref:`clozapine <clozapine>`.
| Toedienen van antipsychotica maakt dat de patient te maken krijgt met vergiftigings :ref:`symptomen <symptomen>`.
| bron: https://vergiftigingen.info

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

#!/usr/bin/env python3

from xml.dom import minidom
from datetime import datetime
import subprocess
import sys

allargs = ""

xmlsrcfile = input("Enter the RSS feed's page address: ")
if not bool(xmlsrcfile):
    xmlsrcfile = 'planetjarre.podigee.io/feed/mp3'  # default RSS file if none is given
    print("***\n*** No value entered, using " + xmlsrcfile + "\n***")

xmldestfile = 'rss.xml'  # target file for RSS XML
subprocess.run(['wget', xmlsrcfile, '-O', xmldestfile])  # get the RSS XML file
default_enclosurename = "rtrvpod_NONAME.txt"

rss_dom = minidom.parse(xmldestfile)  # Use minidom to read the XML file into memory
xml_items = rss_dom.getElementsByTagName('item')  # all the episode info is under <item> tags

# Characters that need to be replaced in filenames, this list is extendable.
replace_dict = {
    '/' : '\u2215',
    '\n' : ''
}

dry_run = False
indexSubtract = 0
# Parse arguments.
for i in range(1, len(sys.argv)):
    if (sys.argv[i] == '--dry-run') or (sys.argv[i] == '-dry-run'):
        print("** Doing a dry run, no episode downloads performed. **")
        dry_run=True
    elif (sys.argv[i] == '--zero') or (sys.argv[i] == '-zero') or (sys.argv[i] == '-z'):
        print("\u2020\u2020 Starting episode numbering at ZERO \u2020\u2020")
        indexSubtract = 1
    else: # accumulate the remaining arguments for passing to wget
        allargs += sys.argv[i] + " "

n = len(xml_items) - indexSubtract
for item in xml_items:  # loop through all <item>s
    # Retrieve the episode title.  Replace any invalid character with its alternative from
    # the translation table, e.g. '/' to U+2215 because OSes don't like '/' in filenames.
    title = item.getElementsByTagName('title')[0].firstChild.nodeValue.translate(str.maketrans(replace_dict))
    # Grab the publication date, and trim off the timezone.
    try:
        pubDate = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue.rsplit(' ', 1)[0]
    except:
        pubDate = "Thu, 01 Jan 1970 00:00:00"  # Use Epoch in case no date is supplied.
    # And most importatly, grab the audio file.
    try:
        enclosure = item.getElementsByTagName('enclosure')[0].getAttribute('url')
    except:
        enclosure = default_enclosurename  # In case there's no attachment for the <item>.
    # Get the file extension.
    # - Start by removing any separator (all after a ?)
    audio = enclosure.rsplit('?')[0]
    # - get the file extension
    fileExt = audio.rsplit('.', 1)[1]
    # Read the time into a time object.
    dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
    # Create the file name which is: episode number. episode name - YYYY-MM-DD.ext
    filename = str(n).zfill(4) + ". " + title + " - " + dt.strftime("%Y-%m-%d") + "." + fileExt
    # Keep count of the number of the episode, starting at the most recent.
    n -= 1
    if (enclosure != default_enclosurename) and (not dry_run):
        # Download the episode, renaming it in the process.
        subprocess.run(['wget', *allargs.split(), enclosure, '-O', filename])
    else:
        # In case of no attachment or doing a dry-run, create an empty filename.
        subprocess.run(['touch', "-t", dt.strftime("%y%m%d%H%M"), filename])
    # Write the xml feed URL to a file
    with open("feedURL.txt", "w") as feedfile:
        feedfile.write(xmlsrcfile + "\n")

#!/usr/bin/env python3

from xml.dom import minidom
from datetime import datetime
import subprocess
import sys

# Initialize variables
allargs = ""
artwork = ""
dry_run = False
indexSubtract = 0
formatxml = False
numbering = True
usage = False
xmldestfile = 'rss.xml'  # target file for RSS XML
formatted_rssxml = 'formatted_rss.xml'
default_enclosurename = "rtrvpod_NONAME.txt"
replace_dict = {  # Characters to replace in filenames, this list is extendable.
    '/' : '\u2215',
    '\n' : ''
}

# Parse arguments.
for i in range(1, len(sys.argv)):
    if (sys.argv[i] == '--dry-run') or (sys.argv[i] == '-dry-run'):
        print("** Doing a dry run, no episode downloads performed. **")
        dry_run = True
    elif (sys.argv[i] == '--zero') or (sys.argv[i] == '-zero') or (sys.argv[i] == '-z'):
        print("\u2020\u2020 Starting episode numbering at ZERO \u2020\u2020")
        indexSubtract = 1
    elif (sys.argv[i] == '--help') or (sys.argv[i] == '-help') or (sys.argv[i] == '-h'):
        usage = True
    elif (sys.argv[i] == '--formatxml') or (sys.argv[i] == '-formatxml'):
        print(f"\u2021\u2021 Output file '{formatted_rssxml}' will be written \u2021\u2021")
        formatxml = True
    elif (sys.argv[i] == '--nonum') or (sys.argv[i] == '-nonum') or (sys.argv[i] == '-nn'):
        print("\u2058\u2058 Files will not be numbered \u2058\u2058") 
        numbering = False
    else: # accumulate the remaining arguments for passing to wget
        allargs += sys.argv[i] + " "

# If the caller requested usage instructions, print those here
if usage:
    print("Usage: rtrvpod.py [arg1] [arg2] ... [argN]")
    print("")
    print("Where arguments can be:")
    print(" --dry-run   : Create empty files rather than download audio files.")
    print(" --formatxml : Create a formatted .xml file from ./rss.xml and quit.")
    print(" -h, --help  : Print usage instructions.")
    print("-nn, --nonum : Don't prefix filenames with a number.")
    print(" -z, --zero  : Start episode numbering at 0 (default 1).")
    print("")
    print("Any other options get passed to wget verbatim.")

    exit(0)
# If the caller requested a formatted xml file, make one and exit
if formatxml:
    try:
        xmldata = minidom.parse(xmldestfile)
    except:
        print(f"ERROR: Can't parse {xmldestfile}")
        exit(1)
    with open(formatted_rssxml, "w") as file:
        formattedxml = xmldata.toprettyxml()  # prettify xml
        # fix some prettyxml formatting
        formattedxml = '\n'.join([s for s in formattedxml.splitlines() 
                                  if s.strip()]) # remove double spacing
        formattedxml = formattedxml.replace("\n<![CDATA", "<![CDATA")
        file.write(formattedxml)
        exit(0)

xmlsrcfile = input("Enter the RSS feed's page address: ")
if not bool(xmlsrcfile):
    xmlsrcfile = 'planetjarre.podigee.io/feed/mp3'  # default RSS file if none is given
    print("***\n*** No value entered, using " + xmlsrcfile + "\n***")

subprocess.run(['wget', xmlsrcfile, '-O', xmldestfile])  # get the RSS XML file

rss_dom = minidom.parse(xmldestfile)  # Use minidom to read the XML file into memory
xml_items = rss_dom.getElementsByTagName('item')  # all the episode info is under <item> tags

# Get the podcast artwork if available
try:
    # The podcast artwork is (usually) under <image>
    image_items = rss_dom.getElementsByTagName('image')
    artwork = image_items[0].getElementsByTagName('url')[0].firstChild.nodeValue
except:
    try:
        # If not under <image>, see if there's artwork under <itunes:image>
        image_items = rss_dom.getElementsByTagName('itunes:image')
        artwork = image_items[0].getAttribute('href')
    except:
        artwork = ""

if artwork != "":
    # Remove all after the '?' and separate basename from dirname, that's the file name.
    artwork_file = artwork.rsplit('?')[0].rsplit('/', 1)[1]
    if (not dry_run):
        subprocess.run(['wget', artwork, '-O', artwork_file])  # Get the RSS XML file.
    else:
        subprocess.run(['touch', artwork_file])  # Create an empty file if in dry-run.

# Loop through all <item>s and get the audio file(s).
n = len(xml_items) - indexSubtract
for item in xml_items:
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
    if (numbering):
        filename = str(n).zfill(4) + ". " + title + " - " + dt.strftime("%Y-%m-%d") + "." + fileExt
    else:
        filename = dt.strftime("%Y-%m-%d") + " - " + title + "." + fileExt
    # Keep count of the number of the episode, starting at the most recent.
    n -= 1
    if (enclosure != default_enclosurename) and (not dry_run):
        # Download the episode, renaming it in the process.
        subprocess.run(['wget', *allargs.split(), enclosure, '-O', filename])
    else:
        # In case of no attachment or doing a dry-run, create an empty filename.
        subprocess.run(['touch', "-t", dt.strftime("%y%m%d%H%M"), filename])

# Write the xml feed URL to a file.
with open("feedURL.txt", "w") as feedfile:
    feedfile.write(xmlsrcfile + "\n")

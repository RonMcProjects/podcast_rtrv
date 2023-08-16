#!/usr/bin/env python3

from xml.dom import minidom
from datetime import datetime
import subprocess
from subprocess import DEVNULL

xmlsrcfile = input("Enter the RSS feed's page address: ")
if not bool(xmlsrcfile):
    xmlsrcfile = "planetjarre.podigee.io/feed/mp3"  # default RSS file if none is given
    print("***\n*** No value entered, using " + xmlsrcfile + "\n***")

xmldestfile = 'rss.xml'  # target file for RSS XML
subprocess.run(['wget', xmlsrcfile, '-O', xmldestfile])  # get the RSS XML file

rss_dom = minidom.parse(xmldestfile)  # Use minidom to read the XML file into memory
xml_items = rss_dom.getElementsByTagName('item')  # all the episode info is under <item> tags

n = len(xml_items)
for item in xml_items:  # loop through all <item>s
    # Grab the episode title, replace any slashes '/' with
    # U+2215 because OSes don't like '/' in file names.
    title = item.getElementsByTagName('title')[0].firstChild.nodeValue.replace("/", "\u2215")
    # Grab the publication date, and trim off the timezone.
    pubDate = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue.rsplit(' ', 1)[0]
    # And most importatly, grab the audio file.
    audio = item.getElementsByTagName('enclosure')[0].getAttribute("url")
    # Get the file extension.
    fileExt = audio.rsplit('.', 1)[1][:3]
    # Read the time into a time object.
    dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
    # Create the file name which is: episode number. episode name - YYYY-MM-DD.ext
    filename = str(n).zfill(4) + ". " + title+ " - " + dt.strftime("%Y-%m-%d") + "." + fileExt
    # Keep count of the number of the episode, starting at the most recent.
    n -= 1
    # Download the episode, renaming it in the process.
    subprocess.run(['wget', audio, '-O', filename])

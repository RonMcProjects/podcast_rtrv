#!/usr/bin/env python3

from xml.dom import minidom
from datetime import datetime
import subprocess

xmlsrcfile = "planetjarre.podigee.io/feed/mp3"  # default RSS file if none is given
xmldestfile = 'rss.xml'                         # target file for RSS XML
subprocess.run(['wget', xmlsrcfile, '-O', xmldestfile]) # get the RSS XML file

rss_dom = minidom.parse(xmldestfile)  # Use minidom to read the XML file into memory
xml_items = rss_dom.getElementsByTagName('item') # In a podcast, all the episode info in under <item> tags

n = len(xml_items)
for item in xml_items:  # loop through all <item>s
    # Grab the episode title, replace any slashes / with U+2215 because OSes don't like it in file names.
    title = item.getElementsByTagName('title')[0].firstChild.nodeValue.replace("/", "∕")
    # Grab the publication date, and trim off the timezone.
    pubDate = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue.rsplit(' ', 1)[0]
    # And most importatly, grab the audio file.
    audio = item.getElementsByTagName('enclosure')[0].getAttribute("url")
    # Get the file extension
    fileExt = audio.rsplit('.', 1)[1][:3]
    # Read the time into a time object
    dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')
    # Create the file name which is
    #   episode number, followed by
    #   episode name, followed by
    #   episode date in YYYY-MM-DD format
    filename = str(n).zfill(3) + ". " + title+ " - " + dt.strftime("%Y-%m-%d") + "." + fileExt
    # keep count of the number of the episode, starting at the most recent
    n -= 1
    # Get the episode, renaming it in the process
    subprocess.run(['wget', audio, '-O', filename])

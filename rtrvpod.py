#!/usr/bin/env python3

from xml.dom import minidom
from datetime import datetime
import subprocess

xmlsrcfile = "planetjarre.podigee.io/feed/mp3"
xmldestfile = 'rss.xml'
subprocess.run(['wget', xmlsrcfile, '-O', xmldestfile])

rss_dom = minidom.parse(xmldestfile)
xml_items = rss_dom.getElementsByTagName('item')

n = len(xml_items)
for item in xml_items:
    title = item.getElementsByTagName('title')[0].firstChild.nodeValue.replace("/", "∕")
    pubDate = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue
    audio = item.getElementsByTagName('enclosure')[0].getAttribute("url")
    dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %z')
    filename = str(n).zfill(3) + ". " + title+ " - " + dt.strftime("%Y-%m-%d") + ".m4a"
    n -= 1
    subprocess.run(['wget', audio, '-O', filename])

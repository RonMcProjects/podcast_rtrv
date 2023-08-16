# podcast_rtrv
This is a simple utility for downloading all the episodes of a podcast.
It prompts the user for a web link to a podcast's RSS feed in XML format.
The utility will fetch the XML file and use it to download all episodes listed therein.

The utility will name the file according to the metadata's **title** and its **pubDate**.
It numbers them from the oldest to the newest.

This has been tested on Linux, Cygwin and MacOS.
It requires *python3* and *wget*.

e.g. To download the Mandolin Minute podcast
```bash
./rtrvpod.py
Enter the RSS feed's page address: https://anchor.fm/s/110b41c/podcast/rss
```
The podcast files will end up in the current directory along with the file rss.xml,
which is a copy of the RSS file.
It can be referred to in order to glean additional metadata about each episode.

If no path is provided (i.e. the user presses <ENTER> without providing a web link to an RSS),
then a default podcast is downloaded.

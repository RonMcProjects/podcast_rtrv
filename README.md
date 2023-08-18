# podcast_rtrv
This is a simple utility for downloading all the episodes of a podcast.
It prompts the user for a web link to a podcast's RSS feed in XML format.
The utility will fetch the XML file and use it to download all episodes listed therein.

The utility will name the files according to the metadata's **title** and **pubDate**.
It numbers them from the oldest to the newest.

This has been tested on Linux, Cygwin and MacOS.
It requires *python3* and *wget*.

e.g. To download the Mandolin Minute podcast
```bash
./rtrvpod.py
Enter the RSS feed's page address: https://anchor.fm/s/110b41c/podcast/rss
```
Any command-line arguments get passed directly to *wget*. For example with
```bash
./rtrvpod.py --spider -nv
```
the argument ```--spider``` tells *wget* to run without downloading any files, and ```-nv```
tells *wget* to run in non-verbose mode.

The podcast files will end up in the current working directory, along with the file rss.xml
which contains the metadata for the podcast.

If no path is provided (i.e. the user presses ENTER without providing a web link to an RSS),
then a default podcast ```planetjarre.podigee.io/feed/mp3``` is downloaded.

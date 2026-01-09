# podcast_rtrv
This is a simple utility for downloading all the episodes of a podcast.
It prompts the user for a web link to a podcast's RSS feed in XML format.
The utility will fetch the XML file and use it to download all episodes listed therein.
It will also fetch the podcast artwork.

The utility will name the files according to the metadata's **title** and **pubDate**.
It defaults to numbering them from the oldest to the newest, with an option to exclude numbering altogether.

This has been tested on Linux, Cygwin and MacOS.
It requires *python3*, *touch*, and *wget*.

e.g. To download the Mandolin Minute podcast
```bash
rtrvpod.py
Enter the RSS feed's page address: https://anchor.fm/s/110b41c/podcast/rss
```
You can do a dry run that won't download any files with the option ```--dry-run```
```bash
rtrvpod.py --dry-run
```
You can tell the program to start numbering episodes at zero, used for example if there's a trailer episode.  Otherwise numbering starts at 1.
```bash
rtrvpod.py --zero
```
To get the usage instructions, use
```bash
rtrvpod.py --help
```
To turn off numbering, in which case the publication date comes first in the filename to provide a sorting order.
```bash
rtrvpod.py --nonum
```
If you pass in the argument ```--html```, every episode description will be saved as an html file alongside the audio file.
```bash
rtrvpod.py --html
```
Any other command-line arguments get passed directly to *wget*. For example with
```bash
rtrvpod.py --no-clobber -nv
```
the argument ```--no-clobber``` tells *wget* to run without overwriting any files, and ```-nv```
tells *wget* to run in non-verbose mode.

The podcast files will end up in the current working directory, along with the file ```rss.xml``` which contains the metadata for the podcast.
The feed URL that was provided will be written to a file ```feedURL.txt``` for future reference.

Sometimes the downloaded rss.xml file has no line breaks.  You can use rtrvpod to create a human-readable file ```formatted_rss.xml```.  If used, this option exits without downloading anything and ignores other parameters.
```bash
rtrvpod.py --formatxml
```
If no path is provided (i.e. the user presses ENTER without providing a web link to an RSS),
then a default podcast ```planetjarre.podigee.io/feed/mp3``` is downloaded.

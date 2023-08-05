# Anime Updater

The Anime updater script allows you to define a list of shows in a simple
python file which will be continuously updated to their most current state.

This is perfect for currently airing shows.

## Creating the script

A sample script which is pretty much self-explanatory can be found
[here](../../toktokkie/templates/anime_updater_template.py). 

Let's walk through the script step-by step:

```python
#!/usr/bin/python
```

This is the 'shebang' line which tells your shell with which program the
script should be executed with. It's not strictly necessary, you can
also call the script using the ```python``` command directly.

```python
from toktokkie.scripts.anime_updater import start
```

This imports the actual script that does the heavy lifting. For this to
work, toktokkie must be installed on your local system and importable
by python, i.e. in you python path. Tools like pip should do this for
you automatically.

```python
search_engines = ["Horriblesubs",
                  "NIBL.co.uk",
                  "ixIRC.com",
                  "intel.haruhichan.com"]
```

This is a list of XDCC search engines to use. To make the script run
faster, you can remove some of these search engines, but keep in mind
that you may be missing out on some search results, as none of these
search engines can find everything available.

```python
config = [

    {"target_directory": "Target Directory 1",
     "horriblesubs_name": "Show Name 1",
     "bot": "Bot Name 1",
     "quality": "1080p",
     "season": "Season Number 1"},

    {"target_directory": "Target Directory 2",
     "horriblesubs_name": "Show Name 2",
     "bot": "Bot Name 2",
     "quality": "720p",
     "season": "Season Number 2"}

]
```

Here you can define which shows you want to update with this script.
Each show is defined as a python dictionary (the parts surrounded by
{curly braces} are called a dictionary) seperated by commas. In these
dictionaries we define 5 parameters for the show:

1. **target_directory**
   The directory in which the downloaded files will be stored.
   Can be a relative or absolute path, but keep in mind that relative
   paths will be determined by the current working directory, NOT the
   script's loaction.
2. **horriblesubs_name**
   The name for the show as defined by horriblesubs (or another fansub
   group of your liking)
3. **bot**
   The name of the bot from which you want to download the show.
   This ensures that you will connect to a bot that you know has a good
   connection to your location
4. **quality**
   The quality requested. Should always be something like 480p, 720p or
   1080p. Series that don't have a quality indicator in their filenames
   ignore this setting. It is however still requires for shows that DO
   specify the quality
5. **season**
   The season of the show to download.
   
Now, to starting the actual script:
   
```python
start(config, search_engines)
start(config, search_engines, continuous=True)
start(config, search_engines, continuous=True, looptime = 3600)
```

Only have ONE of these commands in your script!
These commands start the script's main function, but they all act a bit
differently.

```python
start(config, search_engines)
```

This command just starts the script and runs it once

```python
start(config, search_engines, continuous=True)
```

This command starts the script and keeps running it continuously
indefinitely

```python
start(config, search_engines, continuous=True, looptime = 3600)
```

This command also runs the script continuously, with a specified
interval between loops

This is the entirety of the script!

## What the script does
 
It creates a directory structure like this:

    -showname
    --season x
    --.icons
    
for each show specified in the script, if it does not exist that way yet.

Then it checks the existing episodes (if there are any) that their
file names actually match the episode name on thetvdb.com in the
following format:

    Showname - SXXEXX - EpisodeTitle

and if that is not the case, the files are renamed to the correct episode
title.

Afterwards, it searches the specified search engines for new episodes of
the show. If any are found, they are downloaded and renamed according
to the naming scheme seen above.

## RSS Function

The script can also be used to generate an OPML file that can be imported
by most RSS Readers from the script configuration.

To do this, just call the command like you would when updating, but
add the 'rss' command line argument as well.
# XDCC-DL

A simple command line script that comes bundled with toktokkie. You can
call it using the ```xdcc-dl``` command.

## Usage:

As the script uses argsparse to parse the command line arguments,
you can call the script with the ```--help``` flag to see which options
are available. Here's a quick rundown:

### packstring

This is the xdcc string you'll get from most XDCC packlist sites.
It's formatted like this:

    /msg BOTNAME xdcc send #PACKNUMBER

This string needs to be surrounded by quotation marks to work

### --dest

The destination of the downloaded file. Can be either an existing
directory or a non-existant file path.

If the destination is an existing directory, the file will retain
the original file name.

If the option is omitted, the file will retain the original filename
and be stored in the current working directory

### --server

Can be used to specify which irc server to use. 

If the option is omitted, the script will search the most popular
irc servers for bot matches

## Basic Examples

    xdcc-dl "/msg Bot xdcc send #1"
    
This command will download pack 1 from Bot and store it with its
original filename in the current working directory

    xdcc-dl "/msg Bot xdcc send #123" --dest=/home/user/Downloads/file.txt --server=irc.server.net
    
This command will download pack 123 from Bot and store it as
/home/user/Downloads/file.txt by connecting to the irc.server.net
IRC server.
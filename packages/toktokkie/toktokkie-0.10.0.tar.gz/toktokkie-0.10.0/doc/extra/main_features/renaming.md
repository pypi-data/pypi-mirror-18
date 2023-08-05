# Renaming Episodes

The Renaming feature of Tok Tokkie Media Manager allows the user to specify a directory. Every subdirectory of this directory
will be checked for a .icons subdirectory. If a .icons subdirectory is present, all of the sibling subdirectories'
children files will be renamed using data from thetvdb.com in the format:

    Show Name - SXXEXX - Episode Name

An example:

    -- user-provided directory
     |-- directory 1
     |  |-- subdirectory 1
     |     |-- Season 1
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_01
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_02
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_03
     |	   |   |-- [TV]Super_Hyper_Interesting_TV_Show_04
     | 	   |-- .icons
     | 	   |-- Specials
     |-- directory 2
        |-- Season 1
        |   |-- Episode 1
        |   |-- Episode 2
        |   |-- Episode 3
        |   |-- Episode 4
        |-- Season 3
        |   |-- Episode 1
        |-- .icons

Given this directory tree, the directories 'subdirectory 1' and 'directory 2' will be used for renaming, as they
both contain a .icons subdirectory.

All other subdirectories' children (Episode 1, Episode 2, [TV]Super_Hyper_Interesting_TV_Show_01 etc.) will now be
renamed.

The information is determined like this:

Show Name:  This is the name of the parent directory of the .icons directory, in this case it would be 'directory 2'
or 'subdirectory 1'

Season Number:  This is determined by the individual subdirectory's names. For Example, 'Season 1' results in 1,
'Season 3' in 3. All directories that can't be parsed like this ('Specials', for example) are assigned the season
number 0.

Episode Number:  The alphabetical position of the file in the Season folder

Episode Name:  Determined by the database on thetvdb.com using the other gathered information
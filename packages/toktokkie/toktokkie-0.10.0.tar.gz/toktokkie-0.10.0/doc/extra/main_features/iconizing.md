# Iconizing Directories

The program can also automatically set folder icon properties of directories containing a .icons subdirectory.
The .icons directory can contain icon files (.png for normal operating systems, .ico for Windows) that match the name
of the other subdirectories. The exception to this rule is the main.png/main.ico file, which will be used to iconize the
parent directory.

An Example:

    -- user-provided directory
     |-- directory 1
       |-- subdirectory 1
          |-- Season 1
     	   |   |-- English
     	   |   |-- German
      	   |-- .icons
           |   |-- main.png
           |   |-- German.png
           |   |-- English.png
           |   |-- Season 1.png
           |   |-- Specials.png
      	   |-- Specials

This will set the folder icon of 'subdirectory 1' to '.icons/main.png', 'Season 1' to '.icons/Season 1.png',
'German' to '.icons/German.png' and so forth.

This is currently supported under Windows and Linux file managers that support gvfs metadata.
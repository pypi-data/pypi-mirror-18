ListDownloader
==============

About
-----
This program simply takes a list of files as argument and a directory to download the files, and it downloads them sequentially, or in parallel. The program gives the option to load the whole list, or do parts of the list at a time. An option also is provided for how many threads/processes to be used.

Installation
------------

(Installation was prepared for and tested with Debian Jessie.)

You can install the package with pip using

    # pip install listdownloader

OR you can use the scripts that are provided to do that (`run_build`, and `run_install`), which are available in the repository.

OR you can create the source installation package yourself using

    python3 setup.py sdist

and then use pip to install the package that will be built in the directory `dist`:

    # pip3 install listdownloader-x.y.z.tar.gz

where x.y.z is the current version of the program.

The program installs the package listdownloader and a script file for usage.

Running the script and using the package
----------------------------------------

The script can be executed (globally) using:

    $ downloadlist.py -f file.txt -d destination -t threads -l lines

where:
    `file.txt` is the file name/path with the list of URLs to be downloaded
    `destination` is the path, to which the files should be downloaded
    `threads` is the number of processes to be used to download the URLs simultaneously
    `lines` is the number of lines to read from the files and read simultaneously. 0 leads to reading the whole file.

You may use the package in your own scripts by importing it:

    import listdownloader

then you can download a list of files using:

    listdownloader.download_files(URLs, destination, num_threads)

where:
    `URLs` is a list of the URLs to be downloaded
    `destination` is a string with the path, at which the files have to be saved
    `num_threads` is the number of threads/processes to use for the download.

You can also download a single file using the function:

    listdownloader.download_file(URL, destination)

License
-------
MPL

About
-----
This script was written by Samer Afach, samer@afach.de for test purposes.

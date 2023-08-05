Fling
-----

Simple CLI for file sharing over HTTP.

More importantly, no user or server setup is required.  After the transfer 
is complete, no open ports or servers are left running.

Installation
------------

    pip install fling

Usage Examples
--------------

Share a single file::

    fling  <file>

*This will create a URL for the file.*

Share a directory::

    fling <dir>

*This will create a ZIP archive of the directory and create a URL to share the archive.*

Share a multiple files::

    fling <file1> <file2> <file3>

*This will create a ZIP archive of the files and create a URL to share the archive.*

Share multiple files and directories::

    fling <file1> <file2> <dir>

*This will create a ZIP archive of files and directories and create a URL to share the archive.*

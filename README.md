# SyncMessCleaner
Python program to clean the mess you and or Syncthing may have accidentally created.

Usage:
python3 SyncMessCleaner.py /path/to/base/directory

It will go recursively through /path/to/base/directory looking for .sync-conflict.
After that it will generate CRC32 hashes of the files and the corresponding originals.
If the hashes match, the conflicting file will be deleted.

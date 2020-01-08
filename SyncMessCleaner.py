import sys
import os
import zlib


def crc(file):
    prev = 0
    for eachLine in open(file, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return prev & 0xFFFFFFFF


def get_recursive_file_list(file_base='./', search_pattern='.sync-conflict', exclude_folders=[]):
    file_list = []
    for root, dirs, files in os.walk(file_base, topdown=True):
        for file in files:
            dirs[:] = [d for d in dirs if d not in exclude_folders]
            if search_pattern in file:
                if not file.endswith(".tmp"):  # This is to prevent scanning files which are currently being downloaded
                    print("Found: " + os.path.join(root, file))
                    file_list.append([root, file])
    return file_list


def main(base_path):
    if os.path.isdir(base_path):
        print("Will work on: " + base_path)
        todo_list = get_recursive_file_list(base_path, exclude_folders=['.stversions'])
        print("Finished building ToDo list. Will begin with checking:")
        for directory, conflict_file_name in todo_list:
            # extract file extension from filename info:
            extension = os.path.splitext(conflict_file_name)
            if len(extension) < 2:
                print("Something very strange happened. Splitext should split the name of the conflicting file by the "
                      ". to extract the file extension. This did not work though: " + extension)
                exit(-2)
            extension = extension[-1]  # get last entry (=the extension)

            # extract base name from filename info:
            name_parts = conflict_file_name.split(".sync-conflict")
            if len(name_parts) < 2:
                print("Something very strange happened. The filename of the file containing .sync-conflict could not be"
                      " split by that term.")
                exit(-2)
            base_name = name_parts[0]

            # build hashes of original file and conflict file:
            original_name = base_name + extension
            conflict_crc = crc(os.path.join(directory, conflict_file_name))
            original_crc = crc(os.path.join(directory, original_name))

            if original_crc == conflict_crc:
                os.unlink(os.path.join(directory, conflict_file_name))
                print("Deleted " + conflict_file_name + " as it has the same CRC as the original file.")
            else:
                print("Warning: There are real differences between " + original_name +  " and the conflicting file in "
                      + directory)
    else:
        print("Directory " + base_path + " does not exist. Aborting.")
        exit(-1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python3 SyncMessCleaner.py /path/to/base/directory")

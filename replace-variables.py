"""
To use:
python replace-variables.py example.txt key1=value1 key2=value2 key3=value3
"""

import sys
import re


def replace_in_file(file_name, **kwargs):
    """
    Replace occurrences of keys in the file with their corresponding values.

    :param file_name: name of the file to be modified
    :param kwargs: key-value pairs of the search-replace operations
    """
    with open(file_name, 'r') as f:
        filedata = f.read()
    for key, value in kwargs.items():
        filedata = re.sub(key, value, filedata)
    with open(file_name, 'w') as f:
        f.write(filedata)


def main():
    """
    Main function to execute the script.
    """
    # Check if the file name is provided
    if len(sys.argv) < 2:
        print("Please provide the file name as the first argument.")
        return
    file_name = sys.argv[1]

    # Collect key-value pairs from command line arguments
    kwargs = {}
    for i in range(2, len(sys.argv)):
        key, value = sys.argv[i].split("=")
        kwargs['#{' + key + '}#'] = value
    replace_in_file(file_name, **kwargs)


if __name__ == '__main__':
    main()

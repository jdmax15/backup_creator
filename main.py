#! python3
# backup_creator - Periodically backs up a folder into a zip before sending it to my raspberry Pi for storage.

import os
from functions import create_zip

# TODO: Get connection to Pi verified.

# TODO: Send .zip to the Pi for storage.


def main():
    os.chdir('C:\\Backups')
    create_zip('C:\\Users\\Joelm\\PYTHON_LEARNING')

if __name__ == '__main__':
    main()
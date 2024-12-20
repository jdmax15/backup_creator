#! python3
# backup_creator - Periodically backs up a folder into a zip before sending it to my raspberry Pi for storage.

import os
from functions import create_zip, ping_test, send_to_pi

BACKUP_FROM = ['C:\\Users\\Joelm\\PYTHON_LEARNING', 'C:\\Users\\Joelm\\JAVA_LEARNING']
BACKUP_TO = 'C:\\Backups'
REMOTE_PATH = '/home/jdmax15/Desktop/Backups'
REMOTE_IP = '192.168.1.7'

def main():
    # Change current working path to directory where .zip will be made before being sent.
    os.chdir(BACKUP_TO)

    for file_path in BACKUP_FROM:
        # Creates the .zip at the specified location.
        zip_name = create_zip(file_path)
        zip_path = os.path.join(BACKUP_TO, zip_name)
        
        # Adds the new .zip name to the remote absolute filepath.
        if "PYTHON" in zip_name:    
            remote_path = f"/home/jdmax15/Desktop/Backups/PYTHON/{zip_name}"
        elif "JAVA" in zip_name:
            remote_path = f"/home/jdmax15/Desktop/Backups/JAVA/{zip_name}"

        # TODO: Check if the size of the last backup on the Pi is same as the latest and skip sending if it is.

        # Pings the remote ip and checks for connection before attempting to send .zip.
        try:
            if ping_test(REMOTE_IP):
                send_to_pi(zip_path, remote_path, REMOTE_IP)
            else:
                print('Could not reach destination IP.')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
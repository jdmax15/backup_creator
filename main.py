#! python3
# backup_creator - Periodically backs up a folder into a zip before sending it to my raspberry Pi for storage.

import os
import logging
from functions import create_zip, ping_test, send_to_pi

BACKUP_FROM = ['C:\\Users\\Joelm\\JAVA_LEARNING', 'C:\\Users\\Joelm\\PYTHON_LEARNING', 'C:\\SCRIPTS']
BACKUP_TO = 'C:\\Backups'
REMOTE_PATH = '/home/jdmax15/Desktop/Backups'
REMOTE_IP = '192.168.1.50'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Change current working path to directory where .zip will be made before being sent.
    os.chdir(BACKUP_TO)

    for file_path in BACKUP_FROM:
        # Creates the .zip at the specified location.
        zip_name, zip_size, zip_type = create_zip(file_path)
        zip_path = os.path.join(BACKUP_TO, zip_name)
        
        # Adds the new .zip name to the remote absolute filepath.
        if "PYTHON" in zip_name:    
            remote_path = f"/home/jdmax15/Desktop/Backups/PYTHON/{zip_name}"
        elif "JAVA" in zip_name:
            remote_path = f"/home/jdmax15/Desktop/Backups/JAVA/{zip_name}"
        elif "SCRIPTS" in zip_name:
            remote_path = f"/home/jdmax15/Desktop/Backups/SCRIPTS/{zip_name}"

        # Check if the size of the last backup on the Pi is same as the latest and skip sending if it is.
        with open(f"{zip_type}_zip_size.txt", "r") as file:
            lines = file.readlines()
            if lines[-1] == str(zip_size):
                logging.info(f"{zip_name} has not had any changes since last backup. Skipping {zip_name}...")
                os.remove(zip_name)
                continue
            else:
                try:
                    # Pings the remote ip and checks for connection before attempting to send .zip.
                    if ping_test(REMOTE_IP):
                        send_to_pi(zip_path, remote_path, REMOTE_IP)
                        logging.info(f"{zip_name} successfully backed up and sent to {REMOTE_IP}.")
                    else:
                        logging.error('Could not reach destination IP.')
                        logging.info(f"{zip_name} was backed up but failed to sent to {REMOTE_IP}.")
                except Exception as e:
                    logging.error(e)

                # Write the size of the .zip to a text file for comparison on the next backup.
                with open(f"{zip_type}_zip_size.txt", "a") as file:
                    logging.info(f"{zip_name} size = {zip_size}. Writing size to {zip_type}_zip_size.txt")
                    file.write(str(f"\n{zip_size}"))

    logging.info('\n\nAll backups complete.')       


if __name__ == '__main__':
    main()
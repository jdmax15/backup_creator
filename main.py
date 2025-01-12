#! python3
# backup_creator - Periodically backs up a folder into a zip before sending it to my raspberry Pi for storage.

# TODO: Turn REMOTE_IP and REMOTE_PATH into a dictionary for multiple remote locations for backups. 
# Add functionality for files to also be stored on the Zero 2 W Samba Shared folder. (192.168.1.242/Shared/Backups)

import os
import logging
from functions import create_zip, ping_test, send_to_pi

BACKUP_FROM = ['C:\\Users\\Joelm\\JAVA_LEARNING', 'C:\\Users\\Joelm\\PYTHON_LEARNING', 'C:\\SCRIPTS']
BACKUP_TO = 'C:\\Backups'
REMOTE_PATH = {'192.168.1.50': '/home/jdmax15/Documents/Backups', 
               '192.168.1.242': '192.168.1.242/Shared/Backups'}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Change current working path to directory where .zip will be made before being sent.
    os.chdir(BACKUP_TO)


    # TODO: REFER TO THE REMOTE_PATH DICTIONARY FOR THE REMOTE PATHS.

    for file_path in BACKUP_FROM:
        # Creates the .zip at the specified location.
        zip_name, zip_size, zip_type = create_zip(file_path)
        zip_path = os.path.join(BACKUP_TO, zip_name)
            
        for remote_ip, remote_base_path in REMOTE_PATH.items():

            # Adds the new .zip name to the remote absolute filepath.
                if "PYTHON" in zip_name:    
                    remote_path_pi5 = f"{REMOTE_PATH['192.168.1.50']}/PYTHON/{zip_name}"
                    remote_path_piZ2 = f"{REMOTE_PATH['192.168.1.242']}/PYTHON/{zip_name}"
                elif "JAVA" in zip_name:
                    remote_path_pi5 = f"{REMOTE_PATH['192.168.1.50']}/JAVA/{zip_name}"
                    remote_path_piZ2 = f"{REMOTE_PATH['192.168.1.242']}/JAVA/{zip_name}"
                elif "SCRIPTS" in zip_name:
                    remote_path_pi5 = f"{REMOTE_PATH['192.168.1.50']}/SCRIPTS/{zip_name}"
                    remote_path_piZ2 = f"{REMOTE_PATH['192.168.1.242']}/SCRIPTS/{zip_name}"
                else:
                    logging.error('Could not determine the type of folder being backed up.')
                    continue

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
                                send_to_pi(zip_path, remote_path_pi5, REMOTE_IP)
                                logging.info(f"{zip_name} successfully backed up and sent to {REMOTE_IP}.")
                            else:
                                logging.error('Could not reach destination IP.')
                                logging.info(f"{zip_name} was backed up locally but failed to send to {REMOTE_IP}.")
                        except Exception as e:
                            logging.error(e)

                        # Write the size of the .zip to a text file for comparison on the next backup.
                        with open(f"{zip_type}_zip_size.txt", "a") as file:
                            logging.info(f"{zip_name} size = {zip_size}. Writing size to {zip_type}_zip_size.txt")
                            file.write(str(f"\n{zip_size}"))

    logging.info('\n\nAll backups complete.')       


if __name__ == '__main__':
    main()
import zipfile, os, datetime, time, paramiko, subprocess, re

BACKUP_TYPES = {
    "JAVA": "JAVA_Code_Backup",
    "PYTHON": "PYTHON_Code_Backup",
    "MyScripts": "SCRIPTS_Backup"
}


def create_zip(folder):

    folder = os.path.abspath(folder)

    current_date = datetime.datetime.fromtimestamp(time.time()).strftime('%d_%b_%Y')

    print(current_date)

    zip_file_name = None
    zip_type = None

    for key, value in BACKUP_TYPES.items():
        if key in folder:
            zip_file_name = f'{current_date}_{value}.zip'
            zip_type = key
            break

    if zip_file_name is None or zip_type is None:
        raise ValueError("Folder type not recognized")

    print(f'Creating {zip_file_name}...')
    backup_zip = zipfile.ZipFile(zip_file_name, 'w')    

    # Walk through folder, adding all files to the zip.
    for foldername, _, filenames in os.walk(folder):
        print(f'Adding files in {foldername}...')
        backup_zip.write(foldername)

        for filename in filenames:
            new_base = os.path.basename(folder) + '_'
            if filename.startswith(new_base) and filename.endswith('.zip'):
                continue
            backup_zip.write(os.path.join(foldername, filename))

    zip_size = os.path.getsize(zip_file_name)
    backup_zip.close()

    print('Done.')
    return str(zip_file_name), zip_size, zip_type

# Returns a boolean reponse if Pi remote IP Address can be reached.
def ping_test(ip_address):
    output = subprocess.Popen(["ping.exe", ip_address], stdout=subprocess.PIPE).communicate()[0]
    output = output.decode()  # Decode bytes to string for regex processing.

    # Pattern for a successful response specifically from the target IP.
    success_regex = re.compile(rf"Reply from {ip_address}")
    unreachable_regex = re.compile(rf"Reply from .*: Destination host unreachable")
    timeout_regex = re.compile(rf"{ip_address}: Request timed out")

    # Check specifically for success or failure related to the exact IP
    if success_regex.search(output):
        print(f"{ip_address} - Successful PING")
        return True
    elif unreachable_regex.search(output) or timeout_regex.search(output):
        print(f"{ip_address} - Failed PING")
        return False
    
    # If neither a success nor a failure pattern is matched, handle as failure.
    print(f"{ip_address} - Failed PING (Unrecognized response)")
    return False



# Uses paramiko module to establish an ssh connection and send the .zip file to the Pi.
def send_to_pi(localpath, remotepath, pi_ip):
    username = 'jdmax15'
    password = '1962'

    ssh = None
    sftp = None

    try:        
        print(f"ATTEMPTING TO CONNECT to {pi_ip} with username {username}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=pi_ip, username=username, password=password)
        sftp = ssh.open_sftp()
        print(f"CONNECTED.\nUploading {localpath} to {remotepath}...")
        sftp.put(localpath, remotepath)
        print(f'SUCCESS: File {localpath} successfully sent to {remotepath}')

    except paramiko.SSHException as e:
        print(f"SSH error occurred: {e}")
    except paramiko.AuthenticationException as e:
        print(f"Authentication failed: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
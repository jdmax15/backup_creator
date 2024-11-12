import zipfile, os, datetime, time
 
def create_zip(folder):
    folder = os.path.abspath(folder)
    # Declare folder/zip name. Will increment each time. Use shelve module to keep track?
    current_date = datetime.datetime.fromtimestamp(time.time()).strftime('%d_%b_%Y')
    print(current_date)
    zip_file_name = f'{current_date}_Code_Backup.zip'
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
    backup_zip.close()

    print('Done.')

def send_to_pi():
    return None
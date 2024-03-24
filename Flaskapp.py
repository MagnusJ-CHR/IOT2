from azure.storage.blob import BlobServiceClient
import os,time,shutil,datetime,subprocess


storage_account_key = 'wrDJZyn6evl+1g6NGU9+rjZnHMehP3PK2uzwD5dLiI9WKUn+zBaHTCrgpAN3MfKqaU9zKW3cPw2J+AStveQ+jg=='
storage_account_name = 'iot2storageblobs'
connection_string = 'DefaultEndpointsProtocol=https;AccountName=iot2storageblobs;AccountKey=wrDJZyn6evl+1g6NGU9+rjZnHMe>container_name = 'iotdata2'
account_url = 'https://iot2storageblobs.blob.core.windows.net/iotdata2'

def get_db_connection():
    conn = sqlite3.connect('/home/magnusjacobsen/Flaskapp/Database/SensorData.db')
    conn.row_factory = sqlite3.Row
    return conn



def time_now():
        now = time.localtime()
        current_time = (" {}-{}-{}".format(now[0], now[1], now[2]))
        return current_time

def ifdownloadedSince():
        now = time.localtime()
        downloaded = (" {}-{}-{}-{}-{}-{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
        return downloaded


def uploadToBlobStorage(file_path,file_name):
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        with open(file_path,"rb") as data:
                blob_client.upload_blob(data, overwrite=True)
        print(f"Uploaded / Replaced {file_name}.")

def download_blob_to_file():
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob="SensorData.db")
        with open(file=os.path.join(r'/home/magnusjacobsen/Flaskapp/Database', 'SensorData.db'), mode="wb") as sample_b>                
		download_stream = blob_client.download_blob()
                sample_blob.write(download_stream.readall())
                lastdownload = ifdownloadedSince()
                print("Database downloaded!")
                return lastdownload

def is_blob_modified_last():
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container='iotdata2', blob="SensorData.db")
        blob_properties = blob_client.get_blob_properties()
        prevProperties = str(blob_properties['last_modified'])
        return prevProperties

def is_blob_modified():
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container='iotdata2', blob="SensorData.db")
        global prevDownload
        global flaskwebsite
        blob_properties = blob_client.get_blob_properties()
        local_file_path = "/home/magnusjacobsen/Flaskapp/Database/SensorData.db"
        local_file_mtime = str(os.path.getmtime(local_file_path))
        blob_creation_time = str(blob_properties['last_modified'])
        if prevDownload != blob_creation_time:
                print("New data! Downloading.")
                prevDownload = blob_creation_time
                download_path = "/home/magnusjacobsen/Flaskapp/Database/SensorData.db"
                with open(download_path, "wb") as f:
                        filepathtoBackup()
                        download_blob_to_file()
                        time.sleep(10)
                        uploadToBlobStorage(Backuppath, BackupFile)
                        blob_data = blob_client.download_blob()
                        f.write(blob_data.readall())
                        print("Downloaded database,backup completed of old database and attempting restart.")
                        try:
                                flaskwebsite.terminate()
                                print("Old Flask app killed!")
                                flaskwebsite = subprocess.Popen(["nohup", "python", "app.py", "&"])
                                print("New Flask app started!" + time_now())
                        except subprocess.CalledProcessError as e:
                                print(f"Error: {e} , could not attempt restart.")




def filepathtoBackup():
        original_file = "SensorData.db"
        new_file = f"{original_file[:-3]}{time_now()}.db"
        source_path = "/home/magnusjacobsen/Flaskapp/Database/SensorData.db"
        destination_path = "/home/magnusjacobsen/Flaskapp/Database/Backup/" + new_file
        shutil.copy(source_path, destination_path)
        print('Data backed up on:' + time_now())


Backuppath = ('/home/magnusjacobsen/Flaskapp/Database/Backup/SensorData' + time_now() + '.db')
BackupFile = ('SensorData' + time_now() + '.db')
prevDownload = is_blob_modified_last()
flaskwebsite = subprocess.Popen(["nohup", "python", "app.py", "&"])
filepathtoBackup()
uploadToBlobStorage(Backuppath, BackupFile)
is_blob_modified()
print("Started Flask application, current data backed up to /Database/Backup, and checked for new data!")
try:
        while True:
                is_blob_modified()
                time.sleep(5)
except KeyboardInterrupt:
        flaskwebsite.terminate()
        print("Shutting down Flask website")
        time.sleep(1)



import serial,time,sqlite3
from CopyAndMove import filepathtoBackup,filepathtoUpload,time_now,time_now_timestamp
from azure.storage.blob import BlobServiceClient

filepathtoBackup()
filepathtoUpload()

global timestamp
backup_data = ('SensorData' + time_now() + '.db')
old_is_bytes = ""
to_bytes = "2024-3-20-17H-5M-43S#0#0#1#23#30#1
is_bytes = to_bytes.split('#')

storage_account_key = 'PRIVAT!'"
storage_account_name = 'Storage blob at Azure' 
connection_string = 'PRIVAT!'
container_name = 'iotdata2'
account_url = 'https://iot2storageblobs.blob.core.windows.net/iotdata2'

serialPort = serial.Serial(
	port="/dev/ttyAMA0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serial_string = ""

def upload_to_blob_storage(file_path,file_name):
	blob_service_client = BlobServiceClient.from_connection_string(connection_string)
	blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

	with open(file_path,"rb") as data:
		blob_client.upload_data(data, overwrite=True)
		print(f"Uploaded / Replaced {file_name}.")

def upload_to_blob_storage_backup(file_path,file_name):
	blob_service_client = BlobServiceClient.from_connection_string(connection_string)
	blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

	with open(file_path,"rb") as data:
		blob_client.upload_data(data, overwrite=True)
		print(f"Uploaded / Replaced {file_name}.")

def insert_into_db():
	try:
		conn = sqlite3.connect(database='Filepath til Database')
		cur = conn.cursor()
		query = 'INSERT INTO SensorData (Timestamp,Battery,Motion,Flamme,Temperatur,Fugtighed)VALUES(?,?,?,?,?,?)'
		data = (is_bytes[0], is_bytes[1],is_bytes[2],is_bytes[3],is_bytes[4],is_bytes[5])
		cur.execute(query, data)
		rowid = cur.lastrowid
		print(f'ID of last row insert = {rowid}')
		conn.commit()
		conn.close
		upload_to_blob_storage('Filepath', 'Filename')
		upload_to_storage_backup('Directory' + 'SensorData' + time_now()+'.db', backup_data)
	except sqlite3.OperationalError as oe:
		print(f'Op Error : { oe }')
	except IndexError:
		pass
		except sqlite3.IntegrityError as ie:
		pass
	except sqlite3.ProgrammingError as pe:
		print(f'Op Error : { pe }')

print("Ready to receive!")
while True:
	while True:
		try:
			serial_string = serialPort.readlione().strip()
			to_bytes = serialString.decode("Ascii")
			is_bytes = to_bytes.split('#')
		except UnicodeDecodeError:
			pass
		except serial.SerialException:
			pass
		try:
			if is_bytes != "2024-3-20-17H-5M-43S#0#0#1#23#30#1" and is_bytes[0] != "":
				is_bytes[0] = time_now_timestamp()
				insert_into_db()
				time.sleep(0.2)
		except IndexError:
			pass

		
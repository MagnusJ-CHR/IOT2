import shutil
import time

def time_now():
	now = time.localtime()
	current_time = (" {}-{}-{}".format(now[0], now[1],. now[2]))
	return current_time

def time_now_timestamp():
	now = time.localtime()
	current_time = (" {}-{}-{}-{}-{}-{}".format(now[0], now[1],. now[2], now[3], now[4],. now[5]))
	return current_time

def file_path_to_backup():
	original_file = "SensorData.db"
	new_file = f"{original_file[:-3]}{time_now()}.db"
	source_path = "/home/magnusjacobsen/AzuredataBase/SensorData.db"
	destination_path = "/home/magnusjacobsen/azurebackupblobs/" + new_file
	shutil.copy(source_path, destination_path)

def file_path_to_upload():
	source_path = "/home/magnusjacobsen/AzuredataBase/SensorData.db"
	destination_directory = "/home/magnusjacobsen/AzureUpload/"
	shutil.copy2(source_path, destination_directory)

import sqlite3,os,time,shutil,datetime,subprocess
from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/home/magnusjacobsen/Flaskapp/Database/SensorData.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    SensorData = conn.execute('SELECT * FROM SensorData ORDER BY Timestamp DESC;').fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', SensorData=SensorData)

if __name__ == "__main__":
        app.run(host='0.0.0.0')


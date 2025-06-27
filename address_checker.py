import os
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

DB_PATH = 'address_checks.db'
ADDRESSES = [
    '1600 Amphitheatre Parkway, Mountain View, CA',
    '1 Infinite Loop, Cupertino, CA',
    'Invalid Address Example',
]

def create_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS address_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_address TEXT NOT NULL,
            status TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            response_json TEXT,
            checked_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()

def check_address(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': GOOGLE_MAPS_API_KEY}
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        if data['status'] == 'OK':
            loc = data['results'][0]['geometry']['location']
            return 'OK', loc['lat'], loc['lng'], data
        else:
            return data['status'], None, None, data
    except Exception as e:
        return 'ERROR', None, None, {'error': str(e)}

def main():
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    for address in ADDRESSES:
        status, lat, lng, resp_json = check_address(address)
        conn.execute(
            'INSERT INTO address_checks (input_address, status, latitude, longitude, response_json, checked_at) VALUES (?, ?, ?, ?, ?, ?)',
            (address, status, lat, lng, str(resp_json), datetime.now())
        )
        print(f"Checked: {address} | Status: {status} | Lat: {lat} | Lng: {lng}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main() 
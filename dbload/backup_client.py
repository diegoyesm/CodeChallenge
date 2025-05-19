# dbchallenge/dbload/backup_client.py
import requests
import json
import os
import sys


def backup_tables():
    """
    Client to backup all tables in AVRO format
    """
    url = 'http://localhost:8000/api/backup/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Backup completed successfully!")
            print("Backup files:")
            for table, file_path in data['files'].items():
                print(f"- {table}: {file_path}")
            print("\nTo restore from a backup, use the restore_client.py script.")
            return data['files']
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


if __name__ == '__main__':
    backup_tables()
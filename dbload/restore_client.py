import requests
import json
import os
import sys


def list_backups():
    """
    Client to list available backups for all tables
    """
    url = 'http://localhost:8000/api/list-backups/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Available backups:")
            
            for table, backups in data['backups'].items():
                print(f"\n{table.capitalize()} backups:")
                if backups:
                    for i, backup in enumerate(backups, 1):
                        # Extract just the filename for cleaner display
                        filename = os.path.basename(backup)
                        print(f"  {i}. {filename}")
                else:
                    print("  No backups available")
            
            return data['backups']
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def restore_table(table_name, backup_file):
    """
    Client to restore a specific table from a backup file
    """
    url = 'http://localhost:8000/api/restore-table/'
    
    # If the user only provided a number, we need to get the full backup path
    if backup_file.isdigit():
        backups = list_backups()
        if not backups:
            return None
        
        backup_index = int(backup_file) - 1
        if table_name in backups and 0 <= backup_index < len(backups[table_name]):
            backup_file = backups[table_name][backup_index]
        else:
            print(f"Invalid backup index for table {table_name}")
            return None
    
    data = {
        'table_name': table_name,
        'backup_file': backup_file
    }
    
    try:
        response = requests.post(
            url,
            headers={'Content-type': 'application/json'},
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Restore completed successfully!")
            print(f"Restored {result['records_restored']} records to {result['table']} table")
            return result
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def interactive_restore():
    """
    Interactive client for restoring tables
    """
    print("Database Table Restore Utility")
    print("==============================")
    
    # List available backups
    backups = list_backups()
    if not backups:
        print("No backups available or error connecting to the server")
        return
    
    # Ask which table to restore
    print("\nWhich table would you like to restore?")
    print("1. Department")
    print("2. Job") 
    print("3. Hired Employee")
    
    table_choice = input("Enter your choice (1-3): ")
    
    table_mapping = {
        '1': 'department',
        '2': 'job',
        '3': 'hired_employee'
    }
    
    if table_choice not in table_mapping:
        print("Invalid choice")
        return
    
    table_name = table_mapping[table_choice]
    
    # Check if there are backups for this table
    if not backups[table_name]:
        print(f"No backups available for {table_name}")
        return
    
    # Ask which backup to use
    print(f"\nWhich {table_name} backup would you like to restore?")
    backup_index = input(f"Enter backup number (1-{len(backups[table_name])}): ")
    
    if not backup_index.isdigit() or int(backup_index) < 1 or int(backup_index) > len(backups[table_name]):
        print("Invalid backup number")
        return
    
    backup_file = backups[table_name][int(backup_index) - 1]
    
    # Confirm restore
    print(f"\nYou are about to restore the {table_name} table from backup:")
    print(f"  {os.path.basename(backup_file)}")
    print("\nWARNING: This will replace all existing data in the table!")
    
    confirm = input("Do you want to proceed? (y/n): ")
    if confirm.lower() != 'y':
        print("Restore cancelled")
        return
    
    # Perform the restore
    restore_table(table_name, backup_file)


if __name__ == '__main__':
    # If arguments are provided, use them directly
    if len(sys.argv) > 1:
        if sys.argv[1] == 'list':
            list_backups()
        elif len(sys.argv) == 3:
            table_name = sys.argv[1]
            backup_file = sys.argv[2]
            restore_table(table_name, backup_file)
        else:
            print("Usage:")
            print("  python restore_client.py list")
            print("  python restore_client.py <table_name> <backup_file_or_index>")
            print("  python restore_client.py  # for interactive mode")
    else:
        # Run in interactive mode
        interactive_restore()
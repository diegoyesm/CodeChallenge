# dbchallenge/dbdata/backup.py

import os
import json
import avro.schema
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader
from django.conf import settings
from datetime import datetime
from .models import Department, Job, HiredEmployee

from django.utils.dateparse import parse_datetime
from django.db import transaction



def ensure_backup_dir():
    """Ensure the backup directory exists"""
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return backup_dir


def get_timestamp():
    """Get a timestamp string for filenames"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def backup_department_table():
    """Backup Department table to AVRO format"""
    backup_dir = ensure_backup_dir()
    timestamp = get_timestamp()
    filename = os.path.join(backup_dir, f'department_backup_{timestamp}.avro')
    
    # Define the Avro schema based on the Department model
    schema_json = {
        "namespace": "dbdata",
        "type": "record",
        "name": "Department",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "department", "type": "string"}
        ]
    }
    
    schema = avro.schema.parse(json.dumps(schema_json))
    
    # Create a writer
    with open(filename, 'wb') as f:
        writer = DataFileWriter(f, DatumWriter(), schema)
        
        # Add each Department record to the AVRO file
        for dept in Department.objects.all():
            writer.append({
                "id": dept.id,
                "department": dept.department
            })
        
        writer.close()
    
    return filename


def backup_job_table():
    """Backup Job table to AVRO format"""
    backup_dir = ensure_backup_dir()
    timestamp = get_timestamp()
    filename = os.path.join(backup_dir, f'job_backup_{timestamp}.avro')
    
    # Define the Avro schema based on the Job model
    schema_json = {
        "namespace": "dbdata",
        "type": "record",
        "name": "Job",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "job", "type": "string"}
        ]
    }
    
    schema = avro.schema.parse(json.dumps(schema_json))
    
    # Create a writer
    with open(filename, 'wb') as f:
        writer = DataFileWriter(f, DatumWriter(), schema)
        
        # Add each Job record to the AVRO file
        for job in Job.objects.all():
            writer.append({
                "id": job.id,
                "job": job.job
            })
        
        writer.close()
    
    return filename


def backup_hired_employee_table():
    """Backup HiredEmployee table to AVRO format"""
    backup_dir = ensure_backup_dir()
    timestamp = get_timestamp()
    filename = os.path.join(backup_dir, f'hired_employee_backup_{timestamp}.avro')
    
    # Define the Avro schema based on the HiredEmployee model
    schema_json = {
        "namespace": "dbdata",
        "type": "record",
        "name": "HiredEmployee",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": ["string", "null"]},
            {"name": "datetime", "type": ["string", "null"]},
            {"name": "department_id", "type": "int"},
            {"name": "job_id", "type": "int"}
        ]
    }
    
    schema = avro.schema.parse(json.dumps(schema_json))
    
    # Create a writer
    with open(filename, 'wb') as f:
        writer = DataFileWriter(f, DatumWriter(), schema)
        
        # Add each HiredEmployee record to the AVRO file
        for employee in HiredEmployee.objects.all():
            writer.append({
                "id": employee.id,
                "name": employee.name if employee.name else None,
                "datetime": employee.datetime.isoformat() if employee.datetime else None,
                "department_id": employee.department_id.id,
                "job_id": employee.job_id.id
            })
        
        writer.close()
    
    return filename


def backup_all_tables():
    """Backup all tables to AVRO format"""
    dept_file = backup_department_table()
    job_file = backup_job_table()
    emp_file = backup_hired_employee_table()
    
    return {
        "department": dept_file,
        "job": job_file,
        "hired_employee": emp_file
    }


def list_backups():
    """List all available backup files"""
    backup_dir = ensure_backup_dir()
    backups = {
        "department": [],
        "job": [],
        "hired_employee": []
    }
    
    if os.path.exists(backup_dir):
        for filename in os.listdir(backup_dir):
            if filename.startswith('department_backup_') and filename.endswith('.avro'):
                backups["department"].append(os.path.join(backup_dir, filename))
            elif filename.startswith('job_backup_') and filename.endswith('.avro'):
                backups["job"].append(os.path.join(backup_dir, filename))
            elif filename.startswith('hired_employee_backup_') and filename.endswith('.avro'):
                backups["hired_employee"].append(os.path.join(backup_dir, filename))
    
    # Sort by filename (which includes timestamp) to get latest first
    for table in backups:
        backups[table] = sorted(backups[table], reverse=True)
    
    return backups


@transaction.atomic
def restore_department_table(backup_file):
    """Restore Department table from AVRO backup"""
    # First check if the file exists
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
    
    # Clear existing records
    Department.objects.all().delete()
    
    # Read from AVRO file and create new records
    with open(backup_file, 'rb') as f:
        reader = DataFileReader(f, DatumReader())
        for record in reader:
            Department.objects.create(
                id=record['id'],
                department=record['department']
            )
        reader.close()
    
    return Department.objects.count()


@transaction.atomic
def restore_job_table(backup_file):
    """Restore Job table from AVRO backup"""
    # First check if the file exists
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
    
    # Clear existing records
    Job.objects.all().delete()
    
    # Read from AVRO file and create new records
    with open(backup_file, 'rb') as f:
        reader = DataFileReader(f, DatumReader())
        for record in reader:
            Job.objects.create(
                id=record['id'],
                job=record['job']
            )
        reader.close()
    
    return Job.objects.count()


@transaction.atomic
def restore_hired_employee_table(backup_file):
    """Restore HiredEmployee table from AVRO backup"""
    # First check if the file exists
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
    
    # Clear existing records
    HiredEmployee.objects.all().delete()
    
    # Read from AVRO file and create new records
    with open(backup_file, 'rb') as f:
        reader = DataFileReader(f, DatumReader())
        for record in reader:
            # Get related objects
            department = Department.objects.get(id=record['department_id'])
            job = Job.objects.get(id=record['job_id'])
            
            # Parse datetime if it exists
            datetime_val = None
            if record['datetime']:
                datetime_val = parse_datetime(record['datetime'])
            
            HiredEmployee.objects.create(
                id=record['id'],
                name=record['name'],
                datetime=datetime_val,
                department_id=department,
                job_id=job
            )
        reader.close()
    
    return HiredEmployee.objects.count()


def restore_table(table_name, backup_file):
    """Restore a specific table from an AVRO backup file"""
    if table_name == 'department':
        return restore_department_table(backup_file)
    elif table_name == 'job':
        return restore_job_table(backup_file)
    elif table_name == 'hired_employee':
        return restore_hired_employee_table(backup_file)
    else:
        raise ValueError(f"Unknown table name: {table_name}")
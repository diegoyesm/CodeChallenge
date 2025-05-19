import json
import requests
from csv import DictReader


def load_bulk_hired_employees():
    url = 'http://localhost:8000/api/hired-employee-bulk-list-serializer/'

    data = []
    error_data = []
    with open('../historic_data/hired_employees.csv') as f:
        cf = DictReader(f, fieldnames=['id', 'name', 'datetime', 'department_id', 'job_id'])
        for row in cf:
            if row['id'] and row['name'] and row['datetime'] and row['department_id'] and row['job_id']:
                data.append(
                    {
                        "id": row['id'],
                        "name": row['name'],
                        "datetime": row['datetime'],
                        "department_id": row['department_id'],
                        "job_id": row['job_id']
                    }
                )
            else:
                error_data.append(
                    {
                        "id": row['id'],
                        "name": row['name'],
                        "datetime": row['datetime'],
                        "department_id": row['department_id'],
                        "job_id": row['job_id']
                    }
                )

    response = requests.post(
        url,
        headers={'Content-type': 'application/json'},
        data=json.dumps(
            data
        )
    )

    print("Result")
    print(response.json())
    print("Data with error")
    print(error_data)


if __name__ == '__main__':
    load_bulk_hired_employees()


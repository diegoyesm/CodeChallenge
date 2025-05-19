import json
import requests
from csv import DictReader


def load_bulk_department():
    url = 'http://localhost:8000/api/departments-bulk-list-serializer/'

    data = []
    with open('../historic_data/departments.csv') as f:
        cf = DictReader(f, fieldnames=['id', 'department'])
        for row in cf:
            data.append(
                {
                    'id': row['id'],
                    'department': row['department']
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


if __name__ == '__main__':
    load_bulk_department()


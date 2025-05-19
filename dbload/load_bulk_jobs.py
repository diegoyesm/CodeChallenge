import json
import requests
from csv import DictReader


def load_bulk_job():
    url = 'http://localhost:8000/api/job-bulk-list-serializer/'

    data = []
    with open('../historic_data/jobs.csv') as f:
        cf = DictReader(f, fieldnames=['id', 'job'])
        for row in cf:
            data.append(
                {
                    'id': row['id'],
                    'job': row['job']
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
    load_bulk_job()


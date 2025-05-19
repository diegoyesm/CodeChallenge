import json

import pytest
from csv import DictReader

from dbdata.models import Department, Job
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_add_department(client):
    departments = Department.objects.all()
    assert len(departments) == 0

    test_url = reverse(
        "departments",
    )

    resp = client.post(
        test_url,
        {
            "id": 2,
            "department": "Marketing",
        },
        content_type="application/json"
    )
    assert resp.status_code == 201
    assert resp.data["department"] == "Marketing"

    departments = Department.objects.all()
    assert len(departments) == 1


class TestDepartment:
    @pytest.mark.django_db
    def test_create_task(self, client):
        test_url = reverse(
            "departments",
        )

        with open('./external_files/departments.csv') as f:
            cf = DictReader(f, fieldnames=['id', 'department'])
            for row in cf:
                print(row)
                response = client.post(
                    test_url,
                    data={
                        'id': row['id'],
                        'department': row['department']
                    }
                )
                assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_list_serializer(self, client):
        test_url = reverse(
            "departments-list-serializer",
        )

        data = []
        with open('./external_files/departments.csv') as f:
            cf = DictReader(f, fieldnames=['id', 'department'])
            for row in cf:
                data.append(
                    {
                        'id': row['id'],
                        'department': row['department']
                    }
                )

        response = client.post(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        print("Result")
        print(response.json())
        print(response.status_code)
        assert response.status_code == status.HTTP_201_CREATED

        assert len(response.json()) == len(data)

    @pytest.mark.django_db
    def test_bulk_create_list_serializer(self, client):
        test_url = reverse(
            "departments-bulk-list-serializer",
        )
        data = []
        with open('./external_files/departments.csv') as f:
            cf = DictReader(f, fieldnames=['id', 'department'])
            for row in cf:
                data.append(
                    {
                        'id': row['id'],
                        'department': row['department']
                    }
                )

        response = client.post(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        print("Result")
        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        assert len(response.json()) == len(data)


class TestHiredEmployees:
    @pytest.mark.django_db
    def test_bulk_create_list_serializer(self, client):
        test_url = reverse(
            "hired-employee-bulk-list-serializer",
        )
        data = []
        with open('./external_files/hired_employees.csv') as f:
            cf = DictReader(f, fieldnames=['id', 'name', 'datetime', 'department_id', 'job_id'])
            for row in cf:
                data.append(
                    {
                        'id': row['id'],
                        'name': row['name'],
                        'datetime': row['datetime'],
                        'department_id': row['department_id'],
                        'job_id': row['job_id']
                    }
                )

        response = client.post(
            test_url,
            data=json.dumps(
                data
            ),
            content_type="application/json",
        )

        print("Result")
        print(response.json())

        assert response.status_code == status.HTTP_201_CREATED

        assert len(response.json()) == len(data)

from datetime import datetime

import pytest

from dbdata.models import Department, Job, HiredEmployee


@pytest.mark.django_db
def test_department_model():
    department = Department(id=1, department="Accounting")
    department.save()
    assert department.id == 1
    assert department.department == "Accounting"

    assert str(department) == department.department


@pytest.mark.django_db
def test_job_model():
    job = Job(id=1, job="Accounting")
    job.save()
    assert job.id == 1
    assert job.job == "Accounting"

    assert str(job) == job.job


@pytest.mark.django_db
def test_hired_employee_model():

    department = Department(id=1, department="Accounting")
    department.save()

    job = Job(id=1, job="Accounting")
    job.save()

    hired_employee = HiredEmployee(
        id=1,
        name="Accounting",
        datetime=datetime.now(),
        department_id=department,
        job_id=job
    )
    hired_employee.save()
    assert hired_employee.id == 1
    assert hired_employee.name == "Accounting"
    assert hired_employee.datetime
    assert str(hired_employee.department_id) == str(department)
    assert str(hired_employee.job_id) == str(job)

    assert str(hired_employee) == hired_employee.name

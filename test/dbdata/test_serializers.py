from dbdata.serializers import DepartmentSerializer, JobSerializer


def test_valid_department_serializer(db):
    valid_serializer_data = {
        "id": 1,
        "department": "Accounting"
    }
    serializer = DepartmentSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_department_serializer(db):
    invalid_serializer_data = {
        "id": "1",
    }
    serializer = DepartmentSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"department": ["This field is required."]}


def test_valid_job_serializer(db):
    valid_serializer_data = {
        "id": 1,
        "job": "Accounting"
    }
    serializer = JobSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_job_serializer(db):
    invalid_serializer_data = {
        "id": "1",
    }
    serializer = JobSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"job": ["This field is required."]}

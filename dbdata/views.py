import requests
import pandas as pd
from csv import DictReader
from datetime import datetime
from json import loads, dumps
from django.urls import reverse
from django.db import connection
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from .serializers import (DepartmentSerializer, BulkDepartmentSerializer,
                          BulkJobSerializer, BulkHiredEmployeeSerializer,
                          HiredEmployeeSerializer)
from .models import Department, Job, HiredEmployee



# Create your views here.


class DepartmentList(APIView):
    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListSerializer(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(DepartmentListSerializer, self).get_serializer(*args, **kwargs)


class DepartmentBulkListCreateView(generics.ListCreateAPIView):
    """
    # List/Create/Update the relationships between Labels and CaptureSamples

    Required permissions: *Authenticated*, *CaptureLabelValue add*
    """

    serializer_class = BulkDepartmentSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(DepartmentBulkListCreateView, self).get_serializer(
            *args, **kwargs
        )


class JobBulkListCreateView(generics.ListCreateAPIView):
    """
    # List/Create/Update the relationships between Labels and CaptureSamples

    Required permissions: *Authenticated*, *CaptureLabelValue add*
    """

    serializer_class = BulkJobSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(JobBulkListCreateView, self).get_serializer(
            *args, **kwargs
        )


class HiredEmployeeBulkListCreateView(generics.ListCreateAPIView):
    """
    # List/Create/Update the relationships between Labels and CaptureSamples

    Required permissions: *Authenticated*, *CaptureLabelValue add*
    """

    serializer_class = BulkHiredEmployeeSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(HiredEmployeeBulkListCreateView, self).get_serializer(
            *args, **kwargs
        )

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            for item in request.data:
                job = Job.objects.filter(id=item["job_id"]).first()
                department = Department.objects.filter(id=item["department_id"]).first()

                if job and department:
                    item["job_id"] = job.id
                    item["department_id"] = department.id
                    item["datetime"] = datetime.fromisoformat(item["datetime"])
                else:
                    raise ValidationError("Foreign Key does not exist")
        else:
            raise ValidationError("Invalid Input")

        return super(HiredEmployeeBulkListCreateView, self).post(request, *args, **kwargs)


class EmployeesHiredQuarter(APIView):
    def get(self, request, format=None):
        sql = """
            SELECT 
                d.department
                , j.job
                , extract(quarter from h.datetime) as quarter
                , count(*) total
            FROM dbdata_hiredemployee h
            INNER JOIN dbdata_department d on h.department_id_id = d.id
            INNER JOIN dbdata_job j ON h.job_id_id = j.id
            WHERE extract(YEAR from h.datetime) = 2021
            GROUP BY 1,2,3
            ORDER BY 1,2
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            hired_employee = cursor.fetchall()

        df = pd.DataFrame(hired_employee, columns=['department', 'job', 'quarter', 'total'])
        df_rst = df.pivot_table('total', ['department', 'job'], 'quarter').reset_index()
        df_rst.fillna(0, inplace=True)

        print(df_rst)

        result = df_rst.to_json(orient="index")
        parsed = loads(result)
        df_dumps = dumps(parsed, indent=4)

        return HttpResponse(df_dumps, content_type='application/json')


class EmployeesHiredDepartment(APIView):
    def get(self, request, format=None):
        sql = """
            with totals as (
                SELECT 
                    d.id
                    , d.department
                    , count(h.id) total
                FROM dbdata_hiredemployee h
                INNER JOIN dbdata_department d on h.department_id_id = d.id
                GROUP BY 1,2
            ), totals_2021 as (
                SELECT 
                    extract(YEAR from h.datetime) hired_year
                    , d.id
                    , d.department
                    , count(h.id) total
                FROM dbdata_hiredemployee h
                INNER JOIN dbdata_department d on h.department_id_id = d.id
                WHERE extract(YEAR from h.datetime) = 2021
                GROUP BY 1,2,3
            ), average_year_2021 as (
                SELECT 
                    t.hired_year, 
                    avg(t.total) average_year_2021
                FROM totals_2021 t
                GROUP BY 1
            ), total_average as (
                SELECT
                    t.id
                    , t.department
                    , t.total
                    , ay.average_year_2021
                FROM totals t, average_year_2021 ay
            ), result as (
                SELECT
                    ta.id
                    , ta.department
                    , ta.total
                FROM total_average ta
                WHERE ta.total > ta.average_year_2021
                ORDER BY ta.total DESC
            )
            select *
            from result

        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            hired_employee = cursor.fetchall()

        df = pd.DataFrame(hired_employee, columns=['id', 'department', 'total'])

        result = df.to_json(orient="index")
        parsed = loads(result)
        df_dumps = dumps(parsed, indent=4)

        return HttpResponse(df_dumps, content_type='application/json')



def post_department_data(request):
    test_url = reverse(
        "departments",
    )
    print("URL")
    url = f"http://0.0.0.0:8000{test_url}"
    print(url)
    with open('./external_files/departments.csv') as f:
        cf = DictReader(f, fieldnames=['id', 'department'])
        for row in cf:
            print("Read File")
            print(row)
            response = requests.post(
                url,
                data={
                    'id': row['id'],
                    'department': row['department']
                }
            )
            print(response.json())
    return HttpResponse("Departments")

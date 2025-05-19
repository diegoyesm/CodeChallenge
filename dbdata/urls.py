from django.urls import path

from .views import (DepartmentList, DepartmentListSerializer, DepartmentBulkListCreateView,
                    JobBulkListCreateView, HiredEmployeeBulkListCreateView, EmployeesHiredQuarter,
                    EmployeesHiredDepartment, post_department_data)


urlpatterns = [
    path("api/departments/", DepartmentList.as_view(), name="departments"),
    path("api/departments-list-serializer/", DepartmentListSerializer.as_view(), name="departments-list-serializer"),
    path("api/departments-bulk-list-serializer/",
         DepartmentBulkListCreateView.as_view(),
         name="departments-bulk-list-serializer"),
    path("api/job-bulk-list-serializer/",
         JobBulkListCreateView.as_view(),
         name="job-bulk-list-serializer"),
    path("api/hired-employee-bulk-list-serializer/",
         HiredEmployeeBulkListCreateView.as_view(),
         name="hired-employee-bulk-list-serializer"),
    path("api/employees-hired-quarter/",
         EmployeesHiredQuarter.as_view(),
         name="employees-hired-quarter"),
    path("api/employees-hired-department/",
         EmployeesHiredDepartment.as_view(),
         name="employees-hired-department"),
    path('client/post-department-data/', post_department_data, name='post-department-data'),
]

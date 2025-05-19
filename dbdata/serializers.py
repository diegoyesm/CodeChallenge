
import time
from rest_framework import serializers
from .models import Department, Job, HiredEmployee
from .fields import ModelObjectIdField
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ()


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ()


class HiredEmployeeSerializer(serializers.Serializer):
    department = serializers.CharField(max_length=200)
    #job = serializers.CharField()
    #quarter = serializers.IntegerField()
    #total = serializers.IntegerField()


class DepartmentBulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result

    def to_representation(self, instances):
        start = time.time()
        rep_list = []
        for instance in instances:
            rep_list.append(
                dict(
                    id=instance.id,
                    department=instance.department,
                )
            )

        print("to_rep", time.time() - start)

        return rep_list


class BulkDepartmentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        instance = Department(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ()
        list_serializer_class = DepartmentBulkCreateListSerializer


class JobBulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result

    def to_representation(self, instances):
        start = time.time()
        rep_list = []
        for instance in instances:
            rep_list.append(
                dict(
                    id=instance.id,
                    job=instance.job,
                )
            )

        print("to_rep", time.time() - start)

        return rep_list


class BulkJobSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        instance = Job(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance
        
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ()
        list_serializer_class = JobBulkCreateListSerializer


class HiredEmployeeBulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result




class BulkHiredEmployeeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = HiredEmployee(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = HiredEmployee
        fields = '__all__'
        read_only_fields = ()
        list_serializer_class = HiredEmployeeBulkCreateListSerializer



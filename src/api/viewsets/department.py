import logging

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.models import Department
from api.serializers import DepartmentSerializer
from api import errors

logger = logging.getLogger(__name__)


class GetDepartments(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)


class GetSingleDepartment(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, department_id):
        try:
            department = Department.objects.get(department_id=department_id)
            serializer_element = DepartmentSerializer(instance=department)
            return Response(serializer_element.data)
        except Department.DoesNotExist:
            return errors.handle(errors.DEP_02)

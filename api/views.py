from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from registration.models import CustomUser
from accesskey.models import AccessKey
from .serializers import AccessKeySerializer

@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_access_key_details_with_email(request,email):
    try:
        user = CustomUser.objects.get(email=email)
        if user:
            key = get_object_or_404(AccessKey,user=user,status="active")
            serializer = AccessKeySerializer(key)
            return Response(serializer.data,status=HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
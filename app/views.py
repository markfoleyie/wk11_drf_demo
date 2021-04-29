from django.shortcuts import render

# Create your views here.

from . import models
from . import serializers
from . import permissions as my_permissions
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.schemas.openapi import AutoSchema


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Register(APIView):
    """
    Allows a new user to register an account.
    """

    def post(self, request):
        """
        Takes the following JSON structure as input:

        {"username": "string", "password": "string", "first_name": "string", "last_name": "string", "is_admin": "boolean"}            }

        """
        try:
            if not request.data:
                raise ValueError("Invalid User data")

            # serialized_data = serializers.RegisterSerializer(data=request.data)
            # if serialized_data.is_valid(raise_exception=True):
            incoming_data = {
                "username": request.data["username"],
                "password": request.data["password"],
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "email": f"{request.data['first_name']}.{request.data['last_name']}@tudublin.ie",
                "is_staff": request.data["is_admin"],
            }
            new_user = get_user_model().objects.create_user(**incoming_data)

            return Response({
                "username": request.data["username"],
                "first_name": request.data["first_name"],
                "last_name": request.data["last_name"],
                "is_admin": request.data["is_admin"],
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class UserMeDetails(generics.RetrieveAPIView):
    """"
    Retrieves a summarized view of the current User object.
    """
    serializer_class = serializers.UserMeSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return self.request.user

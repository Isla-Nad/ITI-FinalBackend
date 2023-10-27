from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from accounts.models import User


class UserRegistrationView(APIView):

    def get(self, request, format='json'):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

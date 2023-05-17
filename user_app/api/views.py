from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegistrationSerializer
from user_app.models import Token
# Need to include that code
from user_app import models


@api_view(["POST"])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data["username"] = account.username
            data["email"] = account.email
            data["token"] = Token.objects.get(user=account).key
            return Response(data)
        data["errors"] = serializer.errors
        return Response(data)
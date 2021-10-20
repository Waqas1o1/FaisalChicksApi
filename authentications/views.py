from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from authentications.serializer import UserSerializer, RegisterSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from django.http import HttpResponse
from utils.enums import Groups as g
from app import models as m
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
                        "token": AuthToken.objects.create(user)[1]
                })
    
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        temp_list=super(LoginAPI, self).post(request, format=None)
        temp_list.data['user'] = user.username

        if user.is_superuser:
            temp_list.data['group'] = 'superuser'
        else:
            temp_list.data['group'] = user.groups.all().first().name
            person = temp_list.data['group']
            if person == g.SalesOfficer.value:
                so = m.SalesOfficer.objects.get(user=user)
                temp_list.data['salesofficer'] = {'name':so.name,'id':so.id}
            if person == g.Dispatcher.value:
                temp_list.data['dispatcher'] = {'name':request.user.username,'id':user.id}
                
        return Response({"data":temp_list.data})
    
def CheckAuthenication(request):
    return HttpResponse(f'{request.user.groups.get()}')
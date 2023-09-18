from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, Variables
from .provider import sign_with_google

class VariablesView(APIView):


    def get(self, request, id=None):
        if id:
            variables = Variables.objects.filter(id=id)
            if variables.exists():
                variables = variables.get()
                if variables.password:
                    # get password
                    return Response({})
                return Response(data={"type":"success","variables": variables.variables})
            return Response(data={"type":"error", "message":"variables not found"})                
        if request.user.is_authenticated:
            variables = Variables.objects.filter(user_id=request.user.id)
            data = {
                "type":"success",
                "data":variables.values('variables', "password")    
            }
            return Response(data=data)
        return Response(data={"type":"error", "message":"please login"})

    def put(self, request, id):
        if not request.user.is_authenticated:
            return Response(data={"type":"error", "message":"please login"})
        variables = Variables.objects.filter(id=id, user_id=request.user.id)
        data = request.data
        if variables.exists():
            try:
                variables = variables.get()
                variables.variables = data['variables']
                variables.password = data['password']
                variables.save()
                return Response({"type":"success", "message":"variables updated succesfully"})
            except Exception as e:
                return Response({"type":"error", "message":e})
        return Response(data={"type":"error", "message":"variables not found"})                

    def delete(self, request, id):
        if request.user.is_authenticated:
            variables = Variables.objects.filter(user_id=request.user.id, id=id)
            if variables.exists():
                variables = variables.get()
                variables.delete()
                return Response({"type":"success", "message":"variables was deleted"})
            return Response(data={"type":"error", "message":"variables not found"})                
        return Response(data={"type":"error", "message":"please login"})

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(data={"type":"error", "message":"please login"})
        data = request.data
        try:
            variables = Variables.objects.create(
                variables = data['variables'],
                password = data['password']
            )
            variables.save()
            return Response({"type":"success", "message":"variables created succesfully"})
        except Exception as e:
            return Response({"type":"error", "message":e})


class SignUpWithProviderView(APIView):
    
    def post(self, request, provider):
        token = request.data.get("token")
        if not token:
            return Response({"type": "error", "message": "Couldn't find your email try again"})
        if provider == "google":
            user_token = sign_with_google(token)
            if not user_token:
                return Response({"type": "error", "message": "Couldn't find your email try again"})
            return Response({"type": "success", "data": user_token})
        return Response({"type": "error", "message": "Provider not found"})
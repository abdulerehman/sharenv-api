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
        return Response({})

    def delete(self, request, id):
        return Response({})

    def post(self, request):
        return Response({})


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
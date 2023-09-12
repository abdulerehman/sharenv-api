from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Permissions, User, Variables
from .provider import sign_with_google

class VariablesView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, id=None):
        return Response({})

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




class PermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        return Response({})

    def post(self, request):
        return Response({})

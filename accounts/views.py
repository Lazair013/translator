from functools import wraps

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import TranslationHistory, User
from .serializers import RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Заполните все поля'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь уже есть'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return Response({'username': user.username, 'id': user.id})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TranslateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_text = request.data.get('input_text')
        output_text = input_text[::-1] if input_text else ''
        TranslationHistory.objects.create(
            user=request.user,
            input_text=input_text,
            output_text=output_text
        )
        return Response({'output_text': output_text})


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = TranslationHistory.objects.filter(user=request.user).order_by('-created_at')
        data = [
            {
                "input_text": h.input_text,
                "output_text": h.output_text,
                "created_at": h.created_at,
            } for h in history
        ]
        return Response({"history": data})
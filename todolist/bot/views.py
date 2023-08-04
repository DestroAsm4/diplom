from rest_framework.views import APIView, Response
from rest_framework import permissions, status

from .models import TgUser
from .serializers import VerificationSerializer
from .tg.client import TgClient
from todolist.settings import BOT_TOKEN


class VerificationView(APIView):
    serializer_class = VerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data.get('verification_code')

            tg_user = TgUser.objects.filter(verification_code=verification_code).first()
            if tg_user:
                tg_user.user_id = request.user.id
                tg_user.save()

                response_data = {
                    'tg_id': tg_user.tg_id,
                    'username': tg_user.username,
                    'verification_code': tg_user.verification_code,
                    'user_id': tg_user.user_id,
                }

                client = TgClient(BOT_TOKEN)
                client.send_message(chat_id=tg_user.tg_id, text='You are successfully verified!')

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response('Telegram user not found', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

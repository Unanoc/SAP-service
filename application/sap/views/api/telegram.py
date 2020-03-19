import telebot
from rest_framework.views import APIView
from rest_framework.response import Response

from application.sap.models import (
    FeedbackSettings,
)
from application.sap.utils import send_to_telegram_channel


class BotSender(APIView):
    authentication_classes = []
    permission_classes = []

    def post (self, request, format=None):
        _hash = request.data["hash"]
        url = request.data["url"]
        
        fs = FeedbackSettings.objects.get_by_hash(hash=_hash)
        message = "Please, leave some feedback about passed class.\n\n{}/{}".format(
            fs.base_url, 
            fs.hash_url,
        )
        result = dict()
        
        try:
            send_to_telegram_channel(channel=fs.telegram_channel, message=message)
            result['message'] = "Done!"
        except telebot.apihelper.ApiException as e:
            result['message'] = "Bot is not a member of the channel chat or this channel chat does not exist."
        except Exception as e:
            result['message'] = "Something bad happend... Bot has not send this link. Please, try again."

        return Response(result)

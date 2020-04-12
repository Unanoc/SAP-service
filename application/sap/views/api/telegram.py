import telebot
from rest_framework.views import APIView
from rest_framework.response import Response

from application.sap.utils import send_to_telegram_channel


class BotSender(APIView):
    authentication_classes = []
    permission_classes = []

    def post (self, request, format=None):
        msg = request.data["message"]
        url = request.data["url"]
        tg_chan = request.data["telegram_channel"]
    
        msg_url = "{}\n\n{}".format(msg, url)
        result = dict()
        try:
            send_to_telegram_channel(channel=tg_chan, message=msg_url)
            result['message'] = "Done!"
        except telebot.apihelper.ApiException as e:
            result['message'] = "Bot is not a member of the channel chat or this channel chat does not exist."
        except Exception as e:
            result['message'] = "Something bad happend... Bot has not send this link. Please, try again."

        return Response(result)

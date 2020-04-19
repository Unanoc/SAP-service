import telebot
from django.utils.translation import gettext as _
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
            result['message'] = _("Done!")
        except telebot.apihelper.ApiException as e:
            print(e)
            result['message'] = _("Bot is not a member of the channel or this channel does not exist.")
        except Exception as e:
            print(e)
            result['message'] = _("Something bad happend... Bot has not send this link. Please, try again.")
        return Response(result)

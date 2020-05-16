import telebot

from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.response import Response


class BotSender(APIView):
    authentication_classes = []
    permission_classes = []

    def send_to_telegram_channel(self, channel, message):
        from application.settings import CONFIG

        bot = telebot.TeleBot(CONFIG['token'])
        bot.send_message(channel, text=message)


    def post(self, request, format=None):
        msg = request.data["message"]
        url = request.data["url"]
        chat = request.data["chat_name"]
    
        msg_url = "{}\n\n{}".format(msg, url)
        result = dict()
        try:
            self.send_to_telegram_channel(channel=chat, message=msg_url)
            result['message'] = _("Done!")
        except telebot.apihelper.ApiException as e:
            print(e)
            result['message'] = _("Bot is not a member of the channel or this channel does not exist.")
        except Exception as e:
            print(e)
            result['message'] = _("Something bad happend... Bot has not send this link. Please, try again.")
        return Response(result)

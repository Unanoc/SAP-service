import telebot
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from application.sap.models import (
    FeedbackSettings,
)
from application.sap.utils import send_to_telegram_channel


@login_required(login_url='/auth/signin/')
def telegrambot_send_to_telegram(request, hash):
    fs = FeedbackSettings.objects.get_by_hash(hash=hash)
    message = "Please, leave some feedback about passed class.\n\n{}/{}".format(
        fs.base_url, 
        fs.hash_url,
    )

    try:
        send_to_telegram_channel(channel=fs.telegram_channel, message=message)
    except telebot.apihelper.ApiException as e:
        return render(request, 'response_message.html', 
            {'message': "Bot is not a member of the channel chat or this channel chat does not exist."}
        )
    except Exception as e:
        return render(request, 'response_message.html', 
            {'message': "Something bad happend... Bot has not send this link. Please, try again."}
        )

    return redirect('/')

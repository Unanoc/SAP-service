from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response

from application.sap.models import (
    CommentedFeedback,
    EstimatedFeedback,
    FeedbackSettings,
)


class Commented(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            fs = FeedbackSettings.objects.get_by_id(id=request.data["settings"])
            cf = CommentedFeedback.objects.create(
                text=request.data["text"],
                settings=fs,
            )
            cf.save()
        except MultiValueDictKeyError:
            pass

        return Response({'status': 'OK'})
        

class Estimated(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        try:
            fs = FeedbackSettings.objects.get_by_id(id=request.data["settings"])
            cf = EstimatedFeedback.objects.create(
                rating=request.data['rating'],
                text=request.data['text'],
                settings=fs,
            )
            cf.save()
        except MultiValueDictKeyError:
            pass

        return Response({'status': 'OK'})


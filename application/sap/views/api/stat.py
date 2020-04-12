import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from application.sap.models import (
    CommentedFeedback,
    EstimatedFeedback,
)


class Comments(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        date = datetime.datetime.strptime(request.data["date"], '%d/%m/%Y').strftime('%Y-%m-%d')
        
        objects = CommentedFeedback.objects.get_group_comments_for_day(
            user_id=request.data["user_id"],
            date=date,
            group_name=request.data["group_name"].upper(),
            subject=request.data["subject"],
            class_type=request.data["class_type"],
        )

        result = {
            "group": request.data["group_name"].upper(),
            "subject": request.data["subject"],
            "comments": objects,
        }

        return Response(result)


class GroupAverage(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        date_from = datetime.datetime.strptime(request.data["from"], '%d/%m/%Y').strftime('%Y-%m-%d')
        date_to = datetime.datetime.strptime(request.data["to"], '%d/%m/%Y').strftime('%Y-%m-%d')
        
        objects = EstimatedFeedback.objects.get_group_average(
            user_id=request.data["user_id"],
            date_from=date_from,
            date_to=date_to,
            group_name=request.data["group_name"].upper(),
            subject=request.data["subject"],
            class_type=request.data["class_type"],
        )

        result = {
            "group": request.data["group_name"].upper(),
            "objects": objects,
        }

        return Response(result)


class GroupDayInfo(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        date = datetime.datetime.strptime(request.data["date"], '%d/%m/%Y').strftime('%Y-%m-%d')
        
        objects = EstimatedFeedback.objects.get_group_day_info(
            user_id=request.data["user_id"],
            date=date,
            group_name=request.data["group_name"].upper(),
            subject=request.data["subject"],
            class_type=request.data["class_type"],
        )

        result = {
            "group": request.data["group_name"].upper(),
            "date": date,
            "objects": objects,
        }

        return Response(result)

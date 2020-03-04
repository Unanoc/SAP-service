import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from application.sap.models import (
    EstimatedFeedback,
)


class GroupsData(APIView):
    authentication_classes = []
    permission_classes = []

    def post (self, request, format=None):
        date_from = datetime.datetime.strptime(request.data["from"], '%d/%m/%Y').strftime('%Y-%m-%d')
        date_to = datetime.datetime.strptime(request.data["to"], '%d/%m/%Y').strftime('%Y-%m-%d')
        
        objects = EstimatedFeedback.objects.get_group_stat(
            user_id=request.data["user_id"],
            date_from=date_from,
            date_to=date_to,
            group=request.data["group"].upper(),
            subject=request.data["subject"],
        )

        result = {
            "group": request.data["group"].upper(),
            "objects": objects,
        }

        return Response(result)
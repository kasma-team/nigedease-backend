from users.models.activity import ActivityLog
from users.serializers.activity import ActivityLogSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from typing import Dict, Any, cast

class ActivityLogView(APIView):

  @swagger_auto_schema(
      operation_summary="List activity logs",
      operation_description="Get a list of all activity logs",
      tags=['Activity Logs'],
      responses={
          200: ActivityLogSerializer(many=True)
      }
  )
  def get(self, request: Request):
    activity_logs = ActivityLog.get_all()
    serializer = ActivityLogSerializer(activity_logs, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
      operation_summary="Create activity log",
      operation_description="Create a new activity log",
      tags=['Activity Logs'],
      request_body=ActivityLogSerializer,
      responses={
          201: ActivityLogSerializer,
          400: 'Bad Request'
      }
  )
  def post(self, request: Request):
    data = cast(Dict[str, Any], request.data)
    activity_log = ActivityLog.create(
        user_id=data.get('user'),
        action=data.get('action'),
        description=data.get('description', '')
    )
    serializer = ActivityLogSerializer(activity_log)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ActivityLogDetailView(APIView):

  def get_activity_log(self, id):
    activity_log = ActivityLog.get_by_id(id)
    if not activity_log:
      raise Http404
    return activity_log
    
  @swagger_auto_schema(
      operation_summary="Get activity log detail",
      operation_description="Get details of a specific activity log",
      tags=['Activity Logs'],
      manual_parameters=[
          openapi.Parameter(
              'id',
              openapi.IN_PATH,
              description="Activity Log ID",
              type=openapi.TYPE_STRING,
              format=openapi.FORMAT_UUID
          )
      ],
      responses={
          200: ActivityLogSerializer,
          404: 'Not Found'
      }
  )
  def get(self, request: Request, id):
    activity_log = self.get_activity_log(id)
    serializer = ActivityLogSerializer(activity_log)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
      operation_summary="Update activity log",
      operation_description="Update an existing activity log",
      tags=['Activity Logs'],
      manual_parameters=[
          openapi.Parameter(
              'id',
              openapi.IN_PATH,
              description="Activity Log ID",
              type=openapi.TYPE_STRING,
              format=openapi.FORMAT_UUID
          )
      ],
      request_body=ActivityLogSerializer,
      responses={
          200: ActivityLogSerializer,
          400: 'Bad Request',
          404: 'Not Found'
      }
  )
  def put(self, request: Request, id):
    activity_log = self.get_activity_log(id)
    data = cast(Dict[str, Any], request.data)
    
    # Update fields
    updated_data = {
        "action": data.get('action', activity_log['action']),
        "description": data.get('description', activity_log['description'])
    }
    
    # We could add an update method to the ActivityLog class, but for now we'll use delete and create
    ActivityLog.delete(id)
    new_activity_log = ActivityLog.create(
        user_id=activity_log['user_id'],
        action=updated_data['action'],
        description=updated_data['description']
    )
    
    serializer = ActivityLogSerializer(new_activity_log)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
      operation_summary="Delete activity log",
      operation_description="Delete an activity log",
      tags=['Activity Logs'],
      manual_parameters=[
          openapi.Parameter(
              'id',
              openapi.IN_PATH,
              description="Activity Log ID",
              type=openapi.TYPE_STRING,
              format=openapi.FORMAT_UUID
          )
      ],
      responses={
          204: 'No Content',
          404: 'Not Found'
      }
  )
  def delete(self, request: Request, id):
    self.get_activity_log(id)  # Check if it exists
    ActivityLog.delete(id)
    return Response(status=status.HTTP_204_NO_CONTENT)

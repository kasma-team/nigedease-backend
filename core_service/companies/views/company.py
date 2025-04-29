from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
<<<<<<< Updated upstream
from drf_spectacular.utils import extend_schema, OpenApiResponse
from companies.models import Company
from companies.serializers.company import CompanySerializer


class CompanyListView(APIView):
    @extend_schema(
        description="Get a list of all companies",
=======
from rest_framework.permissions import IsAuthenticated
from core_service.auth import UserManagementJWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from companies.models import Company, SubscriptionPlan
from companies.serializers.company import CompanySerializer
from companies.permissions import IsSuperAdmin
import requests
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CompanyListView(APIView):
    authentication_classes = [UserManagementJWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    @swagger_auto_schema(
        operation_description="Get a list of all companies (Super Admin only)",
>>>>>>> Stashed changes
        responses={200: CompanySerializer(many=True)}
    )
    def get(self, request: Request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
<<<<<<< Updated upstream
    @extend_schema(
        description="Create a new company",
        request=CompanySerializer,
        responses={
            201: CompanySerializer,
            400: OpenApiResponse(description="Invalid data")
=======
    @swagger_auto_schema(
        operation_description="Create a new company with an admin user (Super Admin only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'short_name', 'address', 'subscription_plan_id', 'currency_id', 
                     'admin_first_name', 'admin_last_name', 'admin_email', 'admin_password'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Company name'),
                'short_name': openapi.Schema(type=openapi.TYPE_STRING, description='Company short name'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Company address'),
                'subscription_plan_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Subscription plan ID'),
                'currency_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Currency ID'),
                'admin_first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Admin user first name'),
                'admin_last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Admin user last name'),
                'admin_email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Admin user email'),
                'admin_password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Admin user password'),
            },
        ),
        responses={
            201: CompanySerializer,
            400: "Invalid data",
            403: "Permission denied"
>>>>>>> Stashed changes
        }
    )
    def post(self, request: Request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    authentication_classes = [UserManagementJWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    def get_company(self, id):
        try:
            return Company.objects.get(id=id)
        except Company.DoesNotExist:
            raise Http404
    
<<<<<<< Updated upstream
    @extend_schema(
        description="Get a specific company by ID",
        responses={
            200: CompanySerializer,
            404: OpenApiResponse(description="Company not found")
=======
    @swagger_auto_schema(
        operation_description="Get a specific company by ID (Super Admin only)",
        responses={
            200: CompanySerializer,
            404: "Company not found",
            403: "Permission denied"
>>>>>>> Stashed changes
        }
    )
    def get(self, request: Request, id):
        company = self.get_company(id)
        serializer = CompanySerializer(company)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

<<<<<<< Updated upstream
    @extend_schema(
        description="Update a company",
        request=CompanySerializer,
        responses={
            200: CompanySerializer,
            400: OpenApiResponse(description="Invalid data"),
            404: OpenApiResponse(description="Company not found")
=======
    @swagger_auto_schema(
        operation_description="Update a company (Super Admin only)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Company name'),
                'short_name': openapi.Schema(type=openapi.TYPE_STRING, description='Company short name'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='Company address'),
                'subscription_plan_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Subscription plan ID'),
                'currency_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid', description='Currency ID'),
            },
        ),
        responses={
            200: CompanySerializer,
            400: "Invalid data",
            404: "Company not found",
            403: "Permission denied"
>>>>>>> Stashed changes
        }
    )
    def put(self, request: Request, id):
        company = self.get_company(id)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

<<<<<<< Updated upstream
    @extend_schema(
        description="Delete a company",
        responses={
            204: OpenApiResponse(description="Company deleted successfully"),
            404: OpenApiResponse(description="Company not found")
=======
    @swagger_auto_schema(
        operation_description="Delete a company (Super Admin only)",
        responses={
            204: "Company deleted",
            404: "Company not found",
            403: "Permission denied"
>>>>>>> Stashed changes
        }
    )
    def delete(self, request: Request, id):
        company = self.get_company(id)
        company.delete()
        return Response({'message': 'Company deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
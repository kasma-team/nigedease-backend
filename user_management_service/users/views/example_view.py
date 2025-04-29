from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsSuperAdmin, IsAdmin, IsSales, IsStockManager, HasRolePermission
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SuperAdminOnlyView(APIView):
    """
    A view that only super admins can access.
    """
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    @swagger_auto_schema(
        operation_summary="Super Admin Only Endpoint",
        operation_description="This endpoint can only be accessed by users with the Superadmin role",
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Super Admin access granted"
                        )
                    }
                )
            ),
            403: "Forbidden"
        },
        tags=['Role-Based Access']
    )
    def get(self, request):
        return Response({"message": "Super Admin access granted"}, status=status.HTTP_200_OK)

class AdminOnlyView(APIView):
    """
    A view that only admins can access.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @swagger_auto_schema(
        operation_summary="Admin Only Endpoint",
        operation_description="This endpoint can only be accessed by users with the Admin role",
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Admin access granted"
                        )
                    }
                )
            ),
            403: "Forbidden"
        },
        tags=['Role-Based Access']
    )
    def get(self, request):
        return Response({"message": "Admin access granted"}, status=status.HTTP_200_OK)

class SalesOnlyView(APIView):
    """
    A view that only sales staff can access.
    """
    permission_classes = [IsAuthenticated, IsSales]
    
    @swagger_auto_schema(
        operation_summary="Sales Only Endpoint",
        operation_description="This endpoint can only be accessed by users with the Sales role",
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Sales access granted"
                        )
                    }
                )
            ),
            403: "Forbidden"
        },
        tags=['Role-Based Access']
    )
    def get(self, request):
        return Response({"message": "Sales access granted"}, status=status.HTTP_200_OK)

class StockManagerOnlyView(APIView):
    """
    A view that only stock managers can access.
    """
    permission_classes = [IsAuthenticated, IsStockManager]
    
    @swagger_auto_schema(
        operation_summary="Stock Manager Only Endpoint",
        operation_description="This endpoint can only be accessed by users with the Stock Manager role",
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Stock Manager access granted"
                        )
                    }
                )
            ),
            403: "Forbidden"
        },
        tags=['Role-Based Access']
    )
    def get(self, request):
        return Response({"message": "Stock Manager access granted"}, status=status.HTTP_200_OK)

class PermissionBasedView(APIView):
    """
    A view that requires a specific permission.
    """
    permission_classes = [IsAuthenticated, HasRolePermission('manage_inventory')]
    
    @swagger_auto_schema(
        operation_summary="Permission-Based Endpoint",
        operation_description="This endpoint requires the 'manage_inventory' permission",
        responses={
            200: openapi.Response(
                description='Success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Permission granted"
                        )
                    }
                )
            ),
            403: "Forbidden"
        },
        tags=['Role-Based Access']
    )
    def get(self, request):
        return Response({"message": "Permission granted"}, status=status.HTTP_200_OK) 
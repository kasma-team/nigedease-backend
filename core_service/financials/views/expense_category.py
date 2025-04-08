from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from financials.models.expense_category import ExpenseCategory
from financials.serializers.expense_category import ExpenseCategorySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ExpenseCategoryListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all expense categories",
        responses={200: ExpenseCategorySerializer(many=True)},
    )
    def get(self, request: Request):
        expense_categories = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(expense_categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new expense category",
        request_body=ExpenseCategorySerializer,
        responses={
            201: ExpenseCategorySerializer,
            400: "Bad Request",
        },
    )
    def post(self, request: Request):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseCategoryDetailView(APIView):
    def get_category(self, id):
        try:
            category = ExpenseCategory.objects.get(pk=id)
            return category
        except ExpenseCategory.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a specific expense category by ID",
        responses={200: ExpenseCategorySerializer, 404: "Not Found"},
    )
    def get(self, request: Request, id):
        category = self.get_category(id)
        serializer = ExpenseCategorySerializer(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific expense category by ID",
        request_body=ExpenseCategorySerializer,
        responses={
            200: ExpenseCategorySerializer,
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def put(self, request: Request, id):
        category = self.get_category(id)
        serializer = ExpenseCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific expense category by ID",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request: Request, id):
        category = self.get_category(id)
        category.delete()
        return Response({'message': 'Expense category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
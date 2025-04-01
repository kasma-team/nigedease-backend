from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentModeViewSet, CurrencyViewSet, SubscriptionPlanViewSet,
    CompanyViewSet, BankViewSet, PaymentInViewSet, PaymentOutViewSet,
    ReportViewSet
)

router = DefaultRouter()
router.register(r'paymentmodes', PaymentModeViewSet, basename='paymentmode')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'subscriptionplans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'paymentins', PaymentInViewSet, basename='paymentin')
router.register(r'paymentouts', PaymentOutViewSet, basename='paymentout')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
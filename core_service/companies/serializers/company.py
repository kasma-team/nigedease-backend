from rest_framework import serializers
from companies.models.company import Company
from companies.serializers.currency import CurrencySerializer
from companies.serializers.subscription_plan import SubscriptionPlanSerializer

class AdminUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

class CompanySerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    subscription_plan_id = serializers.UUIDField(write_only=True)
    currency_id = serializers.UUIDField(write_only=True)
    
    # Admin user fields
    admin_email = serializers.EmailField(write_only=True, required=True)
    admin_password = serializers.CharField(write_only=True, required=True)
    admin_first_name = serializers.CharField(write_only=True, required=True)
    admin_last_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'short_name', 'address',
            'subscription_plan', 'currency',
            'subscription_plan_id', 'currency_id',
            'admin_email', 'admin_password', 'admin_first_name', 'admin_last_name',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'name': {'required': True},
            'short_name': {'required': True},
            'address': {'required': True},
            'subscription_plan_id': {'required': True},
            'currency_id': {'required': True},
        }

    def create(self, validated_data):
        # Extract admin user data
        admin_data = {
            'email': validated_data.pop('admin_email'),
            'password': validated_data.pop('admin_password'),
            'first_name': validated_data.pop('admin_first_name'),
            'last_name': validated_data.pop('admin_last_name'),
        }
        
        # Create company
        company = super().create(validated_data)
        
        # Create admin user in user management service
        try:
            import requests
            from django.conf import settings
            
            # Prepare user data
            user_data = {
                'email': admin_data['email'],
                'password': admin_data['password'],
                'first_name': admin_data['first_name'],
                'last_name': admin_data['last_name'],
                'company_id': str(company.id),
                'role': 'Admin'  # This assumes the role name in user management service
            }
            
            # Make request to user management service
            response = requests.post(
                f"{settings.USER_MANAGEMENT_SERVICE_URL}/users/",
                json=user_data,
                timeout=5
            )
            
            if response.status_code != 201:
                # If user creation fails, delete the company
                company.delete()
                raise serializers.ValidationError({
                    'admin_user': 'Failed to create admin user. Please try again.'
                })
                
        except requests.RequestException as e:
            # If there's a connection error, delete the company
            company.delete()
            raise serializers.ValidationError({
                'admin_user': f'Error connecting to user management service: {str(e)}'
            })
            
        return company


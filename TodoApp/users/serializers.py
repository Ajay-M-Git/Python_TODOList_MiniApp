from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  
    def validate_username(self, value):

        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric and not contain spaces.")
        return value
    
    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value
    
    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Name must contain only alphabets.")
        return value
    
    def create(self, validated_data):
        password = validated_data.get('password')  
        user = CustomUser.objects.create_user(**validated_data) 
        user._plain_password = password  
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
    
        if hasattr(instance, '_plain_password'):
            representation['password'] = instance._plain_password  
        
        return representation


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def validate(self, data):
        refresh = RefreshToken(data['refresh'])
        return {'access': str(refresh.access_token), 'refresh': str(refresh)}

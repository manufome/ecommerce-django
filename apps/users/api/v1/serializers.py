from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def validate(self, data):
        if data['first_name'] == '' or data['last_name'] == '':
            raise serializers.ValidationError("El nombre y apellido son requeridos")
        if User.objects.filter(username=data['username']).exists() and self.instance.username != data['username']:
            raise serializers.ValidationError("El nombre de usuario ya existe")
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("El correo electrónico ya existe")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        if len(data['password']) < 8 or not any(char.isdigit() for char in data['password']) or not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in data['password']):
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres, un número y un carácter especial")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        if len(data['new_password']) < 8 or not any(char.isdigit() for char in data['new_password']) or not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in data['new_password']):
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres, un número y un carácter especial")
        return data
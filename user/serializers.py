from rest_framework import serializers
from .models import User
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "birthdate",
            "age",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_age(self, obj):
        today = date.today()
        age = (
            today.year
            - obj.birthdate.year
            - ((today.month, today.day) < (obj.birthdate.month, obj.birthdate.day))
        )
        return age

    def validate_birthdate(self, value):
        if (date.today() - value).days < (15 * 365.25):
            raise serializers.ValidationError("Vous devez avoir minimum 15 ans")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

        """user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            birthdate=validated_data["birthdate"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user"""

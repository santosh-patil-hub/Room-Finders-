# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



# serializers.py

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return {'user': user}




# serializers.py

from rest_framework import serializers
from .models import Room, Area
from django.contrib.auth import get_user_model

User = get_user_model()

# Area Serializer
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']

# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Optional for owner
    area = AreaSerializer()

    class Meta:
        model = Room
        fields = [
            'id', 'owner', 'title', 'room_type', 'rent_per_month', 'deposit', 'light_bill_responsibility',
            'occupants_allowed', 'address', 'landmark', 'area', 'house_number', 'floor_number', 
            'image1', 'image2', 'image3', 'image4', 'image5', 'owner_mobile_no'
        ]

    def create(self, validated_data):
        area_data = validated_data.pop('area')
        area_instance = Area.objects.create(**area_data)  # Create the Area instance
        validated_data['area'] = area_instance
        
        # Create the Room instance
        room = Room.objects.create(**validated_data)
        return room

    def update(self, instance, validated_data):
        area_data = validated_data.pop('area', None)
        if area_data:
            # Update the area instance if necessary
            area_instance = instance.area
            for attr, value in area_data.items():
                setattr(area_instance, attr, value)
            area_instance.save()
        
        # Update the Room instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

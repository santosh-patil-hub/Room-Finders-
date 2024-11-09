# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Room, Area
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
    
    def create(self, validated_data):
        # sourcery skip: inline-immediately-returned-variable
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return {'user': user}


# Area Serializer
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']

# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Optional for owner
    area = AreaSerializer()  # Nested AreaSerializer

    class Meta:
        model = Room
        fields = [
            'id', 'owner', 'title', 'room_type', 'rent_per_month', 'deposit', 'light_bill_responsibility',
            'occupants_allowed', 'address', 'landmark', 'area', 'house_number', 'floor_number', 
            'image1', 'image2', 'image3', 'image4', 'image5', 'owner_mobile_no', 'availability_status'
        ]

    def create(self, validated_data):
        # Pop the area data from validated data and create the Area instance
        area_data = validated_data.pop('area')
        area_instance = Area.objects.create(**area_data)  # Create the Area instance
        
        # Create the Room instance and associate the newly created area instance
        room = Room.objects.create(area=area_instance, **validated_data)
        return room

    def update(self, instance, validated_data):
        # Check for area data in the update request and update if present
        area_data = validated_data.pop('area', None)
        if area_data:
            # If the area exists, update it
            area_instance = instance.area
            for attr, value in area_data.items():
                setattr(area_instance, attr, value)
            area_instance.save()
        
        # Now update the Room instance itself with the remaining validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'room_type', 'rent_per_month', 'deposit', 'address', 'landmark', 'area']
        ordering = ['-rent_per_month']  # Default ordering by rent_per_month descending
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'room_type': {'read_only': True},
            'rent_per_month': {'read_only': True},
            'deposit': {'read_only': True},
            'address': {'read_only': True},
            'landmark': {'read_only': True},
            'area': {'read_only': True},
        }

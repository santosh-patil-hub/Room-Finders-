# views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer

# views.py

from rest_framework.permissions import AllowAny  # Import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view (no authentication required)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user if serializer is valid
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view (no authentication required)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


# views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class OwnerRoomView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Ensure the user is an owner
        user = request.user
        if user.user_type != 'owner':
            return Response({"message": "Only owners can create rooms."}, status=status.HTTP_403_FORBIDDEN)
        
        # Create a room
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=user)  # Save room with the current user as the owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, room_id):
        # Ensure the user is an owner and has permission to update the room
        user = request.user
        if user.user_type != 'owner':
            return Response({"message": "Only owners can update rooms."}, status=status.HTTP_403_FORBIDDEN)

        try:
            room = Room.objects.get(id=room_id, owner=user)
        except Room.DoesNotExist:
            return Response({"message": "Room not found or you do not have permission to edit it."}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the room
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        # Ensure the user is an owner and has permission to delete the room
        user = request.user
        if user.user_type != 'owner':
            return Response({"message": "Only owners can delete rooms."}, status=status.HTTP_403_FORBIDDEN)

        try:
            room = Room.objects.get(id=room_id, owner=user)
        except Room.DoesNotExist:
            return Response({"message": "Room not found or you do not have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the room
        room.delete()
        return Response({"message": "Room deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer

class TenantDashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all rooms (no exclusion, showing rooms owned by others as well)
        rooms = Room.objects.all()  # Get all rooms
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

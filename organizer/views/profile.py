from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from ..models import OrganizerProfile
from ..serializers import OrganizerProfileSerializer


class OrganizerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=OrganizerProfileSerializer)
    def get(self, request):
        try:
            profile = OrganizerProfile.objects.get(user=request.user)
            serializer = OrganizerProfileSerializer(profile)
            return Response(serializer.data)
        except OrganizerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=OrganizerProfileSerializer, responses=OrganizerProfileSerializer)
    def post(self, request):
        if OrganizerProfile.objects.filter(user=request.user).exists():
            return Response({'error': 'Profile already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrganizerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=OrganizerProfileSerializer, responses=OrganizerProfileSerializer)
    def put(self, request):
        try:
            profile = OrganizerProfile.objects.get(user=request.user)
        except OrganizerProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerProfileListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=OrganizerProfileSerializer)
    def get(self, request):
        profiles = OrganizerProfile.objects.all()
        serializer = OrganizerProfileSerializer(profiles, many=True)
        return Response(serializer.data)

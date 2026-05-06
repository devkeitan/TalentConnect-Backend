from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from ..models import TalentPortfolio, TalentMedia
from ..serializers import TalentMediaSerializer
import httpx
import os
import uuid

class TalentMediaUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            portfolio = TalentPortfolio.objects.get(user=request.user)
        except TalentPortfolio.DoesNotExist:
            return Response({'error': 'Create your portfolio first'}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        ext = file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{ext}"
        file_path = f"talent_media/{unique_filename}"

        supabase_url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')

        upload_url = f"{supabase_url}/storage/v1/object/talent-media/{file_path}"
        headers = {
            "Authorization": f"Bearer {service_key}",
            "Content-Type": file.content_type,
        }
        response = httpx.post(upload_url, content=file.read(), headers=headers)

        if response.status_code not in [200, 201]:
            return Response({'error': 'Upload failed', 'detail': response.text}, status=500)

        public_url = f"{supabase_url}/storage/v1/object/public/talent-media/{file_path}"

        media = TalentMedia.objects.create(
            portfolio=portfolio,
            media_type=request.data.get('media_type', 'photo'),
            file=public_url,
            caption=request.data.get('caption', file.name)
        )

        serializer = TalentMediaSerializer(media)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, media_id):
        try:
            media = TalentMedia.objects.get(id=media_id, portfolio__user=request.user)
        except TalentMedia.DoesNotExist:
            return Response({'error': 'Media not found'}, status=status.HTTP_404_NOT_FOUND)

        # Extract file path from the public URL
        # URL format: https://xxx.supabase.co/storage/v1/object/public/talent-media/talent_media/filename.jpg
        supabase_url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')
        file_url = media.file
        file_path = file_url.split('/storage/v1/object/public/talent-media/')[-1]

        # Delete from Supabase Storage bucket
        delete_url = f"{supabase_url}/storage/v1/object/talent-media/{file_path}"
        headers = {"Authorization": f"Bearer {service_key}"}
        httpx.delete(delete_url, headers=headers)

        # Delete from DB
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

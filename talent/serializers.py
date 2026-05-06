from rest_framework import serializers
from .models import TalentPortfolio, TalentMedia


class TalentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentMedia
        fields = ['id', 'media_type', 'file', 'caption', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class TalentPortfolioSerializer(serializers.ModelSerializer):
    media = TalentMediaSerializer(many=True, read_only=True)  # nested media list
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = TalentPortfolio
        fields = [
            'id', 'user_email', 'talent_name',
            'location', 'bio', 'service_type',
            'min_price', 'max_price', 'is_available',
            'media', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

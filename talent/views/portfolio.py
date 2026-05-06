from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from ..models import TalentPortfolio
from ..serializers import TalentPortfolioSerializer

class TalentPortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=TalentPortfolioSerializer)
    def get(self, request):
        try:
            portfolio = TalentPortfolio.objects.get(user=request.user)
            serializer = TalentPortfolioSerializer(portfolio)
            return Response(serializer.data)
        except TalentPortfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=TalentPortfolioSerializer, responses=TalentPortfolioSerializer)
    def post(self, request):
        if TalentPortfolio.objects.filter(user=request.user).exists():
            return Response({'error': 'Portfolio already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TalentPortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=TalentPortfolioSerializer, responses=TalentPortfolioSerializer)
    def put(self, request):
        try:
            portfolio = TalentPortfolio.objects.get(user=request.user)
        except TalentPortfolio.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TalentPortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Public — anyone can browse talent portfolios
class TalentPortfolioListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=TalentPortfolioSerializer)
    def get(self, request):
        portfolios = TalentPortfolio.objects.all()
        serializer = TalentPortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)
    
class TalentPortfolioDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, portfolio_id):
        try:
            portfolio = TalentPortfolio.objects.get(id=portfolio_id)
            serializer = TalentPortfolioSerializer(portfolio)
            return Response(serializer.data)
        except TalentPortfolio.DoesNotExist:
            return Response({'error': 'Talent not found'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BloodRequest
from blood.serializers import  BloodRequestSerializer,DonorSerializer,DonationHistorySerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from user.models import User
from rest_framework.views import APIView
from rest_framework.pagination import  PageNumberPagination
from urllib.parse import unquote_plus


class DefaultPagination(PageNumberPagination):
    page_size = 9

class BloodRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing blood requests.
    
    - Users can only see their own requests (as requester or donor)
    - Creating requests requires authentication
    """
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        return BloodRequest.objects.filter(
            Q(requester=user) | Q(donor=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Accept a blood donation request.
        
        - Only available for pending requests
        - Donor must be eligible (available and past cooldown period)
        - Updates donor's last donation date and availability
        """
        blood_request = self.get_object()
        user = request.user

        # Validate request state
        if blood_request.status != 'Pending':
            return Response(
                {'error': 'This request is no longer available for acceptance'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent self-acceptance
        if blood_request.requester == user:
            return Response(
                {'error': 'You cannot accept your own blood request'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if already has a donor
        if blood_request.donor:
            return Response(
                {'error': 'This request already has a donor'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate donor eligibility
        if not user.is_available:
            return Response(
                {'error': 'You are currently marked as unavailable for donations'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check donation cooldown period
        if user.last_donation_date:
            cooldown_period = timezone.now().date() - timedelta(days=90)
            if user.last_donation_date > cooldown_period:
                return Response(
                    {'error': 'You must wait 90 days between donations'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Update blood request and donor status
        try:
            blood_request.donor = user
            blood_request.status = 'Accepted'
            blood_request.save()
            
            # Update donor's last donation date and availability
            user.last_donation_date = timezone.now().date()
            user.is_available = False
            user.save()
            
            return Response(
                {
                    'status': 'Request accepted successfully',
                    'details': {
                        'request_id': blood_request.id,
                        'next_eligible_date': user.last_donation_date + timedelta(days=90)
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    


class DonorFilter(filters.FilterSet):
    blood_group = filters.ChoiceFilter(
        choices=User.BLOOD_GROUP_CHOICES,
        label='Blood Group'
    )
    
    class Meta:
        model = User
        fields = ['blood_group']

class DonorListView(ListAPIView):

    """
    List available donors
    
    Public endpoint - no authentication required
    Filterable by blood_group using query parameters
    """
   
    serializer_class = DonorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DonorFilter
    pagination_class = DefaultPagination
    def get_queryset(self):
        queryset = User.objects.filter(
            is_available=True,
            blood_group__isnull=False
        ).exclude(blood_group='')

        # Manually decode the blood_group param
        blood_group_raw = self.request.GET.get('blood_group')
        if blood_group_raw:
            blood_group = unquote_plus(blood_group_raw)
            queryset = queryset.filter(blood_group=blood_group)

        return queryset.order_by('blood_group', '-last_donation_date')
    

class Dashboard(APIView):

    """
    User dashboard showing:
    
    - Active requests (excluding user's own requests)
    - User's donation history
    - Endpoint to accept requests (POST)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        active_requests = BloodRequest.objects.exclude(
            requester=request.user
        ).filter(status='Pending')  

        donation_history = BloodRequest.objects.filter(
            donor=request.user
        )
        
        return Response({
            'active_requests': BloodRequestSerializer(active_requests, many=True).data,
            'donation_history': DonationHistorySerializer(donation_history, many=True).data
        })
    
    def post(self, request):
        request_id = request.data.get('request_id')
        try:
            blood_request = BloodRequest.objects.get(id=request_id)
            if blood_request.status == 'Pending' and blood_request.requester != request.user:
                blood_request.status = 'Accepted'  
                blood_request.donor = request.user 
                blood_request.save()
                return Response({'status': 'Request accepted'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
        except BloodRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
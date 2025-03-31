from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Ticket
from .serializer import TicketSerializer
from apps.users.permissions import IsAdmin
from django.utils.http import urlsafe_base64_decode



# Create your views here.
class TicketsViewSet(ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.all()
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        createdAt = self.request.query_params.get('createdAt')
        if status is not None:
            queryset = queryset.filter(status=status)
        if priority is not None:
            queryset = queryset.filter(priority=priority)
        if createdAt is not None:
            queryset = queryset.filter(createdAt=createdAt)
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update','list']:
            return [IsAdmin()]
        return []  
    
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # send email to notfiy the user
        send_mail(
            subject="Customer Support Ticketing System",
            message="Your issue is " + updated_instance.status,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[updated_instance.senderEmail],
            fail_silently=False,
        )

        return Response(self.get_serializer(updated_instance).data)
    
    @action(detail=False, methods=['get'], url_path=r'user/(?P<email>.+)')
    def user_tickets(self, request, email=None):
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
   
        queryset = Ticket.objects.filter(senderEmail=email)
        if not queryset.exists():
            return Response({"message": "No tickets found for this email"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketSerializer(queryset, many=True)
        return Response({"tickets": serializer.data}, status=status.HTTP_200_OK)
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

class BootcampView(generics.CreateAPIView):
    serializer_class = BootcampSerializer
    
    def send_mail(self, email):
        from_email = "Support@aoo.com"

        to_email = email
        subject = 'Bootcamp Registration Confirmation'
        text_content = 'Bootcamp Registration Confirmation'
        html_content = render_to_string('bootcamp_email.html')

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')
        try:
            client = Bootcamp_client.objects.get(email=email)
            return Response({"message":"Email already exists"}, status=400)
        except Bootcamp_client.DoesNotExist:
            try:
                client = Bootcamp_client.objects.create(name=name, phone_number=phone_number, email=email)
                client = Bootcamp_client.objects.get(email=email)
                workload= self.send_mail(client.email)
                return Response({"message":"Successful"}, status=202)
            except:
                client = Bootcamp_client.objects.create(name=name, phone_number=None, email=email)
                client = Bootcamp_client.objects.get(email=email)
                workload= self.send_mail(client.email)
                return Response({"message":"Successful"}, status=202)
        

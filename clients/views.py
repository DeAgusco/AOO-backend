import asyncio
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from telegram import Bot
from django.conf import settings

# Create your views here.
class ClientView(generics.CreateAPIView):
    serializer_class = ClientSerializer

    async def send_telegram_message(self, message):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        chat_id = settings.TELEGRAM_CHAT_ID
        try:
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(e)

    def send_mail(self,name,email,description):
        from_email = "Achlogs@achlive.net"

        to_email = ["deagusco@gmail.com", "kobbyisreal@gmail.com"]
        subject = 'Order confirmation'
        text_content = 'Thank you for the order!'
        html_content = render_to_string('email_client.html', context={"name":name,"email":email,"description":description})

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        phone_number = serializer.validated_data.get('phone_number')
        email = serializer.validated_data.get('email')
        job_description = serializer.validated_data.get('job_description')
        
        try:
            client = Client.objects.get(email=email)
            return Response({"message": "Email already exists"}, status=400)
        except Client.DoesNotExist:
            try:
                client = Client.objects.create(name=name, phone_number=phone_number, email=email, job_description=job_description)
                # Use asyncio.run to call the async function
                message = f"New client created!\n\nBilling Info: {job_description}\n Name: {name}\nEmail Address: {email}\nPhone Number: {phone_number}"
                asyncio.run(self.send_telegram_message(message))
                self.send_mail(name,email,description=job_description)
                return Response({"message":"Successful"}, status=202)
            except:
                client = Client.objects.create(name=name, phone_number=None, email=email, job_description=job_description)
                # Use asyncio.run to call the async function
                message = f"New client created!\n\nBilling Info: {job_description}\n Name: {name}\nEmail Address: {email}\nPhone Number: {phone_number}"
                asyncio.run(self.send_telegram_message(message))
                self.send_mail(name,email,description=job_description)
                return Response({"message":"Successful"}, status=202)

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializsrs import OTPSerializer
from .models import OTP
from .services import OTPService
from smtp_client import send_email

class OTPViewsSet(viewsets.APIView):
    serializer_class = OTPSerializer
    
    def create(self):
            user = self.request.user
            mail = self.request.data.get('mail')
            code_otp = OTPService.generate_code()
            otp_code = OTP(
                user = user or None,
                hash_otp = OTPService.hash_otp(code_otp),
            )
            
            # send email
            if send_email(
                to_addr=mail,
                msg=f"Your OTP code for authentication is {code_otp}"
            ):
                return Response(
                    data={
                        "uuid": otp_code.uuid,
                    }
                )
            else:
                return Response(
                    data={
                        "msg": "Error while sending email!"
                    },
                    status=500
                )
        
    def get(self):
        user = self.request.user
        code_uuid = self.request.query_params.get('pk')
        otp = self.requests.query_params.get('otp')
        
        # clear old codes
        if user.is_time_to_clean_otp:
            otps = OTP.object.filter(user=self.request.user).all()
            
            for otp in otps:
                if not otp.is_valid:
                    otp.delete()
        
        otp_instance = OTP.objects.get(
            code_uuid=code_uuid    
        )
        hash_otp = otp_instance.hash_otp
        
        return Response(
            data={
                "validation": OTPService.check_otp(
                        otp_instance,
                        otp, 
                        hash_otp
                    ) 
            },
            status=200
        )
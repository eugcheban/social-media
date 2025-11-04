from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializsrs import OTPSerializer
from .models import OTP
from .services import OTPService

class OTPViewsSet(viewsets.APIView):
    serializer_class = OTPSerializer
    
    def create(self):
            user = self.request.user
            otp_code = OTP(
                user = user or None,
                hash_otp = OTPService.generate_code(),   
            )
            
            return Response(
                data={
                    "uuid": otp_code.uuid,
                    "hash_otp": otp_code.hash_otp
                }
            )
        
    def get(self):
        user = self.request.user
        uuid = self.request.query_params.get('pk')
        otp = self.requests.query_params.get('otp')
        
        if user.is_time_to_clean_otp:
            otps = OTP.object.filter(uuid=uuid).all()
            
            for otp in otps:
                if not otp.is_valid:
                    otp.delete()
                    
        return Response(
            data={
                "validation": OTPService.check_otp(otp)         
            },
            status=200
        )
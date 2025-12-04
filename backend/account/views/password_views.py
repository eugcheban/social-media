from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from ..serializers.password_serializers import PasswordChangeSerizliser, PasswordResetSerializer
from rest_framework.decorators import action
from otp.services import OTPService


class PasswordViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordChangeSerizliser
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=["post"], url_path="change")
    def change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully"})


class PasswordResetViewSet(viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]
    
    @action(
        detail=False,
        methods=["post"],
        url_path="reset",
    )
    def reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        send_email_response, otp_instance = OTPService.send_email_otp(
            user=serializer.validated_data['user'],
            email=serializer.validated_data['email']
            
        )
        
        if send_email_response:
            return Response({
                'code_uuid': otp_instance.code_uuid,
            }, status=200)
        else:
            return Response({
                'error': 'Internal server error while reseting password!',
                'email_response': send_email_response
            }, status=500)
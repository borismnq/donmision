from django.db import models
from common.models import TimeStampedModel
import qrcode
import io
import uuid
import jwt
from django.conf import settings


# def decode_qr():
#     encoded_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaXNzaW9uX2lkIjoxMCwidmFsdWUiOjUwfQ.W-GbeDKCESmooP_qLb4H_Nzp3Zo0ZYm1T1WeKh9HT_w"
#     decoded = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#     print(decoded)
def generate_qr_code(data:dict):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=2,
    )
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    qr.add_data(encoded_jwt)
    qr.make(fit=True)
    img = qr.make_image(fill_color="darkblue", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

class QRs(TimeStampedModel):
    mission = models.ForeignKey('missions.Mission', on_delete=models.CASCADE)
    user_organization = models.ForeignKey('users.UserOrganization', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes/')
    scanned = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=[
        ('pending', 'Pending'),
        ('scanned', 'Scanned'),
        ('deleted', 'Deleted')
    ], default='pending')


    def __str__(self):
        return f"QR Code for {self.mission.title}"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code.save(f"{uuid.uuid4()}.png", content=generate_qr_code(
                {
                    "mission_id": self.mission.id,
                    "value": self.value,
                    "scanned": self.scanned
                }
            ), save=False)
        super().save(*args, **kwargs)
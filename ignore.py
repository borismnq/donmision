# import qrcode
# import io
# import json
# import jwt

# from django.conf import settings

# def generate_qr_code(data):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=8,
#         border=2,
#     )
#     data = {
#         "mission_id":10,
#         "value":50
#     }
#     encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
#     qr.add_data(encoded_jwt)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="darkblue", back_color="white")
#     buffer = io.BytesIO()
#     img.save(buffer, format="PNG")
#     with open('qrcode3.png', 'wb') as f:
#         f.write(buffer.getvalue())
#     return buffer.getvalue()

# def decode_qr():
#     encoded_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaXNzaW9uX2lkIjoxMCwidmFsdWUiOjUwfQ.W-GbeDKCESmooP_qLb4H_Nzp3Zo0ZYm1T1WeKh9HT_w"
#     decoded = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#     print(decoded)

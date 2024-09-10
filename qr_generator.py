import qrcode
from io import BytesIO
import base64

class QRGenerator:
    @staticmethod
    def generate_qr(person_id):
        data = f"http://localhost:5000/scan_qr/{person_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buf = BytesIO()
        img.save(buf, format='PNG')
        qr_code = base64.b64encode(buf.getvalue()).decode('utf-8')
        return qr_code

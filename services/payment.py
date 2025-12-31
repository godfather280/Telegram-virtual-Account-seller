import qrcode
from io import BytesIO
from config import UPI_ID, PAYMENT_TIMEOUT
from datetime import datetime

class PaymentService:
    @staticmethod
    def generate_qr_code(amount, payment_id):
        """Generate UPI QR code"""
        upi_url = f"upi://pay?pa={UPI_ID}&pn=Virtual%20Numbers&am={amount}&tn=Payment ID: {payment_id}&cu=INR"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        img.save(bio, "PNG")
        bio.seek(0)
        
        return bio
    
    @staticmethod
    def get_payment_instructions(payment_id, amount):
        """Get payment instructions"""
        minutes = PAYMENT_TIMEOUT // 60
        
        return f"""
💰 **Payment Instructions** 💰

**Payment ID:** `{payment_id}`
**Amount:** ₹{amount}
**UPI ID:** `{UPI_ID}`

**Steps to Pay:**
1. Open your UPI app (FamApp, Google Pay, PhonePe, etc.)
2. Send ₹{amount} to UPI ID: `{UPI_ID}`
3. After payment, you'll get a UTR/Transaction ID
4. Come back here and send that UTR

**OR Scan QR Code below:**

**Note:** Payment expires in {minutes} minutes
        """
    
    @staticmethod
    def validate_utr(utr):
        """Validate UTR format"""
        if not utr or len(utr) < 8:
            return False, "Invalid UTR format"
        
        # Basic validation - can be extended
        if not utr.isalnum():
            return False, "UTR should contain only letters and numbers"
        
        return True, "UTR is valid"
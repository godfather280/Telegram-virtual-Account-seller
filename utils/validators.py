import re

class Validators:
    @staticmethod
    def validate_amount(amount, min_amount=1):
        """Validate amount"""
        try:
            amount_num = float(amount)
            if amount_num < min_amount:
                return False, f"Amount must be at least {min_amount}"
            return True, "Amount is valid"
        except ValueError:
            return False, "Invalid amount format"
    
    @staticmethod
    def validate_utr(utr):
        """Validate UTR"""
        if not utr or len(utr) < 8:
            return False, "UTR must be at least 8 characters"
        
        # Check for basic format (can be extended based on bank formats)
        if not re.match(r'^[A-Za-z0-9]+$', utr):
            return False, "UTR can only contain letters and numbers"
        
        return True, "UTR is valid"
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate phone number"""
        if not phone:
            return False, "Phone number is required"
        
        # Basic international phone validation
        if not re.match(r'^\+[1-9]\d{1,14}$', phone):
            return False, "Invalid phone number format"
        
        return True, "Phone number is valid"
    
    @staticmethod
    def validate_session_string(session_string):
        """Validate Telegram session string"""
        if not session_string:
            return False, "Session string is required"
        
        if len(session_string) < 50:
            return False, "Invalid session string length"
        
        # Basic validation (can be extended)
        return True, "Session string is valid"
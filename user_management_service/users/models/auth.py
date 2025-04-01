import uuid
from datetime import datetime, timedelta
from user_management.mongodb import db

# MongoDB Collections
otp_collection = db.otp

class OTP:
    @staticmethod
    def create(user_id, otp_code):
        """Create a new OTP"""
        otp = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "otp": otp_code,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        otp_collection.insert_one(otp)
        return otp
    
    @staticmethod
    def get_by_id(otp_id):
        """Get OTP by ID"""
        return otp_collection.find_one({"id": otp_id})
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get latest OTP for a user"""
        return otp_collection.find_one({"user_id": user_id}, sort=[("created_at", -1)])
    
    @staticmethod
    def get_by_code(user_id, otp_code):
        """Get OTP by code and user"""
        return otp_collection.find_one({"user_id": user_id, "otp": otp_code})
    
    @staticmethod
    def update(otp_id, data):
        """Update an OTP"""
        data["updated_at"] = datetime.utcnow()
        otp_collection.update_one({"id": otp_id}, {"$set": data})
        return otp_collection.find_one({"id": otp_id})
    
    @staticmethod
    def create_or_update(user_id, otp):
        """Create new OTP or update existing one"""
        existing_otp = OTP.get_by_user_id(user_id)
        
        if existing_otp:
            # Update existing OTP
            OTP.update(existing_otp["id"], {"otp": otp})
            return OTP.get_by_id(existing_otp["id"])
        else:
            # Create new OTP
            return OTP.create(user_id, otp)
    
    @staticmethod
    def delete(otp_id):
        """Delete an OTP"""
        otp_collection.delete_one({"id": otp_id})
    
    @staticmethod
    def is_expired(otp_document):
        """Check if the OTP is expired (older than 10 minutes)"""
        if not otp_document:
            return True
            
        update_time = otp_document["updated_at"]
        expiry_time = update_time + timedelta(minutes=10)
        return datetime.utcnow() > expiry_time
import uuid
from datetime import datetime
from user_management.mongodb import db

# MongoDB Collections
activity_logs_collection = db.activity_logs

class ActivityLog:
    @staticmethod
    def create(user_id, action, description=""):
        """Create a new activity log entry"""
        activity_log = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "action": action,
            "description": description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        activity_logs_collection.insert_one(activity_log)
        return activity_log
    
    @staticmethod
    def get_by_id(activity_id):
        """Get activity log by ID"""
        return activity_logs_collection.find_one({"id": activity_id})
    
    @staticmethod
    def get_by_user(user_id):
        """Get all activity logs for a user"""
        return list(activity_logs_collection.find({"user_id": user_id}).sort("created_at", -1))
    
    @staticmethod
    def get_all():
        """Get all activity logs"""
        return list(activity_logs_collection.find().sort("created_at", -1))
    
    @staticmethod
    def delete(activity_id):
        """Delete an activity log"""
        activity_logs_collection.delete_one({"id": activity_id}) 
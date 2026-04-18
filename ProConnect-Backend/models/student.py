"""
Student Model - Represents student records in the system
"""
from datetime import datetime

class Student:
    """Student model for MongoDB"""
    
    def __init__(self, basic_info, parent_details, siblings=None, relatives=None, created_at=None):
        """
        Initialize a Student object
        
        Args:
            basic_info: Dictionary containing student's basic information
            parent_details: Dictionary containing parent/guardian information
            siblings: List of siblings in engineering field (optional)
            relatives: List of relatives/contacts in engineering field (optional)
            created_at: Creation timestamp (auto-generated if not provided)
        """
        self.basic_info = basic_info
        self.parent_details = parent_details
        self.siblings = siblings or []
        self.relatives = relatives or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = created_at or datetime.utcnow()
        self.status = "submitted"
    
    def to_dict(self):
        """Convert Student object to dictionary for MongoDB storage"""
        return {
            'basic_info': self.basic_info,
            'parent_details': self.parent_details,
            'siblings': self.siblings,
            'relatives': self.relatives,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        """Create Student object from MongoDB document"""
        if data is None:
            return None
        
        student = Student(
            basic_info=data.get('basic_info', {}),
            parent_details=data.get('parent_details', {}),
            siblings=data.get('siblings', []),
            relatives=data.get('relatives', []),
            created_at=data.get('created_at')
        )
        student.updated_at = data.get('updated_at')
        student.status = data.get('status', 'submitted')
        return student

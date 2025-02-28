import re
import psycopg2  # Assuming you're using psycopg2 for PostgreSQL

class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

class EmailValidator:
    def __init__(self, email):
        self.email = email

    def validate_email(self):
        """Validates email format and prevents SQL injection"""
        
        # Email regex for basic validation
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, self.email):
            raise DataValidationError("Invalid email format")
        
        # Preventing SQL injection by using parameterized queries
        # (Example assumes you are querying a database for checking the email)
        try:
            conn = psycopg2.connect("dbname=test user=postgres password=secret")
            cursor = conn.cursor()
            
            # Example SQL query with parameterized query to prevent SQL injection
            cursor.execute("SELECT * FROM users WHERE email = %s", (self.email,))
            result = cursor.fetchone()
            
            if result:
                raise DataValidationError("Email already in use")
            
            cursor.close()
            conn.close()
        
        except Exception as e:
            raise DataValidationError(f"Database error: {str(e)}")

# Example usage
email_validator = EmailValidator("test@example.com")
email_validator.validate_email()

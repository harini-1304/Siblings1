#!/usr/bin/env python3
"""
Test script to verify SMTP email configuration
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection and email sending"""
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    
    print("=" * 60)
    print("📧 SMTP Configuration Test")
    print("=" * 60)
    print(f"SMTP Server: {smtp_server}")
    print(f"SMTP Port: {smtp_port}")
    print(f"Sender Email: {sender_email}")
    print(f"Password Length: {len(sender_password) if sender_password else 0} chars")
    print()
    
    if not sender_email or not sender_password:
        print("❌ Error: Email credentials not configured in .env")
        return False
    
    try:
        print("🔌 Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("✅ STARTTLS connection successful")
        
        print("🔑 Authenticating with email credentials...")
        server.login(sender_email, sender_password)
        print("✅ Authentication successful")
        
        # Create test email
        print("📝 Creating test email...")
        test_email = "test@psgitech.ac.in"
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = test_email
        msg['Subject'] = 'ProConnect - Test Email'
        
        body = """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>✅ Test Email Successful!</h2>
                <p>This is a test email from ProConnect password reset system.</p>
                <p>If you received this, your SMTP configuration is working correctly.</p>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        print(f"📤 Sending test email to {test_email}...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print()
        print("=" * 60)
        print("✅ All tests passed! Email sending should work.")
        print("=" * 60)
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {str(e)}")
        print("   Check that SENDER_PASSWORD is a valid Gmail app password")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_smtp_connection()
    exit(0 if success else 1)

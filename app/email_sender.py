import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def format_email_body(df_display):
    table_html = df_display.to_html(index=False, escape=False)
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            h2 {{
                color: #2c3e50;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #2c3e50;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h2> Daily Portfolio Performance</h2>
        {table_html}
    </body>
    </html>
    """
    return html

def send_email(content):
    
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    
    
    subject = "Daily Stock Performance"
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    if hasattr(content, "to_html"):
        body = format_email_body(content)
    else:
        body = f"""
        <html>
        <body>
            <p>{content}</p>
        </body>
        </html>
        """
    
    msg.attach(MIMEText(body, "html"))
    
    try: 
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("Email Sent Successfully")
        
    except Exception as e:
        print(f"Email Failed: {e}")
        

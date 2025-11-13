from smtplib import SMTP, SMTPConnectError
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(
        from_addr: str="admin@socialmedia.com", 
        to_addr: List[str]=None,
        msg: str=None,
    ):
    try:
        with SMTP(
                os.environ.get('SMTP_HOST', 'localhost'), 
                os.environ.get('SMTP_PORT', 8025)) as client:
            result = client.sendmail(
                from_addr,
                to_addr,        
                msg
            )
            print("Sendmail result:", result)
    except SMTPConnectError as e:
        print("Connection failed:", e)

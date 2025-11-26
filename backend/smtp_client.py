from smtplib import SMTP, SMTPConnectError
from typing import List
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

def send_email(
        from_addr: Optional[str]="admin@socialmedia.com", 
        to_addr: List[str]=None,
        msg: str=None,
        is_test=False
    ):
    try:
        print(f"================= {is_test}")
        print(f"================= {os.environ.get('SMTP_HOST', 'localhost') if is_test is not True else 'smtpd'}")
        with SMTP(
                os.environ.get('SMTP_HOST', 'localhost') if is_test==True else 'smtpd',
                os.environ.get('SMTP_PORT', 8025)) as client:
            result = client.sendmail(
                from_addr,
                to_addr,        
                msg
            )
            print("Sendmail result:", result)
            return True
    except SMTPConnectError as e:
        print("Connection failed:", e)
        return False


if __name__ == "__main__":
    send_email(
        msg="test",
        to_addr="test@mail.como"
    )
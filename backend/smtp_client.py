import os
from core.settings import COMPANY_EMAIL
from smtplib import SMTP, SMTPConnectError
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


def send_email(
    from_addr: Optional[str] = COMPANY_EMAIL,
    to_addr: List[str] = None,
    msg: str = None,
    is_test=False,
):
    try:
        with SMTP(
            (
                os.environ.get("SMTP_HOST", "localhost")
                if is_test
                else "smtpd"
            ),
            os.environ.get("SMTP_PORT", 8025),
        ) as client:
            result = client.sendmail(from_addr, to_addr, msg)
            print("Sendmail result:", result)
            return True
    except SMTPConnectError as e:
        print("Connection failed:", e)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    send_email(msg="test", to_addr="test@mail.como")

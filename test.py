from smtplib import SMTP, SMTPConnectError

try:
    with SMTP("localhost", 8025) as client:
        result = client.sendmail(
            "a@example.com",
            ["b@example.com"],
            """\
From: Anne Person <anne@example.com>
To: Bart Person <bart@example.com>
Subject: A test
Message-ID: <ant>

Hi Bart, this is Anne.
"""
        )
        print("Sendmail result:", result)
except SMTPConnectError as e:
    print("Connection failed:", e)

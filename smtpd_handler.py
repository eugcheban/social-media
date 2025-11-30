import sys

from aiosmtpd.controller import Controller


class PrintHandler:
    async def handle_DATA(self, server, session, envelope):
        print("=== New message received ===")
        print(envelope.content.decode('utf8', errors='replace'))
        print("=== End of message ===")
        sys.stdout.flush()

        return '250 OK'

if __name__ == "__main__":
    controller = Controller(PrintHandler(), hostname="0.0.0.0", port=8025)
    controller.start()
    import asyncio
    asyncio.get_event_loop().run_forever()

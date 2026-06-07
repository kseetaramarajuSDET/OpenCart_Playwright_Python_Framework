import logging
import os
from datetime import datetime


class LogGen:
    @staticmethod
    def loggen():
        # Create 'logs' directory if it doesn't exist
        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        path = os.path.abspath(f"./logs/automation.log_{datetime.now().strftime('%H-%M')}")

        # Configure the logger
        logging.basicConfig(
            filename=path,
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            encoding='utf-8',
            force=True  # Ensures configuration is applied even if previously set
        )
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger

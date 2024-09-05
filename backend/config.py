import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Change to ERROR or WARNING in production
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Logs to console
            # logging.FileHandler('app.log'),  # Logs to a file
        ]
    )

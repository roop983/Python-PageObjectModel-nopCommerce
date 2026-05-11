import logging
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) # By default pytest may be running from a different working directory. To point to this configuratation directory path, use this code to extract the absolute path.
log_path = os.path.join(base_dir, "..", "logs", "nopcommerce.log")

class Log_maker:
    @staticmethod
    def log_gen():
        logging.basicConfig(filename=log_path, format='%(asctime)s:%(levelname)s:%(message)s',datefmt="%Y-%m-%d %H:%M:%S",force=True)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        return logger




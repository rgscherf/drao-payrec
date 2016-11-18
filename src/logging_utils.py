import logging
import sys


def get_logger():
    log = logging.getLogger("drao-payrec")
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return log


def write_preprocess_log(logger):
    logger.info("================")
    logger.info("Beginning claim processing...")
    logger.info("================")


def write_postprocess_log(logger, processed_users, total_users):
    logger.info("================")
    logger.info("Done processing.")
    logger.info("Processed {0} claims out of {1} read from JSON.".format(
        processed_users, total_users))
    logger.info("================")

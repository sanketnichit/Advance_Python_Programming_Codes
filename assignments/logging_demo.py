"""Python Logging Module Practical

Demonstrates logging levels, formatters, handlers, file rotation, logger
hierarchy, exception logging, filters, lazy formatting, and dictConfig.

Run: python logging_demo.py
All generated log files are saved in a temporary folder.
"""

import logging
import logging.config
import logging.handlers
import os
import sys
import tempfile


LOG_DIR = tempfile.mkdtemp(prefix="python_logging_lab_")


def heading(title):
    """Print a heading before each demonstration."""
    print(f"\n{'=' * 8} {title} {'=' * 8}")


def get_logger(name, level=logging.DEBUG):
    """Return a clean named logger without duplicate handlers."""
    logger = logging.getLogger(name)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    logger.filters.clear()
    logger.setLevel(level)
    logger.propagate = False
    return logger


def close_logger_handlers(*loggers):
    """Remove and close handlers created by a demonstration."""
    for logger in loggers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()


def demo_levels():
    """Show the five logging levels and the effect of a threshold."""
    heading("1. LOGGING LEVELS")
    logger = get_logger("lab.levels")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
    logger.addHandler(handler)

    try:
        print("Logger threshold: DEBUG (all five levels are visible)")
        logger.debug("Detailed information for debugging")
        logger.info("Program is running normally")
        logger.warning("Something unexpected happened")
        logger.error("An operation failed")
        logger.critical("A serious problem may stop the program")

        print("\nChanging threshold to WARNING (DEBUG and INFO are hidden)")
        logger.setLevel(logging.WARNING)
        logger.debug("This DEBUG message is hidden")
        logger.info("This INFO message is hidden")
        logger.warning("This WARNING message is visible")
    finally:
        close_logger_handlers(logger)


def demo_formatter():
    """Display time, logger name, level, function and line number."""
    heading("2. LOG FORMATTER")
    logger = get_logger("lab.formatter", logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | "
        "%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        logger.info("This entry includes time, source and message details")
    finally:
        close_logger_handlers(logger)


def demo_handlers():
    """Send log messages to the console and a file at different levels."""
    heading("3. MULTIPLE HANDLERS")
    log_path = os.path.join(LOG_DIR, "application.log")
    logger = get_logger("lab.handlers")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("CONSOLE %(levelname)s - %(message)s")
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    try:
        logger.debug("Debug message: ignored by both handlers")
        logger.info("Info message: sent to console only")
        logger.warning("Warning message: sent to console and file")
        logger.error("Error message: sent to console and file")
        file_handler.flush()

        print("\nContents of application.log (WARNING and above):")
        with open(log_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                print("FILE", line.rstrip())
    finally:
        close_logger_handlers(logger)


def demo_file_rotation():
    """Rotate a log file after it reaches a small size."""
    heading("4. ROTATING FILE HANDLER")
    log_path = os.path.join(LOG_DIR, "activity.log")
    logger = get_logger("lab.rotation", logging.INFO)
    rotating_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=200,
        backupCount=2,
        encoding="utf-8",
    )
    rotating_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(rotating_handler)

    try:
        for number in range(1, 21):
            logger.info("This is rotating log entry number %02d", number)
        rotating_handler.flush()
    finally:
        close_logger_handlers(logger)

    created_files = sorted(
        name for name in os.listdir(LOG_DIR) if name.startswith("activity.log")
    )
    print("Rotated log files:", created_files)


def demo_logger_hierarchy():
    """Show that child loggers pass records to their parent logger."""
    heading("5. LOGGER HIERARCHY")
    parent_logger = get_logger("shop", logging.INFO)
    parent_handler = logging.StreamHandler(sys.stdout)
    parent_handler.setFormatter(
        logging.Formatter("[%(name)s] %(levelname)s - %(message)s")
    )
    parent_logger.addHandler(parent_handler)

    cart_logger = get_logger("shop.cart", logging.NOTSET)
    payment_logger = get_logger("shop.payment", logging.NOTSET)
    cart_logger.propagate = True
    payment_logger.propagate = True

    try:
        cart_logger.info("Item added to cart")
        payment_logger.info("Payment completed successfully")
        payment_logger.debug("This DEBUG message is hidden by the parent level")
    finally:
        close_logger_handlers(parent_logger, cart_logger, payment_logger)


def demo_exception_logging():
    """Use logger.exception() to include the traceback."""
    heading("6. EXCEPTION LOGGING")
    logger = get_logger("lab.exceptions", logging.ERROR)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(handler)

    try:
        try:
            result = 10 / 0
            print(result)  # This line is not reached.
        except ZeroDivisionError:
            logger.exception("The calculation could not be completed")
    finally:
        close_logger_handlers(logger)


class HideSensitiveWords(logging.Filter):
    """Reject log records containing the word 'password'."""

    def filter(self, record):
        return "password" not in record.getMessage().lower()


def demo_filter():
    """Demonstrate a filter that blocks selected messages."""
    heading("7. LOGGING FILTER")
    logger = get_logger("lab.filter", logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    handler.addFilter(HideSensitiveWords())
    logger.addHandler(handler)

    try:
        logger.info("Student signed in successfully")
        logger.info("Password information must not be written to the log")
        logger.info("Student opened the dashboard")
        print("The message containing the blocked word was not displayed.")
    finally:
        close_logger_handlers(logger)


def demo_lazy_formatting_and_extra():
    """Use deferred percent formatting and custom record attributes."""
    heading("8. LAZY FORMATTING AND EXTRA FIELDS")
    logger = get_logger("lab.orders", logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(levelname)s | user=%(user)s | %(message)s")
    )
    logger.addHandler(handler)

    try:
        logger.info(
            "Order %d placed, total Rs. %.2f",
            42,
            1999.50,
            extra={"user": "student"},
        )
    finally:
        close_logger_handlers(logger)


def demo_dictionary_configuration():
    """Configure a logger and handler using logging.config.dictConfig."""
    heading("9. DICTIONARY CONFIGURATION")
    configuration = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(levelname)s | %(name)s | %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "lab.configured": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(configuration)
    logger = logging.getLogger("lab.configured")
    logger.info("This logger was configured using one dictionary")

    close_logger_handlers(logger)


def main():
    """Run all logging demonstrations in order."""
    print("PYTHON LOGGING MODULE PRACTICAL")
    print("Log files will be saved in:", LOG_DIR)

    demo_levels()
    demo_formatter()
    demo_handlers()
    demo_file_rotation()
    demo_logger_hierarchy()
    demo_exception_logging()
    demo_filter()
    demo_lazy_formatting_and_extra()
    demo_dictionary_configuration()

    print("\nConclusion: Logging records program events with levels and timestamps.")
    print("Handlers choose where records go, formatters control their appearance,")
    print("and filters decide which records should be kept.")
    print("\nLog output folder:", LOG_DIR)


if __name__ == "__main__":
    main()

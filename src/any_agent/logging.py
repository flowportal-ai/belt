import logging
from rich.logging import RichHandler

logger = logging.getLogger("flow_portal")
logger.setLevel(logging.DEBUG)
logger.addHandler(RichHandler(rich_tracebacks=True))

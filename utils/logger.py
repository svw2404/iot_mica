
---

### **utils/logger.py**

```python
import logging
import sys

def get_logger(name: str = "IoTARP") -> logging.Logger:
    """Return a single-instance console logger."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        "%H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

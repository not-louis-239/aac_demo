import traceback
from datetime import datetime

from sunrise.core.paths import LOGS_DIR

ERR_LOG_FILE = LOGS_DIR / "err.log"

def write_error_log(err: Exception) -> None:
    date_str = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
    err_str = traceback.format_exc()

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(ERR_LOG_FILE, 'a', encoding='utf-8') as err_log:
        err_log.write(f"Error at {date_str}\n\n{err_str}\n")

def _test():
    try:
        raise TypeError("Test error")
    except TypeError as exc:
        write_error_log(exc)

if __name__ == "__main__":
    _test()

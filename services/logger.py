from datetime import datetime
import pandas as pd
from config import config_manager, paths


def log(message: str, df: pd.DataFrame | None = None) -> None:
    """Append a log entry if logging is enabled in the configuration."""
    config = config_manager.load_config()
    if not config.get("logging_on"):
        return

    paths.LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = paths.LOG_DIR / f"{datetime.now().strftime('%Y%m%d')}.txt"

    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {message}\n")
        if isinstance(df, pd.DataFrame):
            f.write(df.to_string())
            f.write("\n")

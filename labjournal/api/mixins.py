from datetime import datetime

class LoggingMixin:
    def log_action(self, action):
        print(f"{action} action performed at {datetime.now()}")
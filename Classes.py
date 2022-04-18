import datetime

class Contact:
    def __init__(self, name: str, status: int, timestamp: datetime.datetime):
        self.name = name
        self.status = status
        self.timestamp = timestamp
        self.duration = 0

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> int:
        return self.status

    def get_timestamp(self) -> datetime.datetime:
        return self.timestamp

    def get_duration(self) -> int:
        return self.duration

    def set_status(self, status: int):
        self.status = status

    def set_timestamp(self, timestamp: datetime.datetime):
        self.timestamp = timestamp

    def set_duration(self, duration: int):
        self.duration = duration

    def __call__(self, *args, **kwargs):
        return f"{self.name}\t{self.status}\t{self.duration}\t{self.timestamp.strftime('%H:%M:%S, %m/%d/%Y')}"

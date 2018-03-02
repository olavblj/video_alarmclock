import enum


class SystemState(enum.Enum):
    IDLE = 0
    SETTING_ALARM = 1
    WAITING_ALARM = 2
    RUNNING_ALARM = 3

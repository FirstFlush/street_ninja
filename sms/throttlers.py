from rest_framework.throttling import AnonRateThrottle


class ChatMinuteThrottle(AnonRateThrottle):
    rate = "20/min"

class ChatHourThrottle(AnonRateThrottle):
    rate = "100/hour"

class ChatDayThrottle(AnonRateThrottle):
    rate = "500/day"
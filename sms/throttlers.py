from rest_framework.throttling import AnonRateThrottle


class ChatMinuteThrottle(AnonRateThrottle):
    rate = "60/min"

class ChatHourThrottle(AnonRateThrottle):
    rate = "3600/hour"

class ChatDayThrottle(AnonRateThrottle):
    rate = "10000/day"
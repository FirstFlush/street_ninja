from .enums import SMSFollowUpKeywordEnum

class FollowUpProcessingService:

    def __init__(self, msg: str, follow_up_keyword: SMSFollowUpKeywordEnum):
        self.msg = msg
        self.follow_up_keyword = follow_up_keyword

    
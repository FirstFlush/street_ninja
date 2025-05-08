from sms.enums import SMSFollowUpKeywordEnum, FollowUpParams
from ..test_schemas import FollowUpSample

FOLLOWUP_INQUIRIES = [
    FollowUpSample(message="more", location=None, follow_up_enum=SMSFollowUpKeywordEnum.MORE),
    FollowUpSample(message="MORE", location=None, follow_up_enum=SMSFollowUpKeywordEnum.MORE),
    FollowUpSample(message="mOrE", location=None, follow_up_enum=SMSFollowUpKeywordEnum.MORE),

    FollowUpSample(message="info 1", location=None, follow_up_enum=SMSFollowUpKeywordEnum.INFO, params={FollowUpParams.SELECTION.value: 1}),
    FollowUpSample(message="2 INFO", location=None, follow_up_enum=SMSFollowUpKeywordEnum.INFO, params={FollowUpParams.SELECTION.value: 2}),
    FollowUpSample(message="3  info", location=None, follow_up_enum=SMSFollowUpKeywordEnum.INFO, params={FollowUpParams.SELECTION.value: 3}),
    FollowUpSample(message="info 4", location=None, follow_up_enum=SMSFollowUpKeywordEnum.INFO, params={FollowUpParams.SELECTION.value: 4}),

    FollowUpSample(message="directions  1", location=None, follow_up_enum=SMSFollowUpKeywordEnum.DIRECTIONS, params={FollowUpParams.SELECTION.value: 1}),
    FollowUpSample(message="DIRECTIONS 2", location=None, follow_up_enum=SMSFollowUpKeywordEnum.DIRECTIONS, params={FollowUpParams.SELECTION.value: 2}),
    FollowUpSample(message="3 directions", location=None, follow_up_enum=SMSFollowUpKeywordEnum.DIRECTIONS, params={FollowUpParams.SELECTION.value: 3}),
    FollowUpSample(message="14 directions", location=None, follow_up_enum=SMSFollowUpKeywordEnum.DIRECTIONS, params={FollowUpParams.SELECTION.value: 14}),
]

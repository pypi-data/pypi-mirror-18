from .internals import badges
from .base import Badge, BadgeDetail, BadgeAwarded  # NOQA

default_app_config = 'awards.apps.AwardsConfig'


possibly_award_badge = badges.possibly_award_badge

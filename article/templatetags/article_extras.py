from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def rate_active(user, table_type, table_id, vote):
    if (user.is_authenticated()):
        try:
            user.rate_set.get(
                rate_table_type=table_type,
                rate_table_id=table_id,
                rate_vote=int(vote)
            )
            return 'active'
        except ObjectDoesNotExist:
            return None
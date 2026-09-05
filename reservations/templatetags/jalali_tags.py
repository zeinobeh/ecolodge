import jdatetime
from django import template

register = template.Library()


@register.filter
def jalali_date(value):
    if not value:
        return ""

    jalali = jdatetime.date.fromgregorian(date=value)

    return jalali.strftime("%Y/%m/%d")
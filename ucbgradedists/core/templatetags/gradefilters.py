from django import template

register = template.Library()

@register.filter(name='lettergrade')
def lettergrade(value):
    """Maps grade point average to letter grade."""
    if value > 3.7:
        return 'A-'
    elif value > 3.3:
        return 'B+'
    elif value > 3:
        return 'B'
    elif value > 2.7:
        return 'B-'
    elif value > 2.3:
        return 'C+'
    elif value > 2:
        return 'C'
    elif value > 1.7:
        return 'C-'
    elif value > 1.3:
        return 'D+'
    elif value > 1:
        return 'D'
    elif value > 0.7:
        return 'D-'
    else:
        return 'F'

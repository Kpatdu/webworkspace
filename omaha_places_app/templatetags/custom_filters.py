from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    '''
    Function to get the element at a specific index in a sequence.
    '''
    
    try:
        return sequence[position]
    except:
        return None
    
@register.filter
def to(value, arg):
    """
    Usage: {% for i in 1|to:16 %}
    Loops from 1 to 15 (arg not included)
    """
    return range(value, arg)


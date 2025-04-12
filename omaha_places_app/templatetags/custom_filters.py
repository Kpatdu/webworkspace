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

from django import template
import os

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.simple_tag
def is_vercel_demo():
    """Template tag to check if running on Vercel"""
    return 'VERCEL' in os.environ

@register.inclusion_tag('Inventario/demo_warning.html')
def demo_warning(action="modificar"):
    """Include a demo warning banner for Vercel users"""
    return {
        'is_demo': 'VERCEL' in os.environ,
        'action': action
    }

from django import template

register = template.Library()

@register.filter
def custom_yesno(value):
    if value=="Виявлено" or value=="Дозволено":
        return "✔"
    elif value=='Не виявлено':
        return "✘"
    else:
        return value
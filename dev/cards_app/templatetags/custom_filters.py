from django import template

register = template.Library()

@register.filter
def custom_yesno(value):
    if value=="Виявлено" or value=="Дозволено":
        return "✔"
    elif value=='Не виявлено' or value=="Заборонено":
        return "✘"
    elif value==None:
        return ""
    else:
        return value
    

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})
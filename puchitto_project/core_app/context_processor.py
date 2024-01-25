from core_app.models import *

def default(rq):
    categories=Category.objects.all()
    return{
        'categories':categories
    }
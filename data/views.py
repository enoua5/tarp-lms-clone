from datetime import datetime, time, date
from json import dumps, JSONEncoder
from django.forms.models import model_to_dict
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# import ALL THE MODELS!!!
from course_management.models import Assignment, Course
from account.models import Profile


class DatabaseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime) or isinstance(obj, time) or isinstance(obj, date):
            return str(obj)
        if isinstance(obj, Model):
            return obj.id
        if isinstance(obj, ImageFieldFile):
            return str(obj)
        return JSONEncoder.default(self, obj)

def queryset_to_list(qs, fields=None, exclude=None):
    arr = []
    for i in qs:
        arr.append(model_to_dict(i, fields=fields, exclude=exclude))
    return arr

ITEM_MODELS = {
    'course': {'model':Course, 'permission': "course_management.view_course"},
    'assignment': {'model':Assignment, 'permission': "course_management.view_assignment"},
    'profile': {'model':Profile, 'permission': "course_management.view_profile"},

}


def get_all(req, query_dict):
    if not req.user.is_authenticated:
        return HttpResponse('{"message": "You are not logged in"}', status=401)

    item_type = query_dict.get('item_type')

    if(item_type == None):
        return HttpResponse('{"message": "Item type not specified"}', status=400)

    item_model = ITEM_MODELS.get(item_type)['model']

    if(item_model == None):
        return HttpResponse('{"message":"Item type not recognized"}', status=404)

    if not req.user.has_perm(ITEM_MODELS.get(item_type)['permission']):
        return HttpResponse('{"message": "You do not have permission to view that item"}', status=403)


    items = item_model.objects.all()

    data = {
        'items': queryset_to_list(items)
    }

    return HttpResponse(dumps(data, cls=DatabaseEncoder))

QUERY_COMMANDS = {
    'get_all': get_all 
}

# Create your views here.

def basic_query(req):
    query_dict = req.GET
    command = query_dict.get('command')

    if(command == None):
        return HttpResponse('{"message":"Command not specified"}', status=400)

    command_handler = QUERY_COMMANDS.get(command)

    if(command_handler == None):
        return HttpResponse('{"message":"Unrecognized command"}', status=400)

    return command_handler(req, query_dict)


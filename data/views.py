""" See `QUERY_COMMANDS` to find a list of accepted commands and the functions that handle them. """

from datetime import datetime, time, date
from http import HTTPStatus
from json import dumps, JSONEncoder
from django.forms.models import model_to_dict
from django.db.models import Model, Q
from django.db.models.fields.files import ImageFieldFile
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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

def ItemQueryDesc(model, permission, only_mine=True, user_fields=[]):
    return {
        'model': model,
        'permission': permission,
        'only_mine': only_mine,
        'user_fields': user_fields,
    }

ITEM_MODELS = {
    'course': ItemQueryDesc(Course, "course_management.view_course", only_mine=False, user_fields=["instructor_id", "students"]),
    'assignment': ItemQueryDesc(Assignment, "course_management.view_assignment", user_fields=["course__instructor_id", "course__students"]),
    'profile': ItemQueryDesc(Profile, "account.view_profile", user_fields=["user"]),

}

def get_all(req, query_dict):
    if not req.user.is_authenticated:
        return JsonResponse({"message": "You are not logged in"}, status=HTTPStatus.UNAUTHORIZED)

    item_type = query_dict.get('item_type')

    if(item_type == None):
        return JsonResponse({"message": "Item type not specified"}, status=HTTPStatus.BAD_REQUEST)

    item_query_desc = ITEM_MODELS.get(item_type)

    if(item_query_desc == None):
        return JsonResponse({"message":"Item type not recognized"}, status=HTTPStatus.NOT_FOUND)

    if item_query_desc["only_mine"]:
        return JsonResponse({"message": "You can only get your own data from this list"}, status=HTTPStatus.FORBIDDEN)

    item_model = item_query_desc['model']

    if not req.user.has_perm(ITEM_MODELS.get(item_type)['permission']):
        return JsonResponse({"message": "You do not have permission to view that item"}, status=HTTPStatus.FORBIDDEN)


    items = item_model.objects.all()

    data = {
        'items': queryset_to_list(items)
    }

    return JsonResponse(data, encoder=DatabaseEncoder)

def get_mine(req, query_dict):
    if not req.user.is_authenticated:
        return JsonResponse({"message": "You are not logged in"}, status=HTTPStatus.UNAUTHORIZED)

    item_type = query_dict.get('item_type')

    if(item_type == None):
        return JsonResponse({"message": "Item type not specified"}, status=HTTPStatus.BAD_REQUEST)

    item_query_desc = ITEM_MODELS.get(item_type)

    if(item_query_desc == None):
        return JsonResponse({"message":"Item type not recognized"}, status=HTTPStatus.NOT_FOUND)

    item_model = item_query_desc['model']

    if not req.user.has_perm(ITEM_MODELS.get(item_type)['permission']):
        return JsonResponse({"message": "You do not have permission to view that item"}, status=HTTPStatus.FORBIDDEN)

    search_params = Q()


    for field in item_query_desc["user_fields"]:
        keyword = {}
        keyword[field] = req.user.id
        search_params |= Q(**keyword)
        
    items = item_model.objects.filter(search_params).distinct()

    data = {
        'items': queryset_to_list(items)
    }

    return JsonResponse(data, encoder=DatabaseEncoder)

def brew_coffee():
    return JsonResponse({"message": "Tip me over and pour me out!"}, status=HTTPStatus.IM_A_TEAPOT)

QUERY_COMMANDS = {
    'get_all': get_all,
    'get_mine': get_mine,
}

# Create your views here.

@csrf_exempt
def basic_query(req):
    if req.method == 'BREW':
        return brew_coffee()

    query_dict = req.GET
    command = query_dict.get('command')

    if(command == None):
        return JsonResponse({"message":"Command not specified"}, status=HTTPStatus.BAD_REQUEST)

    command_handler = QUERY_COMMANDS.get(command)

    if(command_handler == None):
        return JsonResponse({"message":"Unrecognized command"}, status=HTTPStatus.BAD_REQUEST)

    return command_handler(req, query_dict)


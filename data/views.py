""" See `QUERY_COMMANDS` to find a list of accepted commands and the functions that handle them. """

from datetime import datetime, time, date
from http import HTTPStatus
from json import dumps, JSONEncoder

from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Model, Q, F
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# import ALL THE MODELS!!!
from course_management.models import Assignment, Course
from account.models import Profile
from dashboard.models import Notification


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

def ItemQueryDesc(model, permission, only_mine=True, user_fields=[], annotations={}, allow_delete=False):
    return {
        'model': model,
        'permission': permission,
        'only_mine': only_mine,
        'user_fields': user_fields,
        'annotations': annotations,
        'allow_delete': allow_delete,
    }

ITEM_MODELS = {
    'course': ItemQueryDesc(Course, "course_management.view_course", only_mine=False, user_fields=["instructor_id", "students"]),
    'assignment': ItemQueryDesc(Assignment, "course_management.view_assignment", user_fields=["course__instructor_id", "course__students"]),
    'profile': ItemQueryDesc(Profile, "account.view_profile", user_fields=["user"]),
    'notification': ItemQueryDesc(Notification, None, user_fields=["notified_user"], allow_delete=["notified_user_id"], annotations={'course_name':F("course__course_name"), 'course_department':F("course__department"), 'course_num': F("course__course_num"),'assignment_name':F("assignment__title")}),
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

    perm = ITEM_MODELS.get(item_type)['permission']
    if not req.user.has_perm(perm) and perm is not None:
        return JsonResponse({"message": "You do not have permission to view that item"}, status=HTTPStatus.FORBIDDEN)


    items = item_model.objects.all().annotate(**item_query_desc['annotations']).values()

    # data = {
    #     'items': serializers.serialize('json', items)
    # }

    return JsonResponse({'items':list(items)},safe=False)

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

    perm = ITEM_MODELS.get(item_type)['permission']
    if not req.user.has_perm(perm) and perm is not None:
        return JsonResponse({"message": "You do not have permission to view that item"}, status=HTTPStatus.FORBIDDEN)

    search_params = Q()


    for field in item_query_desc["user_fields"]:
        keyword = {}
        keyword[field] = req.user.id
        search_params |= Q(**keyword)
        
    items = item_model.objects.filter(search_params).distinct().annotate(**item_query_desc['annotations']).values()

    print(items)

    # data = {
    #     'items': serializers.serialize('json', items)
    # }

    return JsonResponse({'items': list(items)}, encoder=DatabaseEncoder)

def delete_by_id(req, query_dict):
    if not req.user.is_authenticated:
        return HttpResponse('{"message": "You are not logged in"}', status=HTTPStatus.UNAUTHORIZED)

    item_type = query_dict.get('item_type')

    if(item_type == None):
        return HttpResponse('{"message": "Item type not specified"}', status=HTTPStatus.BAD_REQUEST)

    item_query_desc = ITEM_MODELS.get(item_type)

    if(item_query_desc == None):
        return HttpResponse('{"message":"Item type not recognized"}', status=HTTPStatus.NOT_FOUND)

    item_id = query_dict.get('id')
    if(item_id == None):
        return HttpResponse('{"message": "Item id not specified"}', status=HTTPStatus.BAD_REQUEST)

    item_model = item_query_desc['model']

    perm = ITEM_MODELS.get(item_type)['permission']
    if not req.user.has_perm(perm) and perm is not None:
        return HttpResponse('{"message": "You do not have permission to view that item"}', status=HTTPStatus.FORBIDDEN)

    try:
        item = item_model.objects.get(id=item_id)
    except(Exception):
        return HttpResponse('{"message": "No item by that id found"}', status=HTTPStatus.NOT_FOUND)
        
    allowed = False
    if ITEM_MODELS.get(item_type)['allow_delete']:
        for field in ITEM_MODELS.get(item_type)['allow_delete']:
            if item.__dict__.get(field) == req.user.id:
                allowed = True
                break
    
    if not allowed:
        return HttpResponse('{"message": "You do not have permission to delete that item"}', status=HTTPStatus.FORBIDDEN)

    item.delete()

    return HttpResponse('{"message":"Deletion success"}', status=HTTPStatus.ACCEPTED)

def delete_all(req, query_dict):
    if not req.user.is_authenticated:
        return HttpResponse('{"message": "You are not logged in"}', status=HTTPStatus.UNAUTHORIZED)

    item_type = query_dict.get('item_type')

    if(item_type == None):
        return HttpResponse('{"message": "Item type not specified"}', status=HTTPStatus.BAD_REQUEST)

    item_query_desc = ITEM_MODELS.get(item_type)

    if(item_query_desc == None):
        return HttpResponse('{"message":"Item type not recognized"}', status=HTTPStatus.NOT_FOUND)

    item_model = item_query_desc['model']

    perm = ITEM_MODELS.get(item_type)['permission']
    if not req.user.has_perm(perm) and perm is not None:
        return HttpResponse('{"message": "You do not have permission to view that item"}', status=HTTPStatus.FORBIDDEN)

        
    allowed = False
    if not ITEM_MODELS.get(item_type)['allow_delete']:
        return HttpResponse('{"message": "You do not have permission to delete that item"}', status=HTTPStatus.FORBIDDEN)

    search_params = Q()

    for field in item_query_desc["user_fields"]:
        keyword = {}
        keyword[field] = req.user.id
        search_params |= Q(**keyword)
        
    items = item_model.objects.filter(search_params).distinct().all()
    
    for item in items:
        item.delete()

    return HttpResponse('{"message":"Deletion success"}', status=HTTPStatus.ACCEPTED)

def brew_coffee():
    return JsonResponse({"message": "Tip me over and pour me out!"}, status=HTTPStatus.IM_A_TEAPOT)

QUERY_COMMANDS = {
    'get_all': get_all,
    'get_mine': get_mine,
    'delete': delete_by_id,
    'delete_all': delete_all,
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


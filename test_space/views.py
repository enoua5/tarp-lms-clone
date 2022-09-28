from django.shortcuts import render
from . import urls

# Create your views here.

def index(req):
    ctx = {
        'urls': urls.urlpatterns
    }
    print(ctx["urls"][0].name)
    return render(req, 'tests/index.html', ctx)

def template(req):
    return render(req, 'tests/template.html')

def accounttype(req):
    ctx = {
        'isStudent': req.user.groups.filter(name="Student").exists(),
        'isInstructor': req.user.groups.filter(name="Instructor").exists(),
    }

    return render(req, 'tests/accounttype.html', ctx)
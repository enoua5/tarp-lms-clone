from django.shortcuts import render
from .forms import ProfileForm


# Create your views here.
def test(req):
    return render(req, 'main/test.html', {})


def profile(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(req, 'main/profile.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ProfileForm()
    return render(req, 'main/profile.html', {'form': form})

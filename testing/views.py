from django.forms.fields import CharField
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms

# Create your views here.

class NewTaskForm (forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(min_value=1, max_value=3, label="Priority")


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "testing/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("testing:index"))
        else:
            return render(request, "testing/add.html", {
                "form": form
            })
    return render(request, "testing/add.html", {
        "form": NewTaskForm()
    })
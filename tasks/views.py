from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import forms

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {"tasks": request.session["tasks"]})

def add(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        form = forms.AddTaskForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data

            if form["priority"].capitalize() not in ["Low", "Medium", "High"]:
               return render(request, "tasks/add.html", 
                    {"tasks": request.session["tasks"], 
                     "form": forms.AddTaskForm(), 
                     "error": f'Error: "{form["priority"]}" is not a valid priority.',
                    })
            
            task_exists = False

            for task in request.session["tasks"]:
                if task["name"] == form["name"].capitalize():
                    task_exists = True

            if not task_exists: 
                request.session["tasks"].append({
                    "name": form["name"].capitalize(),
                    "description": form["description"].capitalize(),
                    "priority": form["priority"].capitalize(),
                })          

                request.session.modified = True

                return HttpResponseRedirect(reverse("tasks:index"))
            
            else:
               return render(request, "tasks/add.html", 
                    {"tasks": request.session["tasks"], 
                     "form": forms.AddTaskForm(), 
                     "error": f'Error: Task "{form["name"].capitalize()}" already exists.',
                    })
    
    return render(request, "tasks/add.html", {"tasks": request.session["tasks"], "form": forms.AddTaskForm()})

def remove(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        form = forms.RemoveTaskForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data

            task_exists = False

            for task in request.session["tasks"]:
                if task["name"] == form["name"].capitalize():
                    task_exists = True

            if task_exists:
                for i in range(len(request.session["tasks"])):
                    if request.session["tasks"][i]["name"] == form["name"].capitalize():
                        request.session["tasks"].pop(i)
                        break

                request.session.modified = True

                return HttpResponseRedirect(reverse("tasks:index"))   

            else:
               return render(request, "tasks/remove.html", 
                    {"tasks": request.session["tasks"], 
                     "form": forms.RemoveTaskForm(), 
                     "error": f'Error: Task "{form["name"].capitalize()}" does not exist.',
                    })

    if request.session["tasks"]:           
        return render(request, "tasks/remove.html", {"form": forms.RemoveTaskForm()})
    
    else:
        return HttpResponseRedirect(reverse("tasks:index"))
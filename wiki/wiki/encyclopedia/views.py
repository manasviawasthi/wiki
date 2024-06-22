from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
markdowner=markdown2.Markdown()

class NewSearchForm(forms.Form):
    searched=forms.CharField(label="Search Encyclopedia")

all_entries=util.list_entries()
error1="FILE DOES NOT EXIST"
error2="FILE ALREADY EXISTS"
error3="ERROR!!!!!"
error4="NO FIELD SHOULD BE EMPTY"

def index(request):
    if request.method == "POST":
        form=NewSearchForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["searched"].strip().lower()
            if title:
                try:           
                    for entry in all_entries:
                        if title in entry.lower():
                            if title==entry.lower():
                                return HttpResponseRedirect(reverse('title',kwargs={"title":title,"form":NewSearchForm}))
                            else:
                                return render(request,"encyclopedia/search.html",{"title":title,"entry":entry,"form":NewSearchForm})
                    return HttpResponseRedirect(reverse('error',kwargs={"error":error1}))             
                except FileNotFoundError:
                    return HttpResponseRedirect(reverse('error',kwargs={"error":error1}))                

        else:
            return render(request, "encyclopedia/index.html", { "entries": util.list_entries(),"form":form})
            
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":NewSearchForm
    })

def title(request,title):
    return render(request,"encyclopedia/title.html",{"title":title,"content":markdowner.convert(util.get_entry(title)),"form":NewSearchForm})

def save(request):
    if request.method == "POST":
        title=request.POST.get('title')
        content=request.POST.get('content')
        if title != "" and content != "":
            if title in [entry.lower() for entry in all_entries]:
                 return HttpResponseRedirect(reverse('error',kwargs={"error":error2}))
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('error',kwargs={"error":error4}))
    else:
        return render(request,"encyclopedia/save_entry.html",{"form":NewSearchForm})
    
def error(request,error):
    return render(request,"encyclopedia/error.html",{"error":error,"form":NewSearchForm})
 
def randompage(request):
    title=random.choice(all_entries)
    return HttpResponseRedirect(reverse('title',kwargs={"title":title}))
    
def edit(request,title):
    content=util.get_entry(title)
    if request.method=="POST":
        content=request.POST.get('content')
        title=request.POST.get('title')
        if title != "" and content != "":
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('title',kwargs={"title":title}))
        else:
            return HttpResponseRedirect(reverse('error',kwargs={"error":error4}))
        
        
    
    return render(request,"encyclopedia/edit.html",{"title":title,"content":content,"form":NewSearchForm})
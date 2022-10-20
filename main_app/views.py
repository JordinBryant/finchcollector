from pyexpat import model
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request,'finches/index.html', { 'finches': finches})

# update this view function
def finches_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()

  # displaying unassociated toys
  toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))

  return render(request, 'finches/detail.html', {
    # include the finch and feeding_form in the context
    'finch': finch,
    'feeding_form': feeding_form,
    'toys' : toys_finch_doesnt_have,
  })

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
   Finch.objects.get(id=finch_id).toys.add(toy_id)
   return redirect('detail', finch_id=finch_id)

class FinchCreate(CreateView):
    model = Finch
    fields = ['name','breed','description','age']
    # success_url = '/finches/' 

class finchUpdate(UpdateView):
    model = Finch
    fields = ('name','breed', 'description', 'age')

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'

class ToyCreate(CreateView):
    model = Toy
    fields = ('name', 'color')

class ToyUpdate(UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'
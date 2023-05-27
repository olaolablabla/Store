from django.shortcuts import render
from .forms import ExampleForm

# Create your views here.

def form_example (request):
      # return render(request, 'form_example.html')
    for name in request.POST:
        print("{}: {}".format(name, request.POST.getlist(name)))
    return render(request, "form-example.html", {"method": request.method})


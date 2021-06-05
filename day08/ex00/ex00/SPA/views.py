from . import models
from django.http.response import HttpResponse
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from .forms import ImageForm

# Create your views here.

class Image_show(ListView, FormView):
    model = models.ImageModel
    template_name = "index.html"
    form_class = ImageForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form: ImageForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)

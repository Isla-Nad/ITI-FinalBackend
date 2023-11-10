
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView,UpdateView,CreateView,DeleteView
from medical_history.models import MedicalHistory
from medical_history.forms import Medical

# Create your views here.
def admin(request):
    Medical_count = MedicalHistory.objects.count()
    return render(request,'admin.html',context={"medical_count":Medical_count})

def ViewMedicalHistory(request):
    medical = MedicalHistory.objects.all()
    return render(request,'medical_history/allmedical.html',context={'medical':medical})
# def seletectedMicalHistory(request,id):
#     selected = get_object_or_404(MedicalHistory, pk=id)
#     return render(request, 'medical_history/view_medical.html',context={'selected':selected})

class MedicalDetailView(DetailView):
    model = MedicalHistory
    template_name = 'medical_history/view_medical.html'
    context_object_name = 'selected'
class MedicalUpdateView(UpdateView):
    model = MedicalHistory
    form_class =  Medical
    template_name = 'medical_history/update_medical.html'
    success_url = reverse_lazy('allmedical') 
class MedicalCreateView(CreateView):
    model = MedicalHistory
    form_class = Medical
    template_name = 'medical_history/update_medical.html'
    success_url = reverse_lazy('allmedical')
class MedicalDeleteView(DeleteView):
    model = MedicalHistory
    template_name = 'medical_history/confirm_delete.html'
    success_url = reverse_lazy('allmedical')  




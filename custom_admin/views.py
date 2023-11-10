
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView,UpdateView,CreateView,DeleteView,ListView
from medical_history.models import MedicalHistory
from medical_history.forms import Medical,MedicalUpdate
from posts.models import Post


# Create your views here.
def admin(request):
    Medical_count = MedicalHistory.objects.count()
    posts_count = Post.objects.count()
    return render(request,'admin.html',context={"medical_count":Medical_count,"postscount":posts_count})

def ViewMedicalHistory(request):
    medical = MedicalHistory.objects.all()
    return render(request,'medical_history/allmedical.html',context={'medical':medical})

class MedicalDetailView(DetailView):
    model = MedicalHistory
    template_name = 'medical_history/view_medical.html'
    context_object_name = 'selected'

class MedicalUpdateView(UpdateView):
    model = MedicalHistory
    form_class = MedicalUpdate
    template_name = 'medical_history/update_medical.html'
    success_url = reverse_lazy('allmedical') 
    
class MedicalCreateView(CreateView):
    model = MedicalHistory
    form_class = Medical
    template_name = 'medical_history/create.html'
    success_url = reverse_lazy('allmedical')
class MedicalDeleteView(DeleteView):
    model = MedicalHistory
    template_name = 'medical_history/confirm_delete.html'
    success_url = reverse_lazy('allmedical')  


# posts in the admin panel  
class PostsListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/postslist.html'

class PostDetialView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/postdetial.html'

class PostCreateView(CreateView):
    model = Post
    template_name ='posts/createpost.html'
    fields = '__all__'
    success_url = reverse_lazy('postslist')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('postslist')  
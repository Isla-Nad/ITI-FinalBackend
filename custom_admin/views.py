
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from medical_history.models import MedicalHistory
from medical_history.forms import Medical,MedicalUpdate
from community.models import Post
from clinics.models import Clinic,ClinicImages,Cases
from community.models import Review


# Create your views here.
def admin(request):
    Medical_count = MedicalHistory.objects.count()
    posts_count = Post.objects.count()
    reviews_count = Review.objects.count()
    clinics_count = Clinic.objects.count()
    clinics_cases_count = Cases.objects.count()
    clinics_images_count = ClinicImages.objects.count()
    return render(request,'admin.html',context={"medical_count":Medical_count,"reviewcount":reviews_count,"postscount":posts_count,"clinicscount":clinics_count,"cliniccasesscount":clinics_cases_count,"clinicimagescount":clinics_images_count})

def ViewMedicalHistory(request):
    medical = MedicalHistory.objects.all()
    return render(request, 'medical_history/allmedical.html', context={'medical': medical})


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
    template_name = 'posts/createpost.html'
    fields = '__all__'
    success_url = reverse_lazy('postslist')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('postslist')


# Clinics in the admin panel

def get_all_clinics(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinics/clinics_list.html', {'clinics': clinics})


class ClinicCreateView(CreateView):
    model = Clinic
    template_name = 'clinics/create_clinic.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_list')


class ClinicDeleteView(DeleteView):
    model = Clinic
    template_name = 'clinics/confirm_delete.html'
    success_url = reverse_lazy('clinics_list')


class ClinicUpdateView(UpdateView):
    model = Clinic
    template_name = 'clinics/edit_clinic.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_list')


# Clinic Cases in the admin panel
def get_all_clinic_cases(request):
    cases = Cases.objects.all()
    return render(request, 'clinicscases/cases_list.html', {'cases': cases})


class ClinicCaseCreateView(CreateView):
    model = Cases
    template_name = 'clinicscases/create_clinic_case.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_cases_list')


class ClinicCaseDeleteView(DeleteView):
    model = Cases
    template_name = 'clinicscases/confirm_delete.html'
    success_url = reverse_lazy('clinics_cases_list')


class ClinicCaseUpdateView(UpdateView):
    model = Cases
    template_name = 'clinicscases/edit_clinic_case.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_cases_list')


# Clinic Images in the admin panel
def get_all_clinic_images(request):
    clinicimages = ClinicImages.objects.all()
    return render(request, 'clinicsimages/images_list.html', {'clinicimages': clinicimages})


class ClinicImageCreateView(CreateView):
    model = ClinicImages
    template_name = 'clinicsimages/create_clinic_images.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_images_list')


class ClinicImageDeleteView(DeleteView):
    model = ClinicImages
    template_name = 'clinicsimages/confirm_delete.html'
    success_url = reverse_lazy('clinics_images_list')


class ClinicImagesUpdateView(UpdateView):
    model = ClinicImages
    template_name = 'clinicsimages/edit_clinic_images.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_images_list') 


class ReviwListView(ListView):
    model = Review
    context_object_name = 'Reviews'
    template_name = 'reviews/reviewlist.html'

class ReviewDetialView(DetailView):
    model = Review
    context_object_name = 'review'
    # extra_context = {'rating':range('review.rating')}
    template_name = 'reviews/reviewdetial.html'

class ReviewCreateView(CreateView):
    model = Review
    fields = '__all__'
    success_url = reverse_lazy('reviewlist')
    template_name ='reviews/reviewcreate.html'

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'reviews/confirm_delete.html'
    success_url = reverse_lazy('reviewlist')  



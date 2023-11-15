
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from medical_history.models import MedicalHistory
from medical_history.forms import Medical, MedicalUpdate
from community.models import Post, Comment
from clinics.models import Clinic, ClinicImages, Cases
from community.models import Review
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


def is_admin(user):
    return user.is_staff


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect(reverse('admin_home'))
            else:
                return render(request, 'login.html', {'error_message': 'This user is not admin.'})
        else:
            return render(request, 'login.html', {'error_message': 'Email or password is incorrect.'})
    else:
        return render(request, 'login.html')


@user_passes_test(is_admin)
def admin(request):
    Medical_count = MedicalHistory.objects.count()
    posts_count = Post.objects.count()
    comments_count = Comment.objects.count()
    reviews_count = Review.objects.count()
    clinics_count = Clinic.objects.count()
    clinics_cases_count = Cases.objects.count()
    clinics_images_count = ClinicImages.objects.count()
    return render(request, 'admin.html', context={"medical_count": Medical_count, "reviewcount": reviews_count, "comments_count": comments_count, "postscount": posts_count, "clinicscount": clinics_count, "cliniccasesscount": clinics_cases_count, "clinicimagescount": clinics_images_count})


@user_passes_test(is_admin)
def ViewMedicalHistory(request):
    medical = MedicalHistory.objects.all()
    return render(request, 'medical_history/allmedical.html', context={'medical': medical})


@method_decorator(user_passes_test(is_admin), name='dispatch')
class MedicalDetailView(DetailView):
    model = MedicalHistory
    template_name = 'medical_history/view_medical.html'
    context_object_name = 'selected'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class MedicalUpdateView(UpdateView):
    model = MedicalHistory
    form_class = MedicalUpdate
    template_name = 'medical_history/update_medical.html'
    success_url = reverse_lazy('allmedical')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class MedicalCreateView(CreateView):
    model = MedicalHistory
    form_class = Medical
    template_name = 'medical_history/create.html'
    success_url = reverse_lazy('allmedical')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class MedicalDeleteView(DeleteView):
    model = MedicalHistory
    template_name = 'medical_history/confirm_delete.html'
    success_url = reverse_lazy('allmedical')


# posts in the admin panel
@method_decorator(user_passes_test(is_admin), name='dispatch')
class PostsListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/postslist.html'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class PostDetialView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/postdetial.html'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/createpost.html'
    fields = '__all__'
    success_url = reverse_lazy('postslist')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('postslist')
# comments*******************************************************


@method_decorator(user_passes_test(is_admin), name='dispatch')
def ViewComments(request):
    comments = Comment.objects.all()
    return render(request, 'comments/commentslist.html', context={'comments': comments})


@method_decorator(user_passes_test(is_admin), name='dispatch')
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'comments/viewcomment.html'
    context_object_name = 'selected'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comments/createcomment.html'
    fields = '__all__'
    success_url = reverse_lazy('commentslist')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comments/confirmdelete.html'
    success_url = reverse_lazy('commentslist')

# ********************************************************************


# Clinics in the admin panel

def get_all_clinics(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinics/clinics_list.html', {'clinics': clinics})


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicCreateView(CreateView):
    model = Clinic
    template_name = 'clinics/create_clinic.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicDeleteView(DeleteView):
    model = Clinic
    template_name = 'clinics/confirm_delete.html'
    success_url = reverse_lazy('clinics_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicUpdateView(UpdateView):
    model = Clinic
    template_name = 'clinics/edit_clinic.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_list')


# Clinic Cases in the admin panel
def get_all_clinic_cases(request):
    cases = Cases.objects.all()
    return render(request, 'clinicscases/cases_list.html', {'cases': cases})


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicCaseCreateView(CreateView):
    model = Cases
    template_name = 'clinicscases/create_clinic_case.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_cases_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicCaseDeleteView(DeleteView):
    model = Cases
    template_name = 'clinicscases/confirm_delete.html'
    success_url = reverse_lazy('clinics_cases_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicCaseUpdateView(UpdateView):
    model = Cases
    template_name = 'clinicscases/edit_clinic_case.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_cases_list')


# Clinic Images in the admin panel
def get_all_clinic_images(request):
    clinicimages = ClinicImages.objects.all()
    return render(request, 'clinicsimages/images_list.html', {'clinicimages': clinicimages})


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicImageCreateView(CreateView):
    model = ClinicImages
    template_name = 'clinicsimages/create_clinic_images.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_images_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicImageDeleteView(DeleteView):
    model = ClinicImages
    template_name = 'clinicsimages/confirm_delete.html'
    success_url = reverse_lazy('clinics_images_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClinicImagesUpdateView(UpdateView):
    model = ClinicImages
    template_name = 'clinicsimages/edit_clinic_images.html'
    fields = '__all__'
    success_url = reverse_lazy('clinics_images_list')


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ReviwListView(ListView):
    model = Review
    context_object_name = 'Reviews'
    template_name = 'reviews/reviewlist.html'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ReviewDetialView(DetailView):
    model = Review
    context_object_name = 'review'
    # extra_context = {'rating':range('review.rating')}
    template_name = 'reviews/reviewdetial.html'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ReviewCreateView(CreateView):
    model = Review
    fields = '__all__'
    success_url = reverse_lazy('reviewlist')
    template_name = 'reviews/reviewcreate.html'


@method_decorator(user_passes_test(is_admin), name='dispatch')
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'reviews/confirm_delete.html'
    success_url = reverse_lazy('reviewlist')

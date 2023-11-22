
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from accounts.models import User, UserProfile
from appointments.models import Appointment
from custom_admin.forms import CasesFormSet, CertificatesFormSet, UserChangeForm, UserForm, UserProfileForm
from medical_history.models import MedicalHistory
from medical_history.forms import Medical, MedicalUpdate
from community.models import Post, Comment
from clinics.models import Clinic, ClinicImages, Cases
from community.models import Review
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def is_admin(user):
    return user.is_staff and user.is_superuser


def is_staff(user):
    return user.is_staff


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect(reverse('admin_home'))
            else:
                return render(request, 'login.html', {'error_message': 'This user is not staff.'})
        else:
            return render(request, 'login.html', {'error_message': 'Email or password is incorrect.'})
    else:
        return render(request, 'login.html')


def admin_logout(request):
    logout(request)
    return redirect(reverse('admin_login'))


@user_passes_test(is_staff)
def admin(request):
    user_count = User.objects.count()
    profile_count = UserProfile.objects.count()
    appointment_count = Appointment.objects.count()
    Medical_count = MedicalHistory.objects.count()
    posts_count = Post.objects.count()
    comments_count = Comment.objects.count()
    reviews_count = Review.objects.count()
    clinics_count = Clinic.objects.count()
    clinics_cases_count = Cases.objects.count()
    clinics_images_count = ClinicImages.objects.count()
    return render(request, 'admin.html', context={'user_count': user_count, 'profile_count': profile_count, 'appointment_count': appointment_count, "medical_count": Medical_count, "reviewcount": reviews_count, "comments_count": comments_count, "postscount": posts_count, "clinicscount": clinics_count, "cliniccasesscount": clinics_cases_count, "clinicimagescount": clinics_images_count})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# users


@user_passes_test(is_staff)
def users_list(request):
    user_list = User.objects.all()
    paginator = Paginator(user_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users/users_list.html', context={'users': users})


@user_passes_test(is_admin)
def user_create(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            return redirect('users_list')
    else:
        user_form = UserForm()
    return render(request, 'users/user_create.html', context={'user_form': user_form})


@user_passes_test(is_admin)
def user_edit(request, id):
    user_to_edit = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserChangeForm(
            request.POST, request.FILES, instance=user_to_edit)
        if user_form.is_valid():
            user_form.save()
            return redirect('users_list')
    else:
        user_form = UserChangeForm(instance=user_to_edit)
    return render(request, 'users/user_edit.html', context={'user_form': user_form, 'user': user_to_edit})


@user_passes_test(is_admin)
def user_delete(request, id):
    user_to_delete = get_object_or_404(User, id=id)
    if user_to_delete == request.user:
        messages.success(request, "You can't delete your self.")
        return redirect('users_list')
    elif request.method == 'POST':
        user_to_delete.delete()
        return redirect('users_list')
    return render(request, 'users/user_delete.html')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# user_profiles


@user_passes_test(is_staff)
def user_profiles_list(request):
    user_profiles_list = UserProfile.objects.all()
    paginator = Paginator(user_profiles_list, 5)
    page = request.GET.get('page')
    try:
        user_profiles = paginator.page(page)
    except PageNotAnInteger:
        user_profiles = paginator.page(1)
    except EmptyPage:
        user_profiles = paginator.page(paginator.num_pages)

    return render(request, 'user_profiles/user_profiles_list.html', context={'user_profiles': user_profiles})


@user_passes_test(is_admin)
def user_profile_edit(request, id):
    user_profile_to_edit = get_object_or_404(UserProfile, id=id)
    user = get_object_or_404(User, id=user_profile_to_edit.id)

    if request.method == 'POST':
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile_to_edit)
        certificates_formset = CertificatesFormSet(
            request.POST, request.FILES, instance=user_profile_to_edit)
        cases_formset = CasesFormSet(
            request.POST, request.FILES, instance=user_profile_to_edit)

        if user_profile_form.is_valid() and certificates_formset.is_valid() and cases_formset.is_valid():
            user_profile_form.save()
            certificates_formset.save()
            cases_formset.save()
            return redirect('user_profiles_list')
    else:
        user_profile_form = UserProfileForm(instance=user_profile_to_edit)
        certificates_formset = CertificatesFormSet(
            instance=user_profile_to_edit)
        cases_formset = CasesFormSet(instance=user_profile_to_edit)

    return render(request, 'user_profiles/user_profile_edit.html', context={
        'user': user,
        'user_profile_form': user_profile_form,
        'certificates_formset': certificates_formset if user.is_doctor else None,
        'cases_formset': cases_formset if user.is_doctor else None,
    })


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# appointments

@user_passes_test(is_staff)
def appointments_list(request):
    appointments_list = Appointment.objects.all()
    paginator = Paginator(appointments_list, 5)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)

    return render(request, 'appointments/appointments_list.html', context={'appointments': appointments})


def appointment_delete(request, id):
    appointment_to_delete = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        if not appointment_to_delete.is_accepted:
            appointment_to_delete.delete()
        else:
            messages.success(request, 'Accepted Appointment can not deleted .')
            return render(request, 'appointments/appointment_delete.html')

        return redirect('appointments_list')
    return render(request, 'appointments/appointment_delete.html')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# medical_history


@user_passes_test(is_staff)
def ViewMedicalHistory(request):
    medical_list = MedicalHistory.objects.all()
    paginator = Paginator(medical_list, 5)
    page = request.GET.get('page')
    try:
        medical = paginator.page(page)
    except PageNotAnInteger:
        medical = paginator.page(1)
    except EmptyPage:
        medical = paginator.page(paginator.num_pages)
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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# posts in the admin panel


@user_passes_test(is_staff)
def posts_list(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/postslist.html', context={'posts': posts})


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
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# comments in admin panel

@user_passes_test(is_staff)
def ViewComments(request):
    comments_list = Comment.objects.all()
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'comments/commentslist.html', context={'comments': comments})


@method_decorator(user_passes_test(is_staff), name='dispatch')
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

@user_passes_test(is_staff)
def get_all_clinics(request):
    clinics_list = Clinic.objects.all()
    paginator = Paginator(clinics_list, 5)
    page = request.GET.get('page')
    try:
        clinics = paginator.page(page)
    except PageNotAnInteger:
        clinics = paginator.page(1)
    except EmptyPage:
        clinics = paginator.page(paginator.num_pages)
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
@user_passes_test(is_staff)
def get_all_clinic_cases(request):
    cases_list = Cases.objects.all()
    paginator = Paginator(cases_list, 5)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
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
@user_passes_test(is_staff)
def get_all_clinic_images(request):
    clinicimages_list = ClinicImages.objects.all()
    paginator = Paginator(clinicimages_list, 5)
    page = request.GET.get('page')
    try:
        clinicimages = paginator.page(page)
    except PageNotAnInteger:
        clinicimages = paginator.page(1)
    except EmptyPage:
        clinicimages = paginator.page(paginator.num_pages)
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


# ********************************************************************
# reviews

@user_passes_test(is_staff)
def reviews_list(request):
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 5)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return render(request, 'reviews/reviewlist.html', context={'reviews': reviews})


@method_decorator(user_passes_test(is_staff), name='dispatch')
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

from django.urls import path
from custom_admin.views import admin, ViewMedicalHistory, MedicalDetailView, MedicalUpdateView, MedicalCreateView, MedicalDeleteView, appointment_delete, appointments_list, posts_list, reviews_list, user_create, user_delete, user_edit, user_profile_edit, user_profiles_list, users_list
from custom_admin.views import PostDetialView, PostCreateView, PostDeleteView
from custom_admin.views import get_all_clinics, ClinicCreateView, ClinicDeleteView, ClinicUpdateView
from custom_admin.views import get_all_clinic_cases, ClinicCaseCreateView, ClinicCaseDeleteView, ClinicCaseUpdateView
from custom_admin.views import get_all_clinic_images, ClinicImageCreateView, ClinicImageDeleteView, ClinicImagesUpdateView
from custom_admin.views import ReviewDetialView, ReviewCreateView, ReviewDeleteView
from custom_admin.views import ViewComments, CommentDetailView, CommentCreateView, CommentDeleteView


urlpatterns = [
    path('admin_home/', admin, name='admin_home'),
    path('users_list/', users_list, name='users_list'),
    path('user_create/', user_create, name='user_create'),
    path('user_edit/<int:id>/', user_edit, name='user_edit'),
    path('user_delete/<int:id>/', user_delete, name='user_delete'),
    path('user_profiles_list/', user_profiles_list, name='user_profiles_list'),
    path('user_profile_edit/<int:id>/', user_profile_edit,
         name='user_profile_edit'),
    path('appointments_list/', appointments_list, name='appointments_list'),
    path('appointment_delete/<int:id>/',
         appointment_delete, name='appointment_delete'),
    path('allmedical', ViewMedicalHistory, name='allmedical'),
    path('allmedical/<int:pk>/', MedicalDetailView.as_view(), name='medical_detail'),
    path('allmedical/update/<int:pk>/',
         MedicalUpdateView.as_view(), name='medical_update'),
    path('medical/create/', MedicalCreateView.as_view(), name='medical_create'),
    path('medical/delete/<int:pk>/',
         MedicalDeleteView.as_view(), name='medical_delete'),
    path('posts', posts_list, name='postslist'),
    path('post/<int:pk>', PostDetialView.as_view(), name='postdetial'),
    path('createpost', PostCreateView.as_view(), name='postcreate'),
    path('deletepost/<int:pk>', PostDeleteView.as_view(), name='postdelete'),
    path('clinics/', get_all_clinics, name='clinics_list'),
    path('clinics/create/', ClinicCreateView.as_view(), name='create_clinic'),
    path('clinics/delete/<int:pk>',
         ClinicDeleteView.as_view(), name='delete_clinic'),
    path('clinics/update/<int:pk>',
         ClinicUpdateView.as_view(), name='update_clinic'),
    path('clinicscases/', get_all_clinic_cases, name='clinics_cases_list'),
    path('clinicscases/create/', ClinicCaseCreateView.as_view(),
         name='create_clinic_case'),
    path('clinicscases/delete/<int:pk>',
         ClinicCaseDeleteView.as_view(), name='delete_clinic_case'),
    path('clinicscases/update/<int:pk>',
         ClinicCaseUpdateView.as_view(), name='update_clinic_case'),
    path('clinicsimages/', get_all_clinic_images, name='clinics_images_list'),
    path('clinicsimages/create/', ClinicImageCreateView.as_view(),
         name='create_clinic_images'),
    path('clinicsimages/delete/<int:pk>',
         ClinicImageDeleteView.as_view(), name='delete_clinic_image'),
    path('clinicsimages/update/<int:pk>',
         ClinicImagesUpdateView.as_view(), name='update_clinic_image'),
    path('comments_list/', ViewComments, name='commentslist'),
    path('comments_list/<int:pk>/',
         CommentDetailView.as_view(), name='comment_detail'),
    # path('createcomment', CommentCreateView.as_view(), name='commentcreate'),
    path('deletecomment/<int:pk>',
         CommentDeleteView.as_view(), name='comment_delete'),


]

urlpatterns += [
    path('reviewlist', reviews_list, name='reviewlist'),
    path('review/<int:pk>', ReviewDetialView.as_view(), name='reviewdetial'),
    path('createreview', ReviewCreateView.as_view(), name='reviewcreate'),
    path('deletereview/<int:pk>', ReviewDeleteView.as_view(), name='reviewdelete'),
]

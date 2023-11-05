from django.urls import path
from accounts.views import UserSignup, MyTokenObtainPairView, add_case, add_certificate, delete_case, delete_certificate, delete_profile_pic, edit_profile, edit_profile_pic, get_cases, get_certificates, get_profile, get_user
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserSignup.as_view(), name='account.register'),
    # path('login/', UserLogin.as_view(), name='account.login'),
    # path('logout/', UserLogout.as_view(), name='account.logout'),
    # path('user/', UserView.as_view(), name='account.user'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', get_user, name='account.user'),
    path('profile/<int:id>', get_profile, name='account.profile'),
    path('profile/edit/', edit_profile, name='account.edit_profile'),
    path('profile/edit/pic/', edit_profile_pic,
         name='account.edit_profile_pic'),
    path('profile/delete/pic/', delete_profile_pic,
         name='account.delete_profile_pic'),
    path('profile/case/', add_case, name='account.add_case'),
    path('profile/case/<int:id>', get_cases, name='account.get_cases'),
    path('profile/case/delete/<int:id>',
         delete_case, name='account.delete_case'),
    path('profile/certificate/', add_certificate,
         name='account.add_certificate'),
    path('profile/certificate/<int:id>', get_certificates,
         name='account.get_certificates'),
    path('profile/certificate/delete/<int:id>',
         delete_certificate, name='account.delete_certificate'),
]

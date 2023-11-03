from django.urls import path
from accounts.views import UserSignup, MyTokenObtainPairView, add_case_image, delete_case_image, edit_profile, get_profile, get_user
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
    path('profile/edit/', edit_profile, name='account.editProfile'),
    path('profile/case/', add_case_image, name='account.addCases'),
    path('profile/case/delete/<int:id>',
         delete_case_image, name='account.deleteCases'),
]

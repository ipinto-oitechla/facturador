from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'
urlpatterns = [
    path('login/',
         views.Login.as_view(),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('change_password/',
         views.change_password,
         name='change_password'),
    path('rol',
       views.RolList.as_view(),
       name='RolList'
       ),
    path('rolAdd',
       views.RolAdd.as_view(),
       name='RolAdd'
       ),
    path('rolUpdate/<int:pk>',
       views.RolUpdate.as_view(),
       name='RolUpdate'
       ),
    path('RolDelete/<int:pk>',
       views.RolDelete.as_view(),
       name='RolDelete'
       ),
    path('users',
       views.UserList.as_view(),
       name='UserList'
       ),
    path('userAdd',
       views.UserAdd.as_view(),
       name='UserAdd'
       ),
    path('userUpdate/<int:pk>',
       views.UserUpdate.as_view(),
       name='UserUpdate'
       ),
    path('UserDelete/<int:pk>',
       views.UserDelete.as_view(),
       name='UserDelete'
       ),
    path('reset_password/<int:pk>',
         views.PasswordResetConfirmView.as_view(),
         name='PasswordResetConfirmView',
        ),
    path('userCambioEstado/<int:pk>',
       views.CambiarEstado.as_view(),
       name='CambiarEstado'
       ),
    path('userCambioTipo/<int:pk>',
       views.CambiarTipo.as_view(),
       name='CambiarTipo'
       ),
]+ static(settings.MEDIA_URL)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'cobrox'
urlpatterns = [
    path('',
         views.Viewindex.as_view(),
         name='index2'
    ),
    path('index.html',
         views.Viewindex.as_view(),
         name='index'
        ),
    path('dashboard',
         views.Viewindex.as_view(),
         name='dashboard'
        ),
    path('filial',
       views.FilialList.as_view(),
       name='FilialList'
       ),
    path('filialAdd',
       views.FilialAdd.as_view(),
       name='FilialAdd'
       ),
    path('filialUpdate/<int:pk>',
       views.FilialUpdate.as_view(),
       name='FilialUpdate'
       ),
    path('FilialDelete/<int:pk>',
       views.FilialDelete.as_view(),
       name='FilialDelete'
       ),
    ] + static(settings.MEDIA_URL)

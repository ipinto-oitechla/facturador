from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework import routers
from .views import CustomAuthToken, ListadoItemsByCatalogo #, ProductoViewSet,

router = routers.DefaultRouter()
#router.register(r'productos', ProductoViewSet)

app_name = 'restser'
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('listitemsbycatalog/<str:codigo>', ListadoItemsByCatalogo.as_view(), name='ListadoItemsByCatalogo'),
    path('listcatalog', views.ListadoCatalogos.as_view(), name='ListadoCatalogos'),
    path('listdepartamentos', views.ListadoDepartamentos.as_view(), name='ListadoDepartamentos'),
    path('listmunicipiosbydepartamento/<int:id>', views.ListadoMunicipiosByDepartamento.as_view(), name='ListadoMunicipiosByDepartamento'),
    path('listcategoriaseconomicas', views.ListadoCategoriasEconomicas.as_view(), name='ListadoCategoriasEconomicas'),
    path('listsubcategoriaseconomicasbycategoria/<int:id>', views.ListadoSubCategoriasEconomicasbyCategoria.as_view(), name='ListadoSubCategoriasEconomicasbyCategoria'),
    path('listactividadesconomicasbysubcategoria/<int:id>', views.ListadoActividadesEconomicasBySub.as_view(), name='ListadoActividadesEconomicasBySub'),
    path('listtributos', views.ListadoTributos.as_view(), name='ListadoTributos'),
    path('facturatest', views.FacturaManagerView.as_view(), name='ListadoFactura'),


    ] + static(settings.MEDIA_URL)

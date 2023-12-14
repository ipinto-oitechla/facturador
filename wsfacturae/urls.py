from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'wsfacturae'
urlpatterns = [
    path('wsentorno',
           views.WsEntornoList.as_view(),
           name='WsEntornoList'
           ),
    path('wsentornoAdd',
           views.WsEntornoAdd.as_view(),
           name='WsEntornoAdd'
           ),
    path('wsentornoUpdate/<int:pk>',
           views.WsEntornoUpdate.as_view(),
           name='WsEntornoUpdate'
           ),
    path('WsEntornoDelete/<int:pk>',
           views.WsEntornoDelete.as_view(),
           name='WsEntornoDelete'
           ),
    path('wsurl',
           views.WsUrlList.as_view(),
           name='WsUrlList'
           ),
    path('wsurlAdd',
           views.WsUrlAdd.as_view(),
           name='WsUrlAdd'
           ),
    path('wsurlUpdate/<int:pk>',
           views.WsUrlUpdate.as_view(),
           name='WsUrlUpdate'
           ),
    path('WsUrlDelete/<int:pk>',
           views.WsUrlDelete.as_view(),
           name='WsUrlDelete'
           ),
    path('mastercat',
           views.MastercatList.as_view(),
           name='MastercatList'
           ),
    path('mastercatAdd',
           views.MastercatAdd.as_view(),
           name='MastercatAdd'
           ),
    path('mastercatUpdate/<int:pk>',
           views.MastercatUpdate.as_view(),
           name='MastercatUpdate'
           ),
    path('MastercatDelete/<int:pk>',
           views.MastercatDelete.as_view(),
           name='MastercatDelete'
           ),
    path('detallemastercatAdd',
           views.DetalleMastercatAdd.as_view(),
           name='DetalleMastercatAdd'
           ),
    path('detallemastercatAdd/<int:pk>',
           views.DetalleMastercatAdd.as_view(),
           name='DetalleMastercatAdd'
           ),
    path('detallemastercatDel/<int:pk>',
           views.DetalleMastercatDelete.as_view(),
           name='DetalleMastercatDelete'
           ),
    path('detallemastercatUpdate/<int:pk>',
           views.DetalleMastercatUpdate.as_view(),
           name='DetalleMastercatupdate'
           ),
    path('catactividadeco',
           views.CatactividadecoList.as_view(),
           name='CatactividadecoList'
           ),
    path('catactividadecoAdd',
           views.CatactividadecoAdd.as_view(),
           name='CatactividadecoAdd'
           ),
    path('catactividadecoUpdate/<int:pk>',
           views.CatactividadecoUpdate.as_view(),
           name='CatactividadecoUpdate'
           ),
    path('catactividadecoDelete/<int:pk>',
           views.CatactividadecoDelete.as_view(),
           name='CatactividadecoDelete'
           ),
    path('subcatactividadeco',
           views.SubCatactividadecoList.as_view(),
           name='SubCatactividadecoList'
           ),
    path('subcatactividadecoAdd/<int:pk>',
           views.SubCatactividadecoAdd.as_view(),
           name='SubCatactividadecoAdd'
           ),
    path('subcatactividadecoUpdate/<int:pk>',
           views.SubCatactividadecoUpdate.as_view(),
           name='SubCatactividadecoUpdate'
           ),
    path('subcatactividadecoDelete/<int:pk>',
           views.SubCatactividadecoDelete.as_view(),
           name='SubCatactividadecoDelete'
           ),
    path('actividadeco',
           views.ActividadecoList.as_view(),
           name='ActividadecoList'
           ),
    path('actividadecoAdd',
           views.ActividadecoAdd.as_view(),
           name='ActividadecoAdd'
           ),
    path('ActividadecoUpdate/<int:pk>',
           views.ActividadecoUpdate.as_view(),
           name='ActividadecoUpdate'
           ),
    path('actividadecoDelete/<int:pk>',
           views.ActividadecoDelete.as_view(),
           name='ActividadecoDelete'
           ),
    path('departamento',
           views.DepartamentoList.as_view(),
           name='DepartamentoList'
           ),
    path('departamentoAdd',
           views.DepartamentoAdd.as_view(),
           name='DepartamentoAdd'
           ),
    path('departamentoUpdate/<int:pk>',
           views.DepartamentoUpdate.as_view(),
           name='DepartamentoUpdate'
           ),
    path('DepartamentoDelete/<int:pk>',
           views.DepartamentoDelete.as_view(),
           name='DepartamentoDelete'
           ),
    #path('municipioAdd',
    #       views.MunicipioAdd.as_view(),
    #       name='MunicipioAdd'
    #       ),
    path('municipioAdd/<int:pk>',
           views.MunicipioAdd.as_view(),
           name='MunicipioAdd'
           ),
    path('municipioDel/<int:pk>',
           views.MunicipioDelete.as_view(),
           name='MunicipioDelete'
           ),
    path('municipioUpdate/<int:pk>',
           views.MunicipioUpdate.as_view(),
           name='Municipioupdate'
           ),
    path('tributo',
           views.TributoList.as_view(),
           name='TributoList'
           ),
    path('tributoAdd',
           views.TributoAdd.as_view(),
           name='TributoAdd'
           ),
    path('tributoUpdate/<int:pk>',
           views.TributoUpdate.as_view(),
           name='TributoUpdate'
           ),
    path('tributoDelete/<int:pk>',
           views.TributoDelete.as_view(),
           name='TributoDelete'
           ),
           #Lista de los DTE
    path('listadoDTE/',
         views.DteList.as_view(),
         name='DteList'),
    path('detalleDTE/<int:pk>',
         views.DteDetail.as_view(),
         name='DteDetail'),
       #Vista para enviar la solicitud de email
    path('enviarMail/<int:pk>',
         views.SendPdfMail.as_view(),
         name="pdfList"),
    path('pdfView/<int:pk>', views.MyPDFView.as_view(), name="pdfView"),
    path('dteFormView/<str:tipo_dte>/', views.DteFormView.as_view(), name="dteFormView"),
    path('productoList/', views.ProductoListView.as_view(), name="ProductoList"),
    path('productoAdd/', views.ProductoAddView.as_view(), name="AddProducto"),
    path('productoDelete/<int:pk>', views.ProductoDelete.as_view(), name="DeleteProducto"),
    path('productoUpdate/<int:pk>', views.ProductoUpdate.as_view(), name="UpdateProducto"),
    path('descuentoList/', views.DescuentoListView.as_view(), name="DescuentoList"),
    path('descuentoAdd/', views.DescuentoAddView.as_view(), name="AddDescuento"),
    path('descuentoUpdate/<int:pk>', views.DescuentoUpdateView.as_view(), name="UpdateDescuento"),
    path('descuentoDelete/<int:pk>', views.DescuentoDelete.as_view(), name="DeleteDescuento"),
    path('EstablecimientoList/', views.EstablecimientoListView.as_view(), name="EstablecimientoList"),
    path('EstablecimientoAdd/', views.EstablecimientoCreateView.as_view(), name="EstablecimientoAdd"),
    path('EstablecimientoDelete/<int:pk>', views.EstablecimientoDeleteView.as_view(), name="EstablecimientoDelete"),
    path('EstablecimientoUpdate/<int:pk>', views.EstablecimientoUpdateView.as_view(), name="EstablecimientoUpdate"),
    path('PuntoVentaAdd/<int:pk>',views.PuntoVentaCreateView.as_view(), name="PuntoVentaAdd"),
    path('PuntoVentaUpdate/<int:pk>',views.PuntoVentaUpdateView.as_view(), name="PuntoVentaUpdate"),
    path('PuntoVentaDelete/<int:pk>',views.PuntoVentaDeleteView.as_view(), name="PuntoVentaDelete"),
    path('ReceptorAdd/',views.ReceptorNCreateView.as_view(), name="ReceptorAdd"),
    path('ReceptorList/',views.ReceptorNList.as_view(), name="ReceptorList"),
    path('ReceptorUpdate/<int:pk>',views.ReceptorNUpdateView.as_view(), name="ReceptorUpdate"),
    path('ReceptorDelete/<int:pk>',views.ReceptorNDeleteView.as_view(), name="ReceptorDelete"),
    path('jsonView/<int:pk>', views.JsonView.as_view(), name="jsonView"),
    path('sendSMS/<int:pk>', views.SendSMS.as_view(), name="sendSMS"),
    path('downloadPDF/<int:pk>', views.DownloadPDF.as_view(),name="downloadPDF"),
    path('emisor/', views.EmisorDetailView.as_view(), name='emisor-detail'),
    path('updateEmisor/<int:pk>', views.EmisorUpdate.as_view(),name="EmisorUpdate"),
    path('ajax/load-subacts/', views.load_subact, name='ajax_load_subacts'),
    path('ajax/load-muns/', views.load_muni, name='ajax_load_munis'),
    path('ajax/load-actecos/', views.load_acteco, name='ajax_load_actecos'),
    path('smtp/', views.SMTPDetailView.as_view(), name='smtp-detail'),
    path('addSMTP/', views.SMTPAddView.as_view(), name="SMTPAdd"),
    path('updateSMTP/<int:pk>', views.SMTPUpdate.as_view(), name="SMTPUpdate"),
    ] + static(settings.MEDIA_URL)

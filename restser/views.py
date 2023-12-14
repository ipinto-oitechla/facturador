from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
#from .models import Producto
from .serializers import FacturaSerializer
from django.dispatch import Signal
from .models import DetalleFactura, Factura
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from wsfacturae.models import detallemastercat,mastercat,departamento,municipio,catactividadeco,subactividadeco,actividadeco,tributo


#class ProductoViewSet(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
#    queryset = Producto.objects.all()
#    serializer_class = ProductoSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            # check if token is expired, delete token and create new one
            expire_seconds = int(getattr(settings, 'REST_FRAMEWORK_TOKEN_DURATION', 3600).total_seconds())
            if (datetime.now() - token.created) > timedelta(seconds=expire_seconds):
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
        return Response({'token': token.key})


class ListadoItemsByCatalogo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, codigo):
        items = detallemastercat.objects.filter(mastercat__codigo=codigo).filter(nm_estado=1).order_by("codigo")
        response_data = []

        for item in items:
            response_data.append({
                'id': item.id,
                'codigo': item.codigo,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoCatalogos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = mastercat.objects.filter(nm_estado=1).order_by("codigo")
        response_data = []

        for item in items:
            response_data.append({
                'id': item.id,
                'codigo': item.codigo,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoDepartamentos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = departamento.objects.filter(nm_estado=1).order_by("codigo")
        response_data = []

        for item in items:
            response_data.append({
                'id': item.id,
                'codigo': item.codigo,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoMunicipiosByDepartamento(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        items = municipio.objects.filter(nm_estado=1).filter(departamento__id=id).order_by("departamento","codigo")
        response_data = []

        for item in items:
            response_data.append({
                'id': item.id,
                'codigo': item.codigo,
                'descripcion': item.descripcion,
                'departamento': item.departamento.descripcion,
            })

        return Response(response_data)


class ListadoCategoriasEconomicas(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = catactividadeco.objects.filter(nm_estado=1).order_by("descripcion")
        response_data = []
        for item in items:
            response_data.append({
                'id': item.id,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoSubCategoriasEconomicasbyCategoria(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        items = subactividadeco.objects.filter(nm_estado=1).filter(catactividadeco__id=id).order_by("descripcion")
        response_data = []
        for item in items:
            response_data.append({
                'id': item.id,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoActividadesEconomicasBySub(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        items = actividadeco.objects.filter(nm_estado=1).filter(subactividadeco__id=id).order_by("descripcion")
        response_data = []
        for item in items:
            response_data.append({
                'id': item.id,
                'codigo': item.codigo,
                'descripcion': item.descripcion,
            })

        return Response(response_data)


class ListadoTributos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = tributo.objects.filter(nm_estado=1).order_by("seccion","codigo","descripcion")
        response_data = []
        for item in items:
            response_data.append({
                'id': item.id,
                'seccion_id': item.seccion,
                'seccion_desc': item.get_seccion_display(),
                'codigo': item.codigo,
                'descripcion': item.descripcion,
                'tipo_id': item.tipo,
                'tipo_desc': item.get_tipo_display(),
                'valor': item.valor,
            })
        return Response(response_data)


class FacturaManagerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = FacturaSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):

        factura = Factura.objects.all()
        serializer = FacturaSerializer(factura, many = True)
        return Response(serializer.data)
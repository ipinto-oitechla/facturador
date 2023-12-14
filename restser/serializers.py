from rest_framework import serializers
from wsfacturae.models import detallemastercat,tributo
from restser.models import Factura, DetalleFactura
import re

patron_tele = r'^\d{4}-\d{4}$'
patron_nrc = r'^\d{6}-\d{1}$'
patron_dui = r'^\d{8}-\d{1}$'
patron_nit = r'^\d{4}-\d{6}-\d{3}-\d{1}$'


class DetalleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'monto']

class FacturaSerializer(serializers.ModelSerializer):
    detalle= DetalleSerializer(many=True)
    class Meta:
        model = Factura
        fields = ['fecha', 'codigo','subtotal','detalle']

    def create(self, validated_data):
        detalle_data = validated_data.pop('detalle')
        factura = Factura.objects.create(**validated_data)
        for detalle in detalle_data:
            DetalleFactura.objects.create(fk_factura=factura, **detalle)
        return factura
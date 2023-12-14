from django.db import models


class DocumentoRelacionado(models.Model):
    tipoDocumento = models.IntegerField()
    tipoGeneracion = models.IntegerField()
    numeroDocumento = models.IntegerField()
    fechaEmision = models.DateField()


class Direccion(models.Model):
    departamento = models.CharField(max_length=200)
    municipio = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)

class Factura(models.Model):
    fecha = models.DateField()
    codigo = models.CharField(max_length=8, null= True)

class DetalleFactura(models.Model):
    fk_factura = models.ForeignKey(Factura, related_name='detalle', on_delete=models.CASCADE, null = True)
    producto = models.CharField(max_length=100, null=True)
    cantidad = models.IntegerField(null=True)
    monto = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    


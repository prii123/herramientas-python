from django.db import models

class Cliente(models.Model):
    nit = models.CharField(max_length=255)
    dv = models.CharField(max_length=255)
    apellido1 = models.CharField(max_length=255)
    apellido2 = models.CharField(max_length=255)
    nombre1 = models.CharField(max_length=255)
    nombre2 = models.CharField(max_length=255)
    razon_social = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    @staticmethod
    def obtener_clientes():
        return Cliente.objects.all()

    @staticmethod
    def obtener_cliente_por_nit(nit):
        try:
            return Cliente.objects.get(nit=nit)
        except Cliente.DoesNotExist:
            return None
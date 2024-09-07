from django.db import models
from django.utils.translation import gettext_lazy as _

class OrderStatus(models.TextChoices):
    PENDING = 'P', _('Pendiente')
    ACCEPTED = 'A', _('Aceptado')
    REJECTED = 'R', _('Rechazado')
    DELIVERED = 'D', _('Entregado')

class PaymentStatus(models.TextChoices):
    PENDING = 'P', _('Pendiente')
    COMPLETED = 'C', _('Completado')
    FAILED = 'F', _('Fallido')

class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'CE', _('Pago contra entrega')
    IN_STORE = 'PT', _('Pago en tienda')
    PSE = 'PSE', _('PSE')

class Locality(models.TextChoices):
    USAQUEN = 'USA', _('Usaquen')
    CHAPINERO = 'CHA', _('Chapinero')
    SANTA_FE = 'STF', _('Santa Fe')
    SAN_CRISTOBAL = 'SC', _('San Cristobal')
    USME = 'USM', _('Usme')
    TUNJUELITO = 'TUN', _('Tunjuelito')
    BOSA = 'BOS', _('Bosa')
    KENNEDY = 'KEN', _('Kennedy')
    FONTIBON = 'FON', _('Fontibon')
    ENGATIVA = 'ENG', _('Engativa')
    SUBA = 'SUB', _('Suba')
    BARRIOS_UNIDOS = 'BAU', _('Barrios Unidos')
    TEUSAQUILLO = 'TEU', _('Teusaquillo')
    LOS_MARTIRES = 'MAR', _('Los Martires')
    ANTONIO_NARIÑO = 'ANT', _('Antonio Nariño')
    PUENTE_ARANDA = 'PUE', _('Pueblo Aranda')
    CANDELARIA = 'CAN', _('Candelaria')
    RAFAEL_URIBE = 'RUR', _('Rafael Uribe')
    CIUDAD_BOLIVAR = 'CBO', _('Ciudad Bolivar')
    SUMAPAZ = 'SUM', _('Sumapaz')

class StreetType(models.TextChoices):
    CALLE = 'CL', _('Calle')
    CARRERA = 'CRA', _('Carrera')
    AVENIDA = 'AV', _('Avenida')
    AVENIDA_CARRERA = 'ACR', _('Avenida Carrera')
    AVENIDA_CALLE = 'ACL', _('Avenida Calle')
    DIAGONAL = 'DG', _('Diagonal')
    TRANSVERSAL = 'TV', _('Transversal')
    AUTOPISTA = 'AUT', _('Autopista')
    VIA = 'VIA', _('Via')
    CIRCULAR = 'CIR', _('Circular')
    CIRCUNVALAR = 'CVC', _('Circunvalar')
    MANZANA = 'MZ', _('Manzana')
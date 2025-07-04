from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from .carrier import Carrier
from .driver import Driver
from .document import Document

User = get_user_model()

class VehicleStatus(models.TextChoices):
    """Status de um veículo na frota em português."""
    ACTIVE = 'active', 'Ativo'
    MAINTENANCE = 'maintenance', 'Em manutenção'
    DECOMMISSIONED = 'decommissioned', 'Baixado'

class DrivingProfile(models.TextChoices):
    """Perfis de direção compatíveis com ORS."""
    DRIVING_CAR = 'driving-car', 'Carro'
    DRIVING_HGV = 'driving-hgv', 'Caminhão/Veículo pesado'

class VehicleAssignment(models.Model):
    """Histórico de atribuição de motorista a veículo."""
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='assignments')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='assignments')
    start_date = models.DateField('Início')
    end_date = models.DateField('Fim', null=True, blank=True)

    class Meta:
        verbose_name = 'Atribuição de Veículo'
        verbose_name_plural = 'Atribuições de Veículo'
        unique_together = ('vehicle', 'driver', 'start_date')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.driver} -> {self.vehicle} ({self.start_date} até {self.end_date or 'presente'})"

auditlog.register(VehicleAssignment)

class Vehicle(models.Model):
    """Veículo na frota: interno ou terceirizado."""
    license_plate = models.CharField(
        'Placa', max_length=10, unique=True,
        db_index=True
    )
    brand = models.CharField('Marca', max_length=50, null=True, blank=True)
    model = models.CharField('Modelo', max_length=50, null=True, blank=True)
    year = models.PositiveSmallIntegerField('Ano de Fabricação',null=True, blank=True)

    # tipo 
    vehicle_type = models.CharField(
        'Tipo de Veículo', max_length=20,
        choices=DrivingProfile.choices,
        default=DrivingProfile.DRIVING_CAR
    )

    # A ligação com a área de rota:
    route_area = models.ForeignKey(
        'RouteArea',
        verbose_name='Área de Rota',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )

    # condução
    driver = models.ForeignKey(
        Driver, verbose_name='Motorista Interno',
        on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles'
    )
    carrier = models.ForeignKey(
        Carrier, verbose_name='Transportadora',
        on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles'
    )
    document = models.ManyToManyField(
        Document,
        verbose_name='Documentos',
        blank=True,
        related_name='documents_vehicles',
        help_text='Documentos relacionados ao veículo'
    )
    
    is_outsourced = models.BooleanField('Terceirizado', default=False)
    is_active = models.BooleanField('Ativo', default=True)

    # capacidades e status
    max_volume_m3 = models.DecimalField('Capacidade (m³)', max_digits=8, decimal_places=2)
    max_weight_kg = models.DecimalField('Capacidade (kg)', max_digits=8, decimal_places=2)
    
    status = models.CharField(
        'Status', max_length=20,
        choices=VehicleStatus.choices,
        default=VehicleStatus.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles_created'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['license_plate']
        indexes = [models.Index(fields=['license_plate']), models.Index(fields=['brand','model'])]

    def clean(self):
        if self.is_outsourced and not self.carrier:
            raise ValidationError('Defina a transportadora para veículo terceirizado.')

    def __str__(self):
        if self.is_outsourced:
            return f"{self.license_plate} - {self.brand} ({self.carrier})"
        return f"{self.license_plate} - {self.brand} ({self.driver})"
    
    @property
    def name(self):
        return self.license_plate
    
    def get_vehicle_type(self):
        return self.get_vehicle_type_display()


    @property
    def formatted_max_weight_kg(self) -> str:
        """
        Exibe max_weight_kg no formato “1.234,56”.
        """
        w = float(self.max_weight_kg or 0)
        # formata com separador de milhar “,” e ponto decimal “.”
        s = f"{w:,.2f}"
        # troca para formato brasileiro: ponto → separador de milhar, vírgula → decimal
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s

    @property
    def formatted_max_volume_m3(self) -> str:
        """
        Exibe max_volume_m3 no formato “1.234,56”.
        """
        v = float(self.max_volume_m3 or 0)
        s = f"{v:,.2f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    
auditlog.register(Vehicle)


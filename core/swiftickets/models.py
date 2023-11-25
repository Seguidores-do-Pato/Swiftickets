from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

#user model

class UserManager(UserManager):
    def _create_user(self,email, password, **extra_fields):
        if not email:
            raise ValueError("Email inválido!!!!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    cpf = models.CharField(max_length=14, blank=True, default='')
    birthday = models.DateField(null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    num_edit = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    lost_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
#event model

class Event(models.Model):
    eventType = models.TextChoices(
        "eventType",
        "Show Festival"
    )
    eventState = models.TextChoices(
        "eventState",
        "Open Closed"
    )
    brazilStates = models.TextChoices(
        "brazilStates",
        "Acre Alagoas Amapá Amazonas Bahia Ceará DistritoFederal EspíritoSanto Goiás Maranhão MatoGrosso MatoGrossodoSul MinasGerais Pará Paraíba Paraná Pernambuco Piauí RiodeJaneiro RioGrandedoNorte RioGrandedoSul Rondônia Roraima SantaCatarina SãoPaulo Sergipe Tocantins"
    )

    type = models.CharField(max_length=14, choices=eventType.choices)
    registrant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255, blank=True, default='')
    state = models.CharField(max_length=14, choices=eventState.choices, default="Open")
    uf = models.CharField(max_length=16, choices=brazilStates.choices, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    open_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    close_at = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return str(self.name)

    def next_state(state):
        return "Closed"

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

#ticket model

class Ticket(models.Model):
    ticketType = models.TextChoices(
        "ticketType",
        "Normal Vip"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False, null=False)
    ticket_type = models.CharField(max_length=14, choices=ticketType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    sale_start_date = models.DateTimeField(default=timezone.now)
    sale_end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.name}"

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

#purchase model

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.ticket.ticket_type} - {self.ticket.event.name}"

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
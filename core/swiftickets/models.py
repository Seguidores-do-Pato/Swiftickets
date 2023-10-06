from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

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
    birthday = models.DateField(null=True, blank=True)
    isEvent = models.BooleanField(default=False)

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
    
#ticket model

class Ticket(models.Model):
    ticketType = models.TextChoices(
        "ticketType",
        "Show Festival"
    )
    ticketState = models.TextChoices(
        "ticketState",
        "Open Closed"
    )
    brazilStates = models.TextChoices(
        "brazilStates",
        "Acre Alagoas Amapá Amazonas Bahia Ceará DistritoFederal EspíritoSanto Goiás Maranhão MatoGrosso MatoGrossodoSul MinasGerais Pará Paraíba Paraná Pernambuco Piauí RiodeJaneiro RioGrandedoNorte RioGrandedoSul Rondônia Roraima SantaCatarina SãoPaulo Sergipe Tocantins"
    )

    type = models.CharField(max_length=14, choices=ticketType.choices)
    registrant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    state = models.CharField(max_length=14, choices=ticketState.choices, default="Open")
    uf = models.CharField(max_length=16, choices=brazilStates.choices, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def next_state(state):
        return "Closed"

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
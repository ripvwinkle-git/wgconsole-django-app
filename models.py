'''
Wgconsole django models.
'''
import subprocess
from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model

class Interface(models.Model):
    '''
    Interfaces fields.
    '''
    name = models.CharField(
        max_length=20,
        primary_key=True,
    )

    address = models.CharField(
        max_length=100,
        blank=False,
        default='',
    )
    port = models.PositiveIntegerField(
        null=True,
    )
    public_key = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )

    endpoint_ip_peer = models.GenericIPAddressField(
        blank = False,
    )
    allowed_ips_peer = models.CharField(
        max_length=100,
        blank=False,
        default='0.0.0.0/0'
    )

    ACTIVE = True
    INACTIVE = False
    STATUS_CHOICES = [
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    ]
    status = models.BooleanField(
        choices=STATUS_CHOICES,
        default=INACTIVE)

    RUNNING = True
    DEAD = False
    STATE_CHOICES = [
        (RUNNING, 'running'),
        (DEAD, 'dead'),
    ]
    state = models.BooleanField(
        choices=STATE_CHOICES,
        default=DEAD,
        editable=False,
    )

    description = models.CharField(
        max_length=1000,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

class Peer(models.Model):
    '''
    Peers fields.
    '''
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    private_key = models.CharField(
        max_length=1000,
        blank=False,
    )
    public_key = models.CharField(
        max_length=1000,
        blank=False,
        unique=True,
    )
    allowed_ips = models.CharField(
        max_length=1000,
        blank=False,
        unique=True,
    )
    listen_port = models.PositiveIntegerField(
        default=51820,
        validators=(validators.MaxValueValidator(65535),)
    )

    ACTIVE = True
    INACTIVE = False
    STATUS_CHOICES = [
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    ]
    status = models.BooleanField(
        choices=STATUS_CHOICES,
        default=ACTIVE)
    state = models.CharField(
        max_length=1000,
        blank=True,
    )

    description = models.CharField(
        max_length=1000,
        blank=True,
    )

    def __str__(self)->str:
        return f'{self.interface} | {self.user}'
    
    @staticmethod
    def genkey()->str:
        try:
            private_key = subprocess.run(
                ('wg', 'genkey'),
                capture_output=True,
                encoding='UTF-8',
                check=False
            )
            return private_key.stdout
        except FileNotFoundError:
            return 'FileNotFoundError'

    @staticmethod
    def pubkey(private_key:str)->str:
        try:
            public_key = subprocess.run(
                ('wg', 'pubkey'),
                input=f'{private_key}',
                capture_output=True,
                encoding='UTF-8',
                check=False
            )
            return public_key.stdout
        except FileNotFoundError:
            return 'FileNotFoundError'

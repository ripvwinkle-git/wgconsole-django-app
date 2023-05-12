from django.contrib import admin
from .models import Interface, Peer

@admin.register(Interface)
class WgInterfaceAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'address',
        'port',
        'public_key',
        'endpoint_ip_peer',
        'allowed_ips_peer',
        'status',
        'state',
        'description',
    )
    readonly_fields = (
        'address',
        'port',
        'public_key',
        'state',
    )
    list_display = (
        'name',
        'address',
        'port',
        'status',
        'state',
        'description',
    )

@admin.register(Peer)
class WgPeerAdmin(admin.ModelAdmin):
    change_form_template = 'admin/wgconsole/peer/change_form.html'
    fields = (
        'user',
        'interface',
        'private_key',
        'public_key',
        'allowed_ips',
        'listen_port',
        'status',
        'state',
        'description',
    )
    readonly_fields = (
        'state',
    )
    list_display = (
        'user',
        'id',
        'interface',
        'allowed_ips',
        'status',
        'state',
        'description',
    )
    list_filter = (
        'interface',
    )



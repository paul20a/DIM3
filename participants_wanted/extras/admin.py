from django.contrib import admin
from extras.models import Actor, Director, Role, Application, Production

admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Role)
admin.site.register(Application)
admin.site.register(Production)

from django.contrib import admin
from .models import Policy, PolicyPremium, HealthPolicy, Dependent, Claim
# Register your models here.
admin.site.register(Policy)
admin.site.register(PolicyPremium)
admin.site.register(HealthPolicy)
admin.site.register(Dependent)
admin.site.register(Claim)
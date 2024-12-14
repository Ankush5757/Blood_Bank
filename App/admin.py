from django.contrib import admin
from . models import Register,Profile_pictures,Request,Blood_Donor, Donate_Us

# Register your models here.

# Register the model once with the custom admin class
admin.site.register(Profile_pictures)
admin.site.register(Register)
admin.site.register(Request)
admin.site.register(Blood_Donor)
admin.site.register(Donate_Us)

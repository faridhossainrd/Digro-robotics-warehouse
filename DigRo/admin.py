from django.contrib import admin
from .models import Allroducts , orders_storage ,Total , robot_map ,productdata,productupdate
# Register your models here.


# Register your models here

admin.site.register(Allroducts)
admin.site.register(orders_storage)
admin.site.register(Total)
admin.site.register(robot_map)
admin.site.register(productdata)
admin.site.register(productupdate)

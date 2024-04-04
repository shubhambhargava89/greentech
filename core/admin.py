from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(CustomerLogin)

admin.site.register(Product)

admin.site.register(Enquiry)

admin.site.register(AdminProfile)

admin.site.register(UserAddres)

admin.site.register(CartItem)

admin.site.register(OrderPlaced)

admin.site.register(Feedback)

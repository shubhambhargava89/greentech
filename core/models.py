from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField()
    category = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10, null=True)
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name


class CustomerLogin(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   email = models.CharField(max_length=100)
   contact_number = models.CharField(max_length=15)
   gender = models.CharField(max_length=15, null=True)
   type = models.CharField(max_length=15, null=True)

   def __str__(self):
       return self.user.first_name


class Enquiry(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, null=True)
    mail = models.CharField(max_length=100)
    about = models.TextField()
    creationdate = models.DateField()

    def __str__(self):
        return self.firstname


class AdminProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.first_name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.first_name


class UserAddres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RAZORPAY', 'Pay with Razorpay'),
    ]

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerLogin, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment_id = models.CharField(max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.user.first_name


class Feedback(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, null=True)
    mail = models.CharField(max_length=100)
    about = models.TextField()
    creationdate = models.DateField()

    def __str__(self):
        return self.firstname
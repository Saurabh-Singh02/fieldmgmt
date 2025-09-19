from django.db import models
# from django.db import models
# from accounts.models import CustomUser   # Assuming you use CustomUser for "User"

# class ClientCompany(models.Model):
#     name = models.CharField(max_length=255)
#     contact_email = models.EmailField()
#     contact_phone = models.CharField(max_length=20, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     industry = models.CharField(max_length=100, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
# 1234
#     def __str__(self):
#         return self.name


# class ClientContacts(models.Model):
#     company = models.ForeignKey(ClientCompany, related_name="contacts", on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     position = models.CharField(max_length=100, blank=True, null=True)
#     is_primary = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.get_full_name()} ({self.company.name})"

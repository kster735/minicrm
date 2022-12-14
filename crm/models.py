from django.db import models

# Create your models here.

class User(models.Model):
    user_firstname = models.CharField(max_length=255)
    user_lastname = models.CharField(max_length=255, null=True)
    user_email = models.CharField(max_length=255)
    user_username = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_phone = models.CharField(max_length=255)
    user_photo = models.CharField(max_length=255)
    user_type = models.IntegerField(default=0)
    user_level_access = models.IntegerField(default=0)
    user_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_username

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_firstname = models.CharField(max_length=255)
    contact_lastname = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255, null=True)
    contact_mobile = models.CharField(max_length=255, null=True)
    contact_address = models.CharField(max_length=255)
    contact_company = models.CharField(max_length=255)
    contact_vat_no = models.CharField(max_length=9, null=True)
    contact_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.contact_firstname + " " + self.contact_lastname + ",      Εταιρεία: " + self.contact_company

class Message(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    message_title = models.CharField(max_length=255)
    message_content = models.CharField(max_length=255)
    message_datetime = models.DateTimeField()
    message_channel = models.CharField(max_length=255)
    message_due_datetime = models.DateTimeField(max_length=255)
    message_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.message_title

class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    message_file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.message_file_name

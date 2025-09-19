from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Project Manager'),
        ('engineer', 'Field Engineer'),
        ('client', 'Client'),
        ('accounts', 'Accounts Team'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class ClientCompany(models.Model):   # or maybe named Client?
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class ClientContact(models.Model):
    company = models.ForeignKey(ClientCompany, on_delete=models.CASCADE, related_name='contacts')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    position = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company.name}"

class EngineerProfile(models.Model):
    SKILL_LEVEL = (
        ('junior', 'Junior'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'engineer'})
    employee_id = models.CharField(max_length=20, unique=True)
    skills = models.ManyToManyField('Skill', blank=True)
    skill_level = models.CharField(max_length=10, choices=SKILL_LEVEL, default='mid')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    max_hours_per_week = models.PositiveIntegerField(default=40)
    current_location = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.DurationField()  # in minutes
    required_skills = models.ManyToManyField(Skill, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_STATUS = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    )
    
    PRIORITY_LEVEL = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    job_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    client = models.ForeignKey(ClientCompany, on_delete=models.CASCADE)
    client_contact = models.ForeignKey(ClientContact, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_engineer = models.ForeignKey(EngineerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_jobs')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVEL, default='medium')
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='pending')
    scheduled_date = models.DateTimeField()
    estimated_duration = models.DurationField()  # in minutes
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    location = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_jobs')
    
    def save(self, *args, **kwargs):
        # Set updated_by if not set during creation
        if not self.pk:  # New object being created
            self.updated_by = self.created_by
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.job_id} - {self.title}"

class JobNote(models.Model):
    NOTE_TYPE = (
        ('text', 'Text Note'),
        ('voice', 'Voice Note'),
        ('image', 'Image Note'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE, default='text')
    content = models.TextField()
    audio_file = models.FileField(upload_to='job_notes/audio/', null=True, blank=True)
    image = models.ImageField(upload_to='job_notes/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Note for {self.job.job_id} by {self.author.username}"
    
class TimeLog(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='time_logs')
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  # in minutes
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_time_logs')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Time log for {self.job.job_id} by {self.engineer.user.username}"

class Expense(models.Model):
    EXPENSE_CATEGORIES = (
        ('transport', 'Transportation'),
        ('materials', 'Materials'),
        ('meals', 'Meals'),
        ('accommodation', 'Accommodation'),
        ('tools', 'Tools & Equipment'),
        ('other', 'Other'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='expenses')
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES, default='other')
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.ImageField(upload_to='expense_receipts/', null=True, blank=True)
    date_incurred = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - ${self.amount} for {self.job.job_id}"
class Invoice(models.Model):
    INVOICE_STATUS = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )
    
    invoice_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='invoice')
    client = models.ForeignKey(ClientCompany, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hours_worked = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.hours_worked and self.rate_per_hour:
            self.subtotal = self.hours_worked * self.rate_per_hour
            self.total_amount = self.subtotal + self.tax_amount
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.invoice_number} - {self.client.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('digital_wallet', 'Digital Wallet'),
    )
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_date = models.DateTimeField()
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='processed_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of ${self.amount} for {self.invoice.invoice_number}"

class GeoLocation(models.Model):
    engineer = models.ForeignKey(EngineerProfile, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accuracy = models.FloatField(null=True, blank=True)  # in meters
    timestamp = models.DateTimeField()
    address = models.TextField(blank=True)
    is_manual = models.BooleanField(default=False)  # Whether the location was manually entered
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.engineer.user.username} at {self.latitude}, {self.longitude}"

class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('job_assigned', 'Job Assigned'),
        ('job_updated', 'Job Updated'),
        ('job_completed', 'Job Completed'),
        ('invoice_sent', 'Invoice Sent'),
        ('payment_received', 'Payment Received'),
        ('system', 'System Notification'),
        ('alert', 'Alert'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_object_type = models.CharField(max_length=50, blank=True)  # e.g., 'job', 'invoice'
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"

class ServiceContract(models.Model):
    CONTRACT_STATUS = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    )
    
    contract_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    client = models.ForeignKey(ClientCompany, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='draft')
    value = models.DecimalField(max_digits=12, decimal_places=2)
    terms = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_contracts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.contract_number:
            # Generate a unique contract number
            self.contract_number = f"CNTR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    def get_related_expense(self):
        from .models import Expense
        try:
            if self.related_object_type == 'expense' and self.related_object_id:
                return Expense.objects.get(id=self.related_object_id)
        except Expense.DoesNotExist:
            return None
        return None
    
    def __str__(self):
        return f"{self.contract_number} - {self.client.name}"

class ContractService(models.Model):
    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE, related_name='services')
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service_type.name} for {self.contract.contract_number}"
    
# billing/models.py
from django.db import models
from django.conf import settings

class DraftEmail(models.Model):
    engineer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Draft to {self.recipient} ({self.subject})"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, ClientCompany, ClientContact, EngineerProfile, Skill, 
    ServiceType, Job, JobNote, TimeLog, Expense, Invoice, InvoiceItem, 
    Payment, GeoLocation, Notification, ServiceContract, ContractService
)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'address', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone', 'address', 'profile_picture')}),
    )

# Inline Admin Classes
class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 1

class JobNoteInline(admin.TabularInline):
    model = JobNote
    extra = 1

class TimeLogInline(admin.TabularInline):
    model = TimeLog
    extra = 1

class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 1

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

class ContractServiceInline(admin.TabularInline):
    model = ContractService
    extra = 1

# Model Admin Classes
class ClientCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'contact_phone', 'industry', 'is_active']
    list_filter = ['industry', 'is_active']
    search_fields = ['name', 'contact_email']
    inlines = [ClientContactInline]

class EngineerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'skill_level', 'hourly_rate', 'is_available']
    list_filter = ['skill_level', 'is_available']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    filter_horizontal = ['skills']

class JobAdmin(admin.ModelAdmin):
    list_display = ['job_id', 'title', 'client', 'service_type', 'status', 'priority', 'scheduled_date']
    list_filter = ['status', 'priority', 'service_type']
    search_fields = ['job_id', 'title', 'client__name']
    date_hierarchy = 'scheduled_date'
    inlines = [JobNoteInline, TimeLogInline, ExpenseInline]

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'issue_date', 'due_date', 'status', 'total_amount']
    list_filter = ['status', 'issue_date']
    search_fields = ['invoice_number', 'client__name']
    date_hierarchy = 'issue_date'
    inlines = [InvoiceItemInline, PaymentInline]

class ServiceContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'client', 'start_date', 'end_date', 'status', 'value']
    list_filter = ['status', 'start_date']
    search_fields = ['contract_number', 'client__name']
    date_hierarchy = 'start_date'
    inlines = [ContractServiceInline]

# Simple Model Admins (no custom configuration needed)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

class JobNoteAdmin(admin.ModelAdmin):
    list_display = ['job', 'author', 'note_type', 'created_at']
    list_filter = ['note_type', 'created_at']
    search_fields = ['job__job_id', 'author__username']

class TimeLogAdmin(admin.ModelAdmin):
    list_display = ['job', 'engineer', 'start_time', 'end_time', 'duration', 'is_approved']
    list_filter = ['is_approved', 'start_time']
    search_fields = ['job__job_id', 'engineer__user__username']

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['job', 'engineer', 'category', 'amount', 'date_incurred', 'is_approved']
    list_filter = ['category', 'is_approved', 'date_incurred']
    search_fields = ['job__job_id', 'engineer__user__username']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'payment_date']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['invoice__invoice_number']

class GeoLocationAdmin(admin.ModelAdmin):
    list_display = ['engineer', 'latitude', 'longitude', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['engineer__user__username']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']

# Register all models - ONLY ONCE per model
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClientCompany, ClientCompanyAdmin)
admin.site.register(ClientContact)
admin.site.register(EngineerProfile, EngineerProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(ServiceType)
admin.site.register(Job, JobAdmin)
admin.site.register(JobNote, JobNoteAdmin)
admin.site.register(TimeLog, TimeLogAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(GeoLocation, GeoLocationAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ServiceContract, ServiceContractAdmin)
admin.site.register(ContractService)
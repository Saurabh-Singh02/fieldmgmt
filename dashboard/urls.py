from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),  # root URL
    path('redirect/', views.redirect_dashboard, name='redirect_dashboard'),

    # Dashboards
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('engineer/', views.engineer_dashboard, name='engineer_dashboard'),
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('accounts/', views.accounts_dashboard, name='accounts_dashboard'),

    # API Endpoints
    path('api/update-availability/', views.update_availability, name='update_availability'),
    path('api/check-in/', views.check_in_location, name='check_in_location'),
    path('api/notifications/unread-count/', views.get_unread_notifications_count, name='unread_notifications_count'),
    path('api/engineer/dashboard-data/', views.engineer_dashboard_data, name='engineer_dashboard_data'),
    path('api/engineer/update-job-status/', views.update_job_status_d, name='update_job_status_d'),

    # Manager Jobs
    path('manager/jobs/', views.manager_jobs, name='manager_jobs'),
    path('manager/jobs/add/', views.add_job, name='add_job'),
    path('manager/jobs/<int:job_id>/', views.job_detail, name='manager_job_detail'),
    path('manager/jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('manager/jobs/<int:job_id>/assign-engineer/', views.assign_engineer, name='assign_engineer'),
    path('manager/jobs/<int:job_id>/update-schedule/', views.update_schedule, name='update_schedule'),
    path('manager/jobs/<int:job_id>/add-note/', views.add_job_note_manager, name='add_job_note_manager'),

    # Manager Engineers
    path('manager/engineers/', views.manager_engineers, name='manager_engineers'),
    path('manager/engineers/add/', views.add_engineer, name='add_engineer'),
    path('manager/engineers/<int:engineer_id>/', views.engineer_detail, name='engineer_detail'),
    path('manager/engineers/<int:engineer_id>/edit/', views.edit_engineer, name='edit_engineer'),
    path('manager/engineers/<int:engineer_id>/toggle-availability/', views.toggle_engineer_availability, name='toggle_engineer_availability'),

    # Manager Notifications
    path('manager/job-updates/', views.manager_job_updates, name='manager_job_updates'),
    path('manager/notifications/', views.manager_job_updates, name='manager_notifications'),
    path('manager/real-time-updates-page/', views.manager_job_updates_real_time_page, name='manager_real_time_updates_page'),

    # Engineer Jobs
    path('engineer/jobs/', views.engineer_jobs, name='engineer_jobs'),
    path('engineer/jobs/<int:job_id>/', views.engineer_job_detail, name='engineer_job_detail'),
    path('engineer/jobs/<int:job_id>/update-status/', views.update_job_status, name='update_job_status'),
    path('engineer/jobs/<int:job_id>/add-note/', views.add_job_note, name='add_job_note'),
    path('engineer/jobs/<int:job_id>/log-time/', views.log_time, name='log_time'),
    path('engineer/jobs/<int:job_id>/add-voice-note/', views.add_voice_note, name='add_voice_note'),
    path('engineer/jobs/<int:job_id>/add-image-note/', views.add_image_note, name='add_image_note'),
    path('engineer/jobs/<int:job_id>/add-expense/', views.add_expense, name='add_expense'),
    path('engineer/jobs/<int:job_id>/capture-photo/', views.capture_photo, name='capture_photo'),
    path('engineer/jobs/<int:job_id>/record-audio/', views.record_audio, name='record_audio'),
    path('engineer/jobs/<int:job_id>/check-in-location/', views.check_in_location, name='check_in_location'),

    # Engineer Utilities
    path('engineer/get-location/', views.get_current_location, name='get_current_location'),
    path('engineer/log-time/', views.log_time_d, name='log_time_d'),
    path('engineer/timesheet/', views.timesheet, name='timesheet'),
    path('engineer/expense-report/', views.expense_report, name='expense_report'),

    # Shared Routes
    path('timesheet/', views.timesheet, name='global_timesheet'),
    path('expense-report/', views.expense_report, name='global_expense_report'),

    # Job Detail (⚠️ choose one type, uuid or int)
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    # path('jobs/<uuid:job_id>/', views.job_detail, name='job_detail_uuid'),

    # Reports
    path('reports/manager/', views.manager_report, name='manager_report'),
    path('reports/engineer/', views.engineer_report_view, name='engineer_report'),

    # Clients
    path("clients/", views.client_list, name="client_list"),
    path("clients/add/", views.client_add, name="client_add"),
    path("clients/<int:pk>/", views.client_detail, name="client_detail"),

    # CSV Upload
    path('manager/upload-engineers/', views.upload_engineer_csv, name='upload_engineer_csv'),
]

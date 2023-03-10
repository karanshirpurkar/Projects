
from django.contrib import admin
from django.urls import path, include
from app import views

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Dashboard Pro"
admin.site.site_title = "Developer Admin Portal"
admin.site.index_title = "Welcome to DashBoard Pro Researcher Portal"

urlpatterns = [
    path("home", views.index, name='home'),
    path("pricing", views.pricing, name='pricing'),
    path("feature", views.feature, name='feature'),
    path("service", views.service, name='service'),
    path("register", views.register, name='register'),
    path("login", views.login_user, name='login'),
    path("chart", views.chart, name='Chart'),
    path("show", views.show, name='show'),
    path("linechart", views.linechart, name='Line Chart'),
    path("barchart", views.barchart, name='Bar Chart'),
    path("scatterchart", views.scatterchart, name='Scatter Chart'),
    path("uploadfile", views.uploadfile, name='Upload File'),
    path("filename", views.get_name, name='File Name'),
    path("piechart", views.piechart, name='Pie Chart'),
    path("boxchart", views.boxchart, name='Box Chart'),
    path("violinechart", views.violinechart, name='Violine Chart'),
    path("scatter3dchart", views.scatter3dchart, name='Scatter 3D Chart'),
    path("line3dchart", views.line3dchart, name='Line 3D Chart'),
    path("dashboard", views.dashboard, name='Dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

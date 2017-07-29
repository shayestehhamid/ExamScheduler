"""opt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from optimizer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^projects/', views.projects),
    url(r'^removeproject/([\w{}]{1,40})/', views.project_remove),
    url(r'^teachers/', views.teachers),
    url(r'^removeteacher/([\w{}]{1,40})/', views.teacher_remove),
    url(r'^removecourse/([\w{}]{1,40})/', views.course_remove),
    url(r'^project/time/([\w{}]{1,40})/', views.times),
    url(r'^removetime/([\w{}]{1,40})/([\w{}]{1,40})/', views.time_remove),
    url(r'^project/course/([\w{}]{1,40})/', views.courses),
    url(r'^project/const/([\w{}]{1,40})/', views.constraint),
    url(r'^project/upload/([\w{}]{1,40})/', views.upload_courses),
    url(r'^project/students/([\w{}]{1,40})/([\w{}]{1,40})/', views.course),
    url(r'^result/([\w{}]{1,40})/', views.result),
    url(r'^course/setteacher/([\w{}]{1,40})/([\w{}]{1,40})', views.set_teacher),
    url(r'^inter/([\w{}]{1,40})/([\w{}]{1,40})/', views.inter),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

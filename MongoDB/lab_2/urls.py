"""lab_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.renderIndex, name='index'),
    url(r'^api/school', views.school, name='school'),
    url(r'^api/db', views.fill_database, name='db'),
    url(r'^api/student', views.student, name='student'),
    url(r'^api/search', views.search, name='student'),
    url(r'^api/rating', views.rating, name='rating'),
    url(r'^api/exam', views.exam, name='exam'),
    url(r'^api/category', views.category, name='category'),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


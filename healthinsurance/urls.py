"""healthinsurance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from insurance import views as ins_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ins_views.home_page_view,name= 'home_page'),
    path('customer/',include('customer.urls')),
    path('after_login', ins_views.after_login_view,name='after_login'),
    path('logout', LogoutView.as_view(template_name='home/base.html'),name='logout'),
    path('policy-types', ins_views.policy_types_view,name='policy_types'),
    path('get-premium-policy/<int:pk>', ins_views.get_premium_policy_view, name='get_premium_policy')
]

from django.urls import path
from django.contrib.auth.views import LoginView
from customer import views

urlpatterns = [
    path('login', LoginView.as_view(template_name='home/login.html'),name='login_page'),
    path('signup', views.signup_page_view, name = 'customer_signup'),
    path('dashboard', views.customer_dashboard_view, name='customer_dashboard'),
    path('apply-policy',views.apply_policy, name='apply_policy'),
    path('dependents', views.add_dependents_view, name='add_dependent'),
    path('claim-insurance/<int:pk>', views.claim_insurance, name='claim_insurance'),
    path('renew_policy/<int:pk>', views.upgrade_policy, name='renew_policy')
]
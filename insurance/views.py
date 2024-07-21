from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import PolicyPremium
# Create your views here.
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')  
    return render(request,'home/base.html')

def after_login_view(request):
    if is_customer(request.user):
        return redirect('customer/dashboard')
    return redirect('/admin/')

def is_customer(user):
    return user.groups.filter(name='INSURANCE_USER').exists()

def policy_types_view(request):
    return render(request, 'home/policy_types.html')

def get_premium_policy_view(request, pk):
    print('policy_premium id: ', pk)
    policy_premium = PolicyPremium.objects.get(id=pk)
    data = {
        'policy': policy_premium.policy.display_name(),
        'premium_type':policy_premium.premium_type,
        'premium_amount': policy_premium.premium_amount,
        'sum_assurance':policy_premium.policy.sum_assurance,
        'number_of_hospitals':policy_premium.number_of_hospitals,
        'tier':policy_premium.tier
    }
    print('data: ', data)
    return JsonResponse(data)
    
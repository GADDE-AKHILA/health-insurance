from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from . import forms as CFORM
from .import models as CMODEL
from insurance import forms as HFORM
from insurance import models as HMODEL
from health_core.helper import date_time_helper
from health_core.helper import data_helper
from health_core.validators import health_policy_validator
from health_core.validators import dependents_validator
from health_core.validators import claim_validator
from health_core.exceptions.health_exception import HealthPolicyException, DependentException, ClaimException
def signup_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('after_login')
    user_form = CFORM.UserForm()
    customer_form = CFORM.CustomerForm()
    data = {'userForm': user_form, 'customerForm':customer_form}
    return render(request,'home/signup.html', data)

def customer_dashboard_view(request):
    health_policies = data_helper.get_user_policies(request.user, HMODEL.HealthPolicy)
    claims = data_helper.get_user_claims(health_policies, HMODEL.Claim)
    pending_claims_amount = data_helper.get_claims_amount_by_status(health_policies, HMODEL.Claim, 'Pending')
    total_claim_amount, total_assurance =  data_helper.get_total_claim_amount(health_policies, HMODEL.Claim)
    metrics = {'total_policies': health_policies.count(), 
               'pending_claims_amount': pending_claims_amount, 
               'total_claim_amount':total_claim_amount,
               'approved_claims_amount' : data_helper.get_claims_amount_by_status(health_policies, HMODEL.Claim, 'Approved'),
                'balance_amount':total_assurance-total_claim_amount}
    data = {'customer':get_customer(request.user), 
            'health_policies': health_policies,
            'claims': claims, 'metrics':metrics}
    print('dashboard data: ', data)
    return render(request, 'customer/dashboard.html', data)

def apply_policy(request):
    health_policy_form = HFORM.HealthPolicyForm()
    try:
        if request.method == 'POST':
            health_policy_form = HFORM.HealthPolicyForm(request.POST)
            if health_policy_form.is_valid:
                health_policy = health_policy_form.save(commit=False)
                policy_premium = health_policy.policy_premium
                health_policy.premium_paid = policy_premium.premium_amount
                health_policy.start_date = date_time_helper.today()
                health_policy.end_date = date_time_helper.today_plus_year()
                if not health_policy_validator.is_user_policy_exists(request.user, policy_premium, HMODEL.HealthPolicy):
                    health_policy.user = request.user
                    health_policy.save()
                    health_policy_form.save_m2m()
                    return HttpResponseRedirect('/customer/dashboard')
                else:
                    messages.error(request, 'User already registered to this policy')
            else:
                print('health_policy_form_errors: ', health_policy_form.errors)
                messages.error(request, health_policy_form.errors)
    except HealthPolicyException as e:
        messages.error(request, str(e))
    except Exception as e:
        print('exception ', e)
        messages.error(request, 'Unable to apply policy')
    data = {'form' : health_policy_form, 'customer' :get_customer(request.user)}
    return render(request, 'customer/apply_policy.html', data)

def claim_policy_view(request, pk):
    data = {'customer': get_customer(request.user)}
    return render(request, 'customer/claim_policy.html', data)

def add_dependents_view(request):
    form = HFORM.DependentForm()
    try:
        if request.method == 'POST':
            form = HFORM.DependentForm(request.POST)
            if form.is_valid():
                dependent = form.save(commit=False)
                dependent.user = request.user
                dependents_validator.check_dependent(dependent, HMODEL.Dependent.objects)
                dependent.save()
            else:
                messages.error(request, form.errors)
    except DependentException as e:
        messages.error(request, str(e))
    except Exception as e:
        print('Exception :', e)
        messages.error(request, 'Error occured!')
    dependents = data_helper.get_dependents(request.user, HMODEL.Dependent)
    data = {'customer':get_customer(request.user), 'dependents': dependents, 'form': form}
    return render(request, 'customer/add_dependents.html', data)

def claim_insurance(request, pk):
    policy = data_helper.get_health_policy(HMODEL.HealthPolicy, pk)
    total_claim_amount, _ = data_helper.get_total_claim_amount([policy], HMODEL.Claim)
    try:
        if request.method == 'POST':
            form = HFORM.ClaimForm(request.POST)
            if form.is_valid():
                claim = form.save(commit=False)
                claim.policy = policy
                claim.claim_date = date_time_helper.today()
                claim.status = 'Pending'
                claim_validator.validate_claim_insurance(policy, claim, total_claim_amount)
                claim.save()
                return HttpResponseRedirect('/customer/dashboard')
            else:
                messages.error(request, form.errors)
    except ClaimException as e:
        messages.error(request, str(e))
    except Exception as e:
        print('unable to claim: ',e)
        messages.error(request, 'unable to claim')

    hpolicy ={
        'policy_premium': policy.policy_premium,
        'amount_claimed':total_claim_amount,
        'end_date': policy.end_date,
        'premium_paid': policy.premium_paid
    }
    form = HFORM.ClaimForm()
    data = {'customer': get_customer(request.user), 'form': form, 'policy' : hpolicy}
    return render(request, 'customer/claim_policy.html', data)

def upgrade_policy(request, pk):
    pass
def get_customer(user):
    return CMODEL.Customer.objects.get(user = user)
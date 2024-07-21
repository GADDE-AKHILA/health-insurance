from django import forms
from .models import Policy, PolicyPremium, HealthPolicy, Dependent, Claim
from health_core.validators import health_policy_validator
from health_core.validators import dependents_validator as dependent_validator
class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['policy_type', 'sum_assurance']

class PolicyPremiumForm(forms.ModelForm):
    class Meta:
        model = PolicyPremium
        fields = ['policy', 'premium_type', 'premium_amount', 'tier', 'number_of_hospitals']


class HealthPolicyForm(forms.ModelForm):
    class Meta:
        model = HealthPolicy
        fields = ['policy_premium', 'dependents']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'dependents': forms.SelectMultiple,
        }
    def clean(self):
        cleaned_data = super().clean()
        policy_premium = cleaned_data.get('policy_premium')
        dependents = cleaned_data.get('dependents')
        health_policy_validator.validate_dependents(policy_premium, dependents)
        return cleaned_data

class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = ['name', 'relation', 'age']
    def clean(self):
        cleaned_data = super().clean()
        relation = cleaned_data.get('relation')
        age = cleaned_data.get('age')
        dependent_validator.validate_depenent(relation, age)
        return cleaned_data

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['dependent', 'claim_amount', 'hospital', 'details']
        widgets = {
            'claim_date': forms.DateInput(attrs={'type': 'date'}),
        }   

class UpgradePolicyForm(forms.ModelForm):
    class Meta:
        model = HealthPolicy
        fields = ['policy_premium']
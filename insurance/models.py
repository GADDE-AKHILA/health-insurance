from django.db import models
from django.contrib.auth.models import User
class Policy(models.Model):
    POLICY_TYPE_CHOICES = [
        ('Individual', 'Health Individual'),
        ('Family', 'Health Family'),
        ('Senior', 'Health Senior Citizens'),
    ]
    # id=models.AutoField(primary_key=True, default= random.randint)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPE_CHOICES, default="Individual")
    sum_assurance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.get_policy_type_display()}"
    def display_name(self):
        return f"{self.get_policy_type_display()}"
    
class PolicyPremium(models.Model):
    PREMIUM_CHOICES = [
        ('Gold', 'Gold'),
        ('Diamond', 'Diamond'),
        ('Platinum', 'Platinum'),
    ]
    # id = models.AutoField(primary_key=True, default= random.randint)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='premiums')
    premium_type = models.CharField(max_length=20, choices=PREMIUM_CHOICES, default="Gold")
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tier = models.PositiveIntegerField()
    number_of_hospitals = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.policy} - {self.get_premium_type_display()}"
    
class HealthPolicy(models.Model):
    policy_premium = models.ForeignKey(PolicyPremium, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_policy', default=None)
    premium_paid = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    start_date = models.DateField()
    end_date = models.DateField()
    dependents = models.ManyToManyField('Dependent', related_name='policies')

    def __str__(self):
        return f"{self.policy_premium.policy} - {self.policy_premium.premium_type} - {self.end_date}"
    def get_claims(self):
        return Claim.objects.filter(policy=self)
    def add_claim(self, claim_amount, claim_date, dependent, hospital):
        claim = Claim(policy=self, claim_amount=claim_amount, claim_date=claim_date, dependent =dependent, hospital=hospital)
        claim.save()
    def total_claim_amount(self):
        return self.get_claims().aggregate(models.Sum('claim_amount'))['claim_amount__sum'] or 0

class Dependent(models.Model):
    RELATION_CHOICES = [
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
        ('Parent', 'Parent'),
        ('Sibling', 'Sibling'),
        ('Self', 'Self'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dependents')
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    age = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.name} ({self.relation})"

class Claim(models.Model):
    CLAIM_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    policy = models.ForeignKey(HealthPolicy, on_delete=models.CASCADE)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_date = models.DateField()
    hospital =  models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices= CLAIM_STATUS, default='Pending')
    dependent = models.ForeignKey(Dependent, on_delete=models.CASCADE)
    details = models.CharField(max_length=200)
    def __str__(self):
        return f"Claim #{self.pk} - Amount: {self.claim_amount}, Date: {self.claim_date}"
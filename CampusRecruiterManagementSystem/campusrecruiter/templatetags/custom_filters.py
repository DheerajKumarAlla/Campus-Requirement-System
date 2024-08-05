from django import template
from campusrecruiter.models import *
register = template.Library()

@register.simple_tag()
def vacancycount(id):
    company = Company.objects.get(id=id)
    totalvacancy = Vacancy.objects.filter(companies = company).count()
    return totalvacancy

@register.simple_tag()
def applicationcount(jobtitle,user):
    company = Company.objects.get(user=user)
    #vacancy = Vacancy.objects.filter(companies = company, JobTitle="yes")


    totalapplyjob = Applyjob.objects.filter(vacancy__in=Vacancy.objects.filter(companies=company,JobTitle=jobtitle)).count()
    return totalapplyjob

@register.filter(name='lastapplied')
def lastapplied(data):
    candidate = Candidate.objects.get(id=data)
    apply = Applyjob.objects.filter(candidate=candidate)
    return apply.last().vacancy.companies.user.first_name
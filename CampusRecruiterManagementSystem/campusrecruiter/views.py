
from django.db.models import Max, Q, query, QuerySet
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, timedelta, time
from datetime import date


# Create your views here.

def index(request):
    vacancy = Vacancy.objects.all()
    return render(request, 'index.html', locals())

def jobDetails(request,pid):
    vacancy = Vacancy.objects.get(id=pid)
    return render(request, 'jobDetails.html', locals())


# ===================== Candidate View Here =====================

def candidate(request):

    try:
        studentid = 1001 if Candidate.objects.count() == 0 else Candidate.objects.aggregate(max=Max('StudentID'))["max"] + 1
        error = ""
        if request.method == "POST":
            fname = request.POST['FirstName']
            lname = request.POST['LastName']
            mob = request.POST['MobileNumber']
            gender = request.POST['Gender']
            email = request.POST['email']
            pwd = request.POST['password']
            try:
                user = User.objects.create_user(username=email, password=pwd, first_name=fname, last_name=lname)
                Candidate.objects.create(user=user, StudentID=studentid, MobileNumber=mob, Gender=gender)
                error = "no"
            except:
                error = "yes"
    except:
        if request.method == 'POST':
            e = request.POST['email']
            p = request.POST['password']
            user = authenticate(username=e, password=p)
            try:
                if user:
                    login(request, user)
                    error1 = "no"
                else:
                    error1 = "yes"
            except:
                error1 = "yes"
    return render(request, 'candidate.html', locals())


def canDashboard(request):
    if not request.user.is_authenticated:
        return redirect('candidate')

    user = request.user
    candidates = Candidate.objects.get(user=user)

    today = datetime.now().date()
    yesterday = today - timedelta(1)
    lasts = today - timedelta(7)

    todayapply = Applyjob.objects.filter(ApplyDate=today,candidate=candidates).count()
    yesterdayapply = Applyjob.objects.filter(ApplyDate=yesterday,candidate=candidates).count()
    lastsevendayapply = Applyjob.objects.filter(ApplyDate=lasts,candidate=candidates).count()
    totalapply = Applyjob.objects.filter(candidate=candidates).count()
    totalvacancy = Vacancy.objects.all().count()

    return render(request, 'canDashboard.html', locals())

def studentProfile(request):
    if not request.user.is_authenticated:
        return redirect('candidate')

    user = User.objects.get(id=request.user.id)
    candidate = Candidate.objects.get(user=user)

    if request.method == "POST":
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        MobileNumber = request.POST['MobileNumber']
        Gender = request.POST['Gender']
        Age = request.POST['Age']
        DOB = request.POST['DOB']

        candidate.user.first_name = fname
        candidate.user.last_name = lname
        candidate.MobileNumber = MobileNumber
        candidate.Gender = Gender
        candidate.Age = Age
        candidate.DOB = DOB

        try:
            candidate.save()
            candidate.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            Image = request.FILES['Image']
            candidate.Image = Image
            candidate.save()
        except:
            pass
    return render(request, 'studentProfile.html', locals())


def addFormDetail(request):
    if not request.user.is_authenticated:
        return redirect('candidate')
    user = request.user
    try:
        education = Education.objects.get(user=user)
    except:
        pass
    try:
        
        user = User.objects.get(id=request.user.id)
        candidates = Candidate.objects.get(user=user)

        error = ""
        if request.method == "POST":
            secondaryBoard = request.POST['SecondaryBoard']
            secondaryBoardyop = request.POST['SecondaryBoardyop']
            secondaryBoardper = request.POST['SecondaryBoardper']
            secondaryBoardcgpa = request.POST['SecondaryBoardcgpa']
            sSecondaryBoard = request.POST['SSecondaryBoard']
            sSecondaryBoardyop = request.POST['SSecondaryBoardyop']
            sSecondaryBoardper = request.POST['SSecondaryBoardper']
            sSecondaryBoardcgpa = request.POST['SSecondaryBoardcgpa']
            graUni = request.POST['GraUni']
            graUniyop = request.POST['GraUniyop']
            graUnidper = request.POST['GraUnidper']
            graUnicgpa = request.POST['GraUnicgpa']
            pGUni = request.POST['PGUni']
            PGUniyop = request.POST['PGUniyop']
            PGUniper = request.POST['PGUniper']
            PGUnicgpa = request.POST['PGUnicgpa']
            ExtraCurriculars = request.POST['ExtraCurriculars']
            OtherAchivement = request.POST['OtherAchivement']

            try:
                Education.objects.create(user=user,
                                         SecondaryBoard=secondaryBoard, SecondaryBoardyop=secondaryBoardyop,
                                         SecondaryBoardper=secondaryBoardper, SecondaryBoardcgpa=secondaryBoardcgpa,
                                         SSecondaryBoard=sSecondaryBoard, SSecondaryBoardyop=sSecondaryBoardyop,
                                         SSecondaryBoardper=sSecondaryBoardper, SSecondaryBoardcgpa=sSecondaryBoardcgpa,
                                         GraUni=graUni, GraUniyop=graUniyop, GraUnidper=graUnidper,
                                         GraUnicgpa=graUnicgpa,
                                         PGUni=pGUni, PGUniyop=PGUniyop, PGUniper=PGUniper, PGUnicgpa=PGUnicgpa,
                                         ExtraCurriculars=ExtraCurriculars, OtherAchivement=OtherAchivement)
                error = "no"
            except:
                error = "yes"
    except:
        pass
    return render(request, 'addFormDetail.html', locals())


def manageFormDetail(request):
    if not request.user.is_authenticated:
        return redirect('candidate')

    user = request.user
    try:
        education = Education.objects.get(user=user)
    except:
        pass

    if request.method == "POST":
        SecondaryBoard = request.POST['SecondaryBoard']
        SecondaryBoardyop = request.POST['SecondaryBoardyop']
        SecondaryBoardper = request.POST['SecondaryBoardper']
        SecondaryBoardcgpa = request.POST['SecondaryBoardcgpa']

        SSecondaryBoard = request.POST['SSecondaryBoard']
        SSecondaryBoardyop = request.POST['SSecondaryBoardyop']
        SSecondaryBoardper = request.POST['SSecondaryBoardper']
        SSecondaryBoardcgpa = request.POST['SSecondaryBoardcgpa']

        GraUni = request.POST['GraUni']
        GraUniyop = request.POST['GraUniyop']
        GraUnidper = request.POST['GraUnidper']
        GraUnicgpa = request.POST['GraUnicgpa']

        PGUni = request.POST['PGUni']
        PGUniyop = request.POST['PGUniyop']
        PGUniper = request.POST['PGUniper']
        PGUnicgpa = request.POST['PGUnicgpa']

        ExtraCurriculars = request.POST['ExtraCurriculars']
        OtherAchivement = request.POST['OtherAchivement']

        education.SecondaryBoard = SecondaryBoard
        education.SecondaryBoardyop = SecondaryBoardyop
        education.SecondaryBoardper = SecondaryBoardper
        education.SecondaryBoardcgpa = SecondaryBoardcgpa

        education.SSecondaryBoard = SSecondaryBoard
        education.SSecondaryBoardyop = SSecondaryBoardyop
        education.SSecondaryBoardper = SSecondaryBoardper
        education.SSecondaryBoardcgpa = SSecondaryBoardcgpa

        education.GraUni = GraUni
        education.GraUniyop = GraUniyop
        education.GraUnidper = GraUnidper
        education.GraUnicgpa = GraUnicgpa

        education.PGUni = PGUni
        education.PGUniyop = PGUniyop
        education.PGUniper = PGUniper
        education.PGUnicgpa = PGUnicgpa

        education.ExtraCurriculars = ExtraCurriculars
        education.OtherAchivement = OtherAchivement

        try:
            education.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'manageFormDetail.html', locals())


def viewVacancy(request):
    if not request.user.is_authenticated:
        return redirect('candidate')
    vacancy = Vacancy.objects.all()
    user = request.user
    candidate = Candidate.objects.get(user = user)

    appliedjob = Applyjob.objects.filter(candidate=candidate)

    li = []
    for i in appliedjob:
        li.append(i.vacancy.id)
    return render(request, 'viewVacancy.html', locals())


def viewVacancyDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('candidate')

    vacancy = Vacancy.objects.get(id=pid)

    user = User.objects.get(id=request.user.id)
    candidates = Candidate.objects.get(user=user)

    date1 = date.today()
    if vacancy.LastDate < date1:
        error="close"
    elif vacancy.ApplyDate > date1:
        error="notopen"
    else:
        if request.method == "POST":
            resume = request.FILES['Resume']
            Applyjob.objects.create(vacancy=vacancy, candidate=candidates, Resume=resume, ApplyDate=date.today())
            error="done"
    return render(request, 'viewVacancyDetails.html', locals())


def historyofAppliedJob(request):
    if not request.user.is_authenticated:
        return redirect('candidate')
    user = request.user
    candidates = Candidate.objects.get(user=user)
    applyjob = Applyjob.objects.filter(candidate=candidates)
    return render(request, 'historyofAppliedJob.html',locals())

def viewHistoryAppliedjob(request, pid):
    if not request.user.is_authenticated:
        return redirect('candidate')

    applyjob = Applyjob.objects.get(id=pid)

    message = Message.objects.filter(appjob=applyjob)
    applyjobid = applyjob.id
    msgcount = Message.objects.filter(appjob=applyjob).count()
    return render(request, 'viewHistoryAppliedjob.html', locals())

def viewEducationDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = User.objects.get(id=pid)
    education = Education.objects.get(user=user)
    return render(request, 'viewEducationDtls.html', locals())


def candbetweenDateReport(request):
    if not request.user.is_authenticated:
        return redirect('candidate')

    user = request.user
    candidates = Candidate.objects.get(user=user)

    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']

        applyjob = Applyjob.objects.filter(Q(ApplyDate__gte=fd) & Q(ApplyDate__lte=td), candidate=candidates)
        return render(request, 'canbetweenReportDtls.html', locals())
    return render(request, 'candbetweenDateReport.html', locals())


def candidateSearchJob(request):
    if not request.user.is_authenticated:
        return redirect('candidate')
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        vacancy = Vacancy.objects.filter(Q(JobTitle__icontains=sd))

        user = request.user
        candidate = Candidate.objects.get(user=user)

        appliedjob = Applyjob.objects.filter(candidate=candidate)

        li = []
        for i in appliedjob:
            li.append(i.vacancy.id)
    return render(request, 'candidateSearchJob.html', locals())

def candidateChangePwd(request):
    if not request.user.is_authenticated:
        return redirect('candidate')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'candidateChangePwd.html', locals())


# =========================== Employers Views Here ===========================

def employees(request):
    try:

        if request.method == "POST":
            comname = request.POST['CompanyName']
            conperson = request.POST['ContactPerson']
            email = request.POST['email']
            pwd = request.POST['password']
            mob = request.POST['MobileNumber']
            comurl = request.POST['CompanyUrl']
            comaddress = request.POST['CompanyAddress']
            comlogo = request.FILES['CompanyLogo']

            try:
                user = User.objects.create_user(username=email, password=pwd, first_name=comname)
                Company.objects.create(user=user, ContactPerson=conperson, MobileNumber=mob, CompanyUrl=comurl,
                                       CompanyAddress=comaddress, CompanyLogo=comlogo)
                error = "no"
            except:
                error = "yes"
    except:
        if request.method == 'POST':
            e = request.POST['email']
            p = request.POST['password']
            user = authenticate(username=e, password=p)
            try:
                if user:
                    login(request, user)
                    error1 = "no"
                else:
                    error1 = "yes"
            except:
                error1 = "yes"
    return render(request, 'employees.html', locals())


def empDashboard(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)
    vacancy = Vacancy.objects.filter(companies=company)

    totalvacancy = Vacancy.objects.filter(companies=company).count()
    #vacancy = Vacancy.objects.filter(companies=company)
    totalapp = Applyjob.objects.filter(vacancy__in=vacancy).count()
    totalNewapp = Applyjob.objects.filter(vacancy__in=vacancy, Status__isnull=True).count()
    totalSelectapp = Applyjob.objects.filter(vacancy__in=vacancy, Status='Sorted').count()
    totalRejectapp = Applyjob.objects.filter(vacancy__in=vacancy, Status='Rejected').count()

    return render(request, 'employee/empDashboard.html', locals())


def comProfile(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = User.objects.get(id=request.user.id)
    company = Company.objects.get(user=user)

    if request.method == "POST":
        comname = request.POST['CompanyName']
        conperson = request.POST['ContactPerson']
        mob = request.POST['MobileNumber']
        comurl = request.POST['CompanyUrl']
        comaddress = request.POST['CompanyAddress']

        company.user.first_name = comname
        company.ContactPerson = conperson
        company.MobileNumber = mob
        company.CompanyUrl = comurl
        company.CompanyAddress = comaddress

        try:
            company.save()
            company.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            comlogo = request.FILES['CompanyLogo']
            company.CompanyLogo = comlogo
            company.save()
        except:
            pass
    return render(request, 'employee/comProfile.html', locals())


def addVacancy(request):
    if not request.user.is_authenticated:
        return redirect('employees')

    user = User.objects.get(id=request.user.id)
    company = Company.objects.get(user=user)
    newVacany = Vacancy.objects.filter(companies=company)

    if request.method == "POST":
        JobTitle = request.POST['JobTitle']
        MonthlySalary = request.POST['MonthlySalary']
        JobDescriptions = request.POST['JobDescriptions']
        JobLocation = request.POST['JobLocation']
        NoofOpenings = request.POST['NoofOpenings']
        ApplyDate = request.POST['ApplyDate']
        LastDate = request.POST['LastDate']

        try:
            Vacancy.objects.create(companies=company,
                                     JobTitle=JobTitle, MonthlySalary=MonthlySalary,
                                     JobDescriptions=JobDescriptions, JobLocation=JobLocation,
                                     NoofOpenings=NoofOpenings, ApplyDate=ApplyDate, LastDate=LastDate)
            error = "no"
        except:
            error = "yes"

    return render(request, 'employee/addVacancy.html', locals())


def manageVacancy(request):
    if not request.user.is_authenticated:
        return redirect('employees')

    user = request.user
    company = Company.objects.get(user=user)
    vacancy = Vacancy.objects.filter(companies=company)

    return render(request, 'employee/manageVacancy.html', locals())

def editVacancy(request,pid):
    if not request.user.is_authenticated:
        return redirect('employees')
    error = ""
    company = Company.objects.all()
    vacancy = Vacancy.objects.get(id=pid)

    if request.method == "POST":
        JobTitle = request.POST['JobTitle']
        MonthlySalary = request.POST['MonthlySalary']
        JobDescriptions = request.POST['JobDescriptions']
        JobLocation = request.POST['JobLocation']
        NoofOpenings = request.POST['NoofOpenings']
        ApplyDate = request.POST['ApplyDate']
        LastDate = request.POST['LastDate']

        vacancy.JobTitle = JobTitle
        vacancy.MonthlySalary = MonthlySalary
        vacancy.JobDescriptions = JobDescriptions
        vacancy.JobLocation = JobLocation
        vacancy.NoofOpenings = NoofOpenings
        vacancy.ApplyDate = ApplyDate
        vacancy.LastDate = LastDate

        try:
            vacancy.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'employee/editVacancy.html', locals())


def newApplication(request):
    if not request.user.is_authenticated:
        return redirect('employees')

    user = request.user
    company = Company.objects.get(user=user)

    vacancy = [i.id for i in Vacancy.objects.filter(companies=company)]
    applyjob = Applyjob.objects.filter(vacancy__in=vacancy, Status=None)

    return render(request, 'employee/newApplication.html', locals())


def sortListedApplication(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)

    vacancy = [i.id for i in Vacancy.objects.filter(companies=company)]
    applyjob = Applyjob.objects.filter(vacancy__in=vacancy, Status="Sorted")
    return render(request, 'employee/sortListedApplication.html', locals())


def rejectApplication(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)

    vacancy = [i.id for i in Vacancy.objects.filter(companies=company)]
    applyjob = Applyjob.objects.filter(vacancy__in=vacancy, Status="Rejected")

    return render(request, 'employee/rejectApplication.html', locals())


def allApplication(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)

    vacancy = [i.id for i in Vacancy.objects.filter(companies=company)]
    applyjob = Applyjob.objects.filter(vacancy__in=vacancy)

    return render(request, 'employee/allApplication.html', locals())

def viewAppliedApplication(request,pid):
    if not request.user.is_authenticated:
        return redirect('employees')
    applyjob = Applyjob.objects.get(id=pid)

    message = Message.objects.filter(appjob=applyjob)
    applyjobid = applyjob.id
    msgcount = Message.objects.filter(appjob=applyjob).count()

    if request.method == "POST":
        Messages = request.POST['Messages']
        Status = request.POST['Status']

        try:
            msg = Message.objects.create(appjob=applyjob, Messages=Messages, Status=Status)
            applyjob.Message = Messages
            applyjob.Status = Status
            applyjob.save()
            error = "no"
        except:
            error = "no"
    return render(request, 'employee/viewAppliedApplication.html', locals())

def viewstudentEduDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = User.objects.get(id=pid)
    education = Education.objects.get(user=user)
    return render(request, 'employee/viewstudentEduDtls.html', locals())

def vacancyReport(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)

    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']

        vacancy = Vacancy.objects.filter(Q(JobpostingDate__gte=fd) & Q(JobpostingDate__lte=td), companies=company)
        return render(request, 'employee/vacancyReportDtls.html', locals())
    return render(request, 'employee/vacancyReport.html', locals())


def applicationCountReport(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    user = request.user
    company = Company.objects.get(user=user)

    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']

        applyjob = Applyjob.objects.filter(Q(ApplyDate__gte=fd) & Q(ApplyDate__lte=td),vacancy__in=Vacancy.objects.filter(companies=company))

        return render(request, 'employee/applicationCountReportDtls.html', locals())
    return render(request, 'employee/applicationCountReport.html', locals())

def employerChangePwd(request):
    if not request.user.is_authenticated:
        return redirect('employees')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'employee/employerChangePwd.html', locals())


# ============================  Admin Here  ===========================

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    totalcompany = Company.objects.all().count()
    totalcandidate = Candidate.objects.all().count()
    totalvacancy = Vacancy.objects.all().count()

    return render(request, 'admin/dashboard.html', locals())

def totalRegCompany(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    company = Company.objects.all()
    return render(request, 'admin/totalRegCompany.html', locals())

def viewCompanyDtls(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    company = Company.objects.get(id=pid)
    return render(request, 'admin/viewCompanyDtls.html', locals())

def totalRegStudent(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    candidate = Candidate.objects.all()
    return render(request, 'admin/totalRegStudent.html', locals())

def viewStudentDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    candidate = Candidate.objects.get(id=pid)
    return render(request, 'admin/viewStudentDtls.html', locals())

def totalVacancy(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vacancy = Vacancy.objects.all()
    return render(request, 'admin/totalVacancy.html', locals())

def viewVacancyDtls(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    vacancy = Vacancy.objects.get(id=pid)
    return render(request, 'admin/viewVacancyDtls.html', locals())

def bwdateComReg(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        company = Company.objects.filter(Q(CompanyRegdate__gte=fd) & Q(CompanyRegdate__lte=td))
        return render(request, 'admin/companydatesReportsDetails.html', locals())
    return render(request, 'admin/bwdateComReg.html', locals())

def admvacancyReport(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']

        company = Company.objects.filter(Q(CompanyRegdate__gte=fd) & Q(CompanyRegdate__lte=td))
        return render(request, 'admin/admvacancyReportDtls.html', locals())
    return render(request, 'admin/admvacancyReport.html', locals())

def adminChangePwd(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/adminChangePwd.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')

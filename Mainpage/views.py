from django.shortcuts import render, redirect, get_object_or_404
from Mainpage.models import *
from django.db.models.functions import ExtractYear
import random
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from datetime import date

def indexpage(request):
    categories = EstimateCategory.objects.all()
    return render(request, 'index.html', {'categories': categories})

def home(request):
    rates = {rate.development_type: rate for rate in CostRates.objects.all()}
    return render(request, 'index.html', {
        'rates': rates
    })

def about(request):
    return render(request,'aboutus.html')

def expertise(request):
    return render(request,'expertise.html')

def projects(request):
    projects = Project.objects.all()


    name_filter = request.GET.get('name')
    year_filter = request.GET.get('year')
    popular_filter = request.GET.get('popular')

    if name_filter:
        projects = projects.filter(name=name_filter)
    if year_filter:
        projects = projects.filter(start_date__year=year_filter)
    if popular_filter:
        projects = projects.filter(name=popular_filter)

    project_names = Project.objects.values_list('name', flat=True).distinct()
    project_years = Project.objects.annotate(year=ExtractYear('start_date')).values_list('year', flat=True).distinct()
    popular_projects = random.sample(list(project_names), min(3, len(project_names)))

    return render(request, 'projects.html', {
        'proj': projects,
        'project_names': project_names,
        'project_years': project_years,
        'popular_projects': popular_projects,
    })

def digital(request):
    return render(request,'digital.html')

def insights(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request,'insight.html',{'blogs': blogs})

def insight_detail(request):
    return render(request,'insight_detail.html')

def insights_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    more_blogs = Blog.objects.exclude(id=blog_id)[:10]
    all_blogs = Blog.objects.all()
    return render(request, 'insight_detail.html', {
        'blog': blog,
        'more_blogs': more_blogs,
        'all_blogs': all_blogs
    })

def contact(request):
    return render(request,"contactus.html")

def careers(request):
    vacant=Vacancy.objects.all()
    return render(request,"career.html")


def contact_view(request):
    submitted = False

    print("received the data")
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        sector = request.POST.get('sector')
        message = request.POST.get('message')

        print("sending it to model")

        query=Query(
            name=name,
            email=email,
            sector=sector,
            message=message
        )

        query.save()
        

        print("saved the data")

        subject = "Thank You for Reaching Out to InfraBuild"
        message_body = f"""
Hi {name},

Thank you for getting in touch with InfraBuild! 🤝

We truly appreciate your interest in our infrastructure solutions 🏗️. Your query has been received ✅ and our team is already reviewing it 🔍.

One of our experts will reach out to you shortly to assist you with the next steps 📞.

If you have any urgent concerns, feel free to contact us at ✉️ support@infrabuild.com or call 📱 +1800-111-222.

Warm regards,  
The InfraBuild Team  
🌐 www.infrabuild.com """


        send_mail(
            subject,
            message_body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        ) 

        submitted = True

    return render(request, 'contactus.html', {'submitted': submitted})

def job_application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        position = request.POST.get('position')
        experience = request.POST.get('experience')
        message = request.POST.get('message')
        resume = request.FILES.get('resume')

        applications=JobApplication(
            name=name,
            email=email,
            phone=phone,
            position=position,
            experience=experience,
            message=message,
            resume=resume
        )
        applications.save()

    return redirect(reverse('careers') + '?submitted=true')

def investors(request):
    all_news = News.objects.order_by('-created_at') 
    return render(request, 'investors.html', {'all_news': all_news})

def news(request):
    all_news = News.objects.all()
    return render(request,'news.html',{'all_news': all_news})

def events(request):
    today = date.today()

    recent_events = Event.objects.filter(date__lt=today).order_by('-date')
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')

    return render(request, 'events.html', {
        'recent_events': recent_events,
        'upcoming_events': upcoming_events
    })

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    related_news = News.objects.exclude(id=news_id).order_by('-created_at')[:5]
    return render(request, 'news_details.html', {
        'news': news_item,
        'related_news': related_news
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    more_projects = Project.objects.exclude(id=project_id)[:6]
    return render(request, 'project_detail.html', {
        'project': project,
        'more_projects': more_projects
    })

def company_profile(request):
    return render(request,'company_profile.html')

def leadership(request):
    return render(request,'leadership.html')

def eco(request):
    return render(request,'eco.html')

def awards(request):
    return render(request,'awards.html')

def Business_Practice(request):
    return render(request,'Business_Practice.html')

def governance(request):
    return render(request,'governance.html')

def estimate(request, category):
    category_obj = get_object_or_404(EstimateCategory, name__iexact=category.replace('-', ' '))
    rates = {rate.development_type: rate for rate in CostRates.objects.all()}
    images = category_obj.images.all()
    return render(request, 'estimate.html', {
        'category': category_obj,
        'images': images,
        'rates': rates
    })

def alert_form_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        language = request.POST.get('language')
        channels = request.POST.getlist('channels')  
        alert_types = request.POST.getlist('alert-types') 
        timing = request.POST.get('timing')
        specific_hours = request.POST.get('specific-hours')

        alert_cus=AlertRegistration(
            name=name,
            email=email,
            phone=phone,
            location=location,
            language=language,
            channels=",".join(channels),
            alert_types=",".join(alert_types),
            timing=timing,
            specific_hours=specific_hours if timing == 'limited' else ''
        )
        
        alert_cus.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        

        return render(request, 'governance.html')
    
    return JsonResponse({'success': False}, status=400)


def mobility(request):
    similar_insights = Blog.objects.all().order_by('-created_at')[:4] 
    return render(request, 'mobility.html', {
        'similar_insights': similar_insights
    })

def climatechange(request):
    return render(request,'climatechange.html')

def connectedhighway(request):
    return render(request,'connectedhighway.html')

def energy(request):
    return render(request,'energy.html')

def places(request):
    return render(request,'places.html')

def resilience(request):
    return render(request,'resilience.html')

def restoration(request):
    return render(request,'restoration.html')

def urbanism(request):
    return render(request,'urbanism.html')

def asset(request):
    return render(request,'asset.html')

def contract(request):
    return render(request,'contract.html')

def design(request):
    return render(request,'design.html')

def business(request):
    return render(request,'business.html')

def architecture(request):
    return render(request,'architecture.html')

def prog(request):
    return render(request,'prog.html')

def commercials(request):
    return render(request,'commercials.html')

def health(request):
    return render(request,'health.html')

def privacy(request):
    return render(request,'privacypolicy.html')

def aerospace(request):
    return render(request,'aerospace.html')

def automotive(request):
    return render(request,'automotive.html')

def chemical(request):
    return render(request,'chemical.html')

def commercial_dev(request):
    return render(request,'commercial_dev.html')

def contractors(request):
    return render(request,'contractors.html')

def power(request):
    return render(request,'power.html')


def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        feedback=UserFeedback.objects.create(name=name, email=email, message=message)
        feedback.save()

        send_mail(
            subject="🌟 Thank You for Your Feedback!",
            message=(
                f"Dear {name},\n\n"
                f"Thank you so much for your valuable feedback! 📝\n\n"
                f"Our team at InfraBuild truly appreciates you taking the time to reach out. "
                f"We’ll carefully review your message and keep you posted with real-time updates, if needed.\n\n"
                f"You're helping us build a better, more resilient community! ❤️\n\n"
                f"Warm regards,\n"
                f"– The InfraBuild Team 👷‍♂️🏗️"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        

        return render(request, 'governance.html')
    
    return JsonResponse({'success': False}, status=400)

def submit_issue(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        issue_type = request.POST['issue_type']
        location = request.POST.get('location', '')
        description = request.POST['description']
        image = request.FILES.get('image')

        report=UserIssueReport.objects.create(
            name=name,
            email=email,
            issue_type=issue_type,
            location=location,
            description=description,
            image=image
        )
        report.save()

        send_mail(
            subject="🛠️ Thanks for Reporting the Issue!",
            message=(
                f"Hello {name},\n\n"
                f"We've received your report regarding *{issue_type.title()}*. 🧾\n\n"
                f"Our InfraBuild team is now reviewing it, and we'll keep you updated as progress is made. "
                f"Your awareness and support help make our cities safer and stronger! 💪\n\n"
                f"Stay connected with us for real-time updates.\n\n"
                f"Kind regards,\n"
                f"– InfraBuild Support Team 🚧📍"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        

        return render(request, 'governance.html')
    
    return JsonResponse({'success': False}, status=400) 
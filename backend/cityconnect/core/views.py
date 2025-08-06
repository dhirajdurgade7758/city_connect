from django.shortcuts import render, redirect

from cityconnect import settings
from .forms import ReportForm
from .models import News, Report
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from django.core.mail import send_mail

def home(request):
    return render(request, 'core/home.html')


@login_required
def report_issue(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report = form.save(commit=False)
            report.location = request.user.area
            report.save()

            return redirect('my_reports')
    else:
        form = ReportForm()
    return render(request, 'core/report_issue.html', {'form': form})

@login_required
def my_reports(request):
    reports = Report.objects.filter(user=request.user).order_by('-created_at')

    # Filtering
    category = request.GET.get('category')
    status = request.GET.get('status')

    if category and category != "All":
        reports = reports.filter(category=category)
    if status and status != "All":
        reports = reports.filter(status=status)

    # Pagination
    paginator = Paginator(reports, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Unique values for dropdowns
    categories = Report.objects.values_list('category', flat=True).distinct()
    statuses = Report.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'statuses': statuses,
        'selected_category': category,
        'selected_status': status,
    }
    return render(request, 'core/my_reports.html', context)

@login_required
def tasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            user = request.user
            user.eco_coins += 10
            user.save() 
            return redirect('tasks')
    else:
        form = TaskForm()
    
    # Show current + past tasks by this user
    task_list = Task.objects.filter(user=request.user).order_by('-submitted_at')
    paginator = Paginator(task_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    # print(page_obj)  # Debugging line to check tasks
    # print(task_list)  # Debugging line to check tasks
    for task in page_obj:
        print(task)
        print(task.get_task_type_display)  # Debugging line to check task images

    return render(request, 'core/tasks.html', {'form': form, 'page_obj': page_obj})


from .models import Redemption

@login_required
def store(request):
    STORE_ITEMS = [
        {'name': 'Tote Bag', 'coins': 30},
        {'name': 'Coffee Coupon', 'coins': 20},
        {'name': 'Plant Kit', 'coins': 50},
    ]
    
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        coins_required = int(request.POST.get('coins_required'))

        if request.user.eco_coins >= coins_required:
            Redemption.objects.create(
                user=request.user,
                item_name=item_name,
                coins_spent=coins_required,
                status='Pending'
            )
            request.user.eco_coins -= coins_required
            request.user.save()
        return redirect('store')

    redemptions = Redemption.objects.filter(user=request.user).order_by('-requested_at')
    return render(request, 'core/store.html', {
        'items': STORE_ITEMS,
        'redemptions': redemptions
    })


@login_required
def news(request):
    news_items = News.objects.order_by('-created_at')
    return render(request, 'core/news.html', {'news_items': news_items})

from .models import Report, Task, Redemption

@login_required
def profile(request):
    reports = Report.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    redemptions = Redemption.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'eco_coins': request.user.eco_coins,
        'report_count': reports.count(),
        'task_count': tasks.count(),
        'redemption_count': redemptions.count(),
        'recent_reports': reports.order_by('-created_at')[:3],
        'recent_tasks': tasks.order_by('-submitted_at')[:3],
        'recent_redemptions': redemptions.order_by('-requested_at')[:3],
    }
    return render(request, 'core/profile.html', context)


@login_required
def leaderboard(request):
    User = get_user_model()
    top_users = User.objects.filter(role='citizen').order_by('-eco_coins')[:10]
    return render(request, 'core/leaderboard.html', {'top_users': top_users})



from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send welcome email
            subject = 'Welcome to CityConnect!'
            message = f"Hello {user.username},\n\nWelcome to CityConnect! 🎉\n\nYou can now report civic issues, earn EcoCoins, and make your city better!"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            print(f"Welcome email sent to {user.email}")

            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


from .forms import ContactForm
from django.contrib import messages

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)

    if report.status != "Pending":
        return HttpResponseForbidden("You can only edit pending reports.")

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('my_reports')
    else:
        form = ReportForm(instance=report)

    return render(request, 'core/edit_report.html', {'form': form, 'report': report})


@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)

    if report.status != "Pending":
        return HttpResponseForbidden("You can only delete pending reports.")

    if request.method == 'POST':
        report.delete()
        return redirect('my_reports')

    return render(request, 'core/delete_report.html', {'report': report})


from .models import Redemption
from django.core.paginator import Paginator

@login_required
def redeem_history(request):
    redemptions = Redemption.objects.filter(user=request.user).order_by('-requested_at')
    paginator = Paginator(redemptions, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/redeem_history.html', {'page_obj': page_obj})


from .models import Report, Task, Redemption

@login_required
def dashboard(request):
    user = request.user
    profile = user

    # Reports
    reports = Report.objects.filter(user=user)
    total_reports = reports.count()
    recent_reports = reports.order_by('-created_at')[:5]

    # Tasks
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.filter(is_verified=True).count()
    pending_tasks = tasks.filter(is_verified=False).count()
    recent_tasks = tasks.order_by('-submitted_at')[:5]

    # Coins
    total_coins = profile.eco_coins

    # Redemption (optional: only if you have a Redemption model)
    pending_redemptions = Redemption.objects.filter(user=user, status='pending').count() if 'Redemption' in globals() else 0

    context = {
        'total_reports': total_reports,
        'total_tasks': total_tasks,
        'total_coins': total_coins,
        'pending_tasks': pending_tasks,
        'pending_redemptions': pending_redemptions,
        'recent_reports': recent_reports,
        'recent_tasks': recent_tasks,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def area_issues(request):
    user_area = request.user.area
    public_reports = Report.objects.filter(location=user_area).exclude(user=request.user).order_by('-created_at')

    paginator = Paginator(public_reports, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/area_issues.html', {
        'page_obj': page_obj,
        'user_area': user_area
    })


def verify_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_verified = True
    task.award_eco_coins()
    messages.success(request, f"{task.eco_coins_awarded} EcoCoins awarded!")
    return redirect('admin_task_list')

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
from .utils import get_badge_info 

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
    top_users_raw = User.objects.filter(role='citizen').order_by('-eco_coins')[:10]

    # Attach badge info to each user
    top_users = []
    for user in top_users_raw:
        badge_name, badge_color, badge_emoji = get_badge_info(user.eco_coins)
        top_users.append({
            'user': user,
            'badge_name': badge_name,
            'badge_color': badge_color,
            'badge_emoji': badge_emoji,
        })

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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Report, Task, Redemption
from .utils import get_badge_info, get_user_badges  # assuming utils.py contains these functions
from .models import UserBadge
@login_required
def dashboard(request):
    user = request.user

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
    total_coins = user.eco_coins
    badge_name, badge_color, badge_emoji = get_badge_info(total_coins)

    # Redemption (optional)
    pending_redemptions = Redemption.objects.filter(user=user, status='pending').count() if Redemption in globals() else 0

    # Achievement Badges
    achievement_badges = get_user_badges(user)
        # Badge notifications
    new_badges = UserBadge.objects.filter(user=user).order_by('-unlocked_at')[:5]
    if not request.session.get('notified_badges'):
        request.session['notified_badges'] = [b.badge_name for b in new_badges]
        notify_badges = new_badges
    else:
        notify_badges = [
            b for b in new_badges if b.badge_name not in request.session['notified_badges']
        ]
        request.session['notified_badges'] += [b.badge_name for b in notify_badges]

    context = {
        'total_reports': total_reports,
        'total_tasks': total_tasks,
        'total_coins': total_coins,
        'pending_tasks': pending_tasks,
        'pending_redemptions': pending_redemptions,
        'recent_reports': recent_reports,
        'recent_tasks': recent_tasks,

        # Coin-based badge
        'badge_name': badge_name,
        'badge_color': badge_color,
        'badge_emoji': badge_emoji,

        # Achievement badges
        'achievement_badges': achievement_badges,
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


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IssuePostForm
from .models import IssuePost

@login_required
def create_issue_post(request):
    if request.method == 'POST':
        form = IssuePostForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('feed')  # We'll create 'feed' in the next step
    else:
        form = IssuePostForm()

    return render(request, 'core/create_issue_post.html', {'form': form})


# from .models import IssuePost

# @login_required
# def feed(request):
#     area_filter = request.GET.get('area')
    
#     if area_filter:
#         posts = IssuePost.objects.filter(area__iexact=area_filter).select_related('user').prefetch_related('likes', 'comments')
#     else:
#         posts = IssuePost.objects.all().select_related('user').prefetch_related('likes', 'comments')

#     # optional: show unique areas for dropdown filter
#     areas = IssuePost.objects.values_list('area', flat=True).distinct()

#     return render(request, 'core/feed.html', {
#         'posts': posts,
#         'area_filter': area_filter,
#         'areas': areas,
#     })


# from django.shortcuts import get_object_or_404

# from .forms import CommentForm

# @login_required
# def post_detail(request, pk):
#     post = get_object_or_404(IssuePost, id=pk)
#     comments = post.comments.select_related('user').order_by('-timestamp')

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.user = request.user
#             new_comment.post = post
#             new_comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()

#     return render(request, 'core/post_detail.html', {
#         'post': post,
#         'comments': comments,
#         'form': form,
#     })



# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from .models import Like, IssuePost

# @login_required
# def toggle_like(request, pk):
#     post = get_object_or_404(IssuePost, id=pk)
#     like, created = Like.objects.get_or_create(user=request.user, post=post)

#     if not created:
#         # Already liked → unlike
#         like.delete()
#         post.likes_count = post.likes.count()
#     else:
#         # New like
#         post.likes_count = post.likes.count()

#         # Optional: Award coins for 10+ likes
#         if post.likes_count == 10:
#             post.user.eco_coins += 5
#             post.user.save()

#     post.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/feed/'))
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import IssuePost, Like, Comment
from .forms import CommentForm

@login_required
def feed(request):
    area_filter = request.GET.get('area')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')
    
    # Base queryset
    posts = IssuePost.objects.select_related('user')\
                           .prefetch_related('likes', 'comments')
    
    # Apply filters
    if area_filter:
        posts = posts.filter(area__iexact=area_filter)
    
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_details__icontains=search_query)
        )
    
    # Get distinct areas for filter dropdown
    areas = IssuePost.objects.values_list('area', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    saved_posts = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    context = {
        'posts': page_obj,
        'saved_posts': saved_posts,
        'area_filter': area_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'areas': areas,
        'status_choices': IssuePost.STATUS_CHOICES,
    }
    
    return render(request, 'core/feed.html', context)


@login_required
def toggle_like(request, post_id):
    print(f"Like toggle initiated by user {request.user.id} for post {post_id}")
    post = get_object_or_404(IssuePost, id=post_id)
    
    # Debug current like state
    # current_state = post.is_liked_by(request.user)
    # print(f"Current like state before toggle: {current_state}")
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        like.delete()
        print("Like removed")
    else:
        print("Like added")
    
    context = {
        'post': post,
        'request': request
    }
    return render(request, 'core/partials/post_card.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(
        IssuePost.objects.select_related('user')
                        .prefetch_related('likes', 'comments__user'),
        id=post_id
    )
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    comments = post.comments.select_related('user').order_by('-timestamp')
    context = {
        'comments': comments,
        'post': post,
        'form': form,
        'is_liked_by': post.is_liked_by(request.user),
    }
    
    return render(request, 'core/post_detail.html', context)


@login_required
def update_post_status(request, post_id):
    if request.method == 'POST' and request.user.is_staff:
        post = get_object_or_404(IssuePost, id=post_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(IssuePost.STATUS_CHOICES).keys():
            post.status = new_status
            post.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_status': post.get_status_display()
                })
    
    return redirect('post_detail', post_id=post_id)


@login_required
def post_comments(request, post_id):
    """View to handle comment display and creation"""
    post = get_object_or_404(IssuePost, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            if request.headers.get('HX-Request'):
                # Return the updated comments list for HTMX
                comments = post.comments.select_related('user').order_by('-timestamp')
                return render(request, 'core/partials/comments_list.html', {
                    'comments': comments,
                    'post': post
                })
            return redirect('feed')
    
    # GET request - return all comments
    comments = post.comments.select_related('user').order_by('-timestamp')
    return render(request, 'core/partials/comments_list.html', {
        'comments': comments,
        'post': post
    })

@login_required
def comment_form(request, post_id):
    """Return just the comment form for HTMX"""
    post = get_object_or_404(IssuePost, id=post_id)
    comments = post.comments.select_related('user').order_by('-timestamp')
    return render(request, 'core/partials/comment_form.html', {
        'comments': comments,
        'post': post
    })

from django.shortcuts import redirect, get_object_or_404
from .models import IssuePost, SavedPost
from django.contrib.auth.decorators import login_required


@login_required
def toggle_save_post(request, post_id):
    post = get_object_or_404(IssuePost, id=post_id)
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)

    if not created:
        saved.delete()

    # Get updated saved posts list after toggle
    saved_posts = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)


    context = {
        'post': post,
        'saved_posts': saved_posts,
        'csrf_token': request.META.get("CSRF_COOKIE")
    }

    return render(request, 'core/partials/post_card.html', context)


@login_required
def saved_posts_view(request):
    posts = (
        IssuePost.objects
        .filter(savedpost__user=request.user)  # only posts that are saved by this user
        .select_related('user')               # optimize FK to user
        .prefetch_related('likes', 'comments') # optimize related sets
    )
    return render(request, 'core/saved_posts.html', {'saved_posts': posts})

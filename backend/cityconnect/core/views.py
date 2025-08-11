from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.db.models import Q

from cityconnect import settings
from .forms import TaskForm, UserRegisterForm, ContactForm, CommentForm, IssuePostForm
from .models import News, Task, ContactMessage, IssuePost, Like, Comment, SavedPost, UserBadge
from .utils import get_badge_info, get_user_badges # assuming utils.py contains these functions
from store.models import Redemption # Import Redemption from the store app

import logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')


@login_required
def tasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            # Initial EcoCoins are awarded in the Task model's save method
            task.save() 
            messages.success(request, f"Task submitted! You earned {task.initial_eco_coins} EcoCoins. More to come upon admin verification!")
            return redirect('tasks')
        else:
            messages.error(request, "Error submitting task. Please check the form.")
    else:
        form = TaskForm()
    
    # Show current + past tasks by this user
    task_list = Task.objects.filter(user=request.user).order_by('-submitted_at')
    paginator = Paginator(task_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'core/tasks.html', {'form': form, 'page_obj': page_obj})


@login_required
def news_view(request):
    news_items = News.objects.order_by('-created_at')
    return render(request, 'core/news.html', {'news_items': news_items})

def news_detail_modal(request, news_id):
    """Returns the content for a single news item to be loaded into a modal."""
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'core/partials/news_detail_modal.html', {'news_item': news_item})

@login_required
def profile(request):
    user = request.user
    issue_posts = IssuePost.objects.filter(user=user)
    tasks = Task.objects.filter(user=user)
    redemptions = Redemption.objects.filter(user=user) # Fetch from store app

    context = {
        'user': user,
        'eco_coins': user.eco_coins,
        'issue_post_count': issue_posts.count(),
        'task_count': tasks.count(),
        'redemption_count': redemptions.count(),
        'recent_issue_posts': issue_posts.order_by('-created_at')[:3],
        'recent_tasks': tasks.order_by('-submitted_at')[:3],
        'recent_redemptions': redemptions.order_by('-redeemed_at')[:3], # Use redeemed_at
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
            logger.info(f"Welcome email sent to {user.email}")

            login(request, user)
            messages.success(request, "Registration successful! Welcome to CityConnect!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


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
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user

    # Issue Posts
    issue_posts = IssuePost.objects.filter(user=user)
    total_issue_posts = issue_posts.count()
    recent_issue_posts = issue_posts.order_by('-created_at')[:5]

    # Tasks
    tasks = Task.objects.filter(user=user)
    total_tasks = tasks.filter(is_verified=True).count()
    pending_tasks = tasks.filter(is_verified=False).count()
    recent_tasks = tasks.order_by('-submitted_at')[:5]

    # Coins
    total_coins = user.eco_coins
    badge_name, badge_color, badge_emoji = get_badge_info(total_coins)

    # Redemption (from store app)
    pending_redemptions = Redemption.objects.filter(user=user, status='pending').count()

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
        'total_issue_posts': total_issue_posts, # Renamed from total_reports
        'total_tasks': total_tasks,
        'total_coins': total_coins,
        'pending_tasks': pending_tasks,
        'pending_redemptions': pending_redemptions,
        'recent_issue_posts': recent_issue_posts, # Renamed from recent_reports
        'recent_tasks': recent_tasks,

        # Coin-based badge
        'badge_name': badge_name,
        'badge_color': badge_color,
        'badge_emoji': badge_emoji,

        # Achievement badges
        'achievement_badges': achievement_badges,
    }

    return render(request, 'core/dashboard.html', context)


def verify_task(request, task_id):
    # This view is likely for admin panel or internal use, keeping it as is.
    task = get_object_or_404(Task, id=task_id)
    task.is_verified = True
    task.award_eco_coins()
    messages.success(request, f"{task.eco_coins_awarded} EcoCoins awarded!")
    return redirect('admin_task_list') # Assuming an admin URL for tasks


@login_required
def create_issue_post(request):
    if request.method == 'POST':
        form = IssuePostForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            messages.success(request, "Issue post created successfully! You can earn more EcoCoins when others like or comment on your post.")
            return redirect('feed')
        else:
            messages.error(request, "Error creating issue post. Please check your input.")
    else:
        form = IssuePostForm()

    return render(request, 'core/create_issue_post.html', {'form': form})


@login_required
def feed(request):
    area_filter = request.GET.get('area')
    status_filter = request.GET.get('status')
    department_filter = request.GET.get('department') # New filter
    search_query = request.GET.get('q')
    
    posts = IssuePost.objects.select_related('user')\
                           .prefetch_related('likes', 'comments')
    
    if area_filter:
        posts = posts.filter(area__iexact=area_filter)
    
    if status_filter:
        posts = posts.filter(status=status_filter)

    if department_filter: # Apply new department filter
        posts = posts.filter(department=department_filter)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_details__icontains=search_query)
        )
    
    areas = IssuePost.objects.values_list('area', flat=True).distinct()
    departments = IssuePost.DEPARTMENT_CHOICES # Get department choices for filter
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    saved_posts = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    context = {
        'posts': page_obj,
        'saved_posts': saved_posts,
        'area_filter': area_filter,
        'status_filter': status_filter,
        'department_filter': department_filter, # Pass to template
        'search_query': search_query,
        'areas': areas,
        'status_choices': IssuePost.STATUS_CHOICES,
        'department_choices': departments, # Pass to template
    }
    
    return render(request, 'core/feed.html', context)

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(IssuePost, id=post_id)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        like.delete()
        messages.info(request, "Like removed.")
    else:
        messages.success(request, "Post liked!")
    
    # Re-render the post card to update like count/icon
    context = {
        'post': post,
        'request': request,
        'saved_posts': SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True) # Needed for post_card
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
            messages.success(request, "Comment added!")
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, "Error adding comment.")
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
            messages.success(request, f"Post status updated to {post.get_status_display()}.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'new_status': post.get_status_display()
                })
        else:
            messages.error(request, "Invalid status provided.")
    else:
        messages.error(request, "You are not authorized to perform this action.")
    
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
            messages.success(request, "Comment added!")
            if request.headers.get('HX-Request'):
                # Return the updated comments list for HTMX
                comments = post.comments.select_related('user').order_by('-timestamp')
                return render(request, 'core/partials/comments_list.html', {
                    'comments': comments,
                    'post': post
                })
            return redirect('feed')
        else:
            messages.error(request, "Error adding comment.")
    
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


@login_required
def toggle_save_post(request, post_id):
    post = get_object_or_404(IssuePost, id=post_id)
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)

    if not created:
        saved.delete()
        messages.info(request, "Post unsaved.")
    else:
        messages.success(request, "Post saved!")

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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/saved_posts.html', {'saved_posts': page_obj})

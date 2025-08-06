from .models import Task, Redemption

def notification_counts(request):
    if request.user.is_authenticated:
        pending_tasks = Task.objects.filter(user=request.user, is_verified=False).count()
        pending_redemptions = Redemption.objects.filter(user=request.user, status='Pending').count()
    else:
        pending_tasks = 0
        pending_redemptions = 0

    return {
        'pending_tasks': pending_tasks,
        'pending_redemptions': pending_redemptions,
    }

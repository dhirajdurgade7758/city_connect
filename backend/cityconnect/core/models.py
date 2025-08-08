from django.db import models
from django.contrib.auth.models import AbstractUser

# Extended user with roles (Citizen or Admin)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='citizen')
    eco_coins = models.PositiveIntegerField(default=0)
    area = models.CharField(max_length=100, blank=True) 

    def __str__(self):
        return self.username


class Report(models.Model):
    CATEGORY_CHOICES = (
        ('pothole', 'Pothole'),
        ('garbage', 'Garbage'),
        ('lighting', 'Street Lighting'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_feedback = models.TextField(blank=True, null=True)    

    def __str__(self):
        return f"{self.title} - {self.status}"


class Task(models.Model):
    TASK_TYPE = (
        ('cleanup', 'Clean-Up'),
        ('ewaste', 'E-Waste Donation'),
        ('other', 'Other'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE)
    proof_image = models.ImageField(upload_to='tasks/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_feedback = models.TextField(blank=True, null=True) 
    eco_coins_awarded = models.PositiveIntegerField(default=0)

    TASK_TYPE_CHOICES = [
        ('cleanup', 'Public Cleanup'),
        ('awareness', 'Awareness Campaign'),
        ('donation', 'E-waste Donation'),
    ]
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.task_type}"

    def award_eco_coins(self):
        # Rule-based coin awarding
        if self.task_type == 'cleanup':
            self.eco_coins_awarded = 20
        elif self.task_type == 'awareness':
            self.eco_coins_awarded = 15
        elif self.task_type == 'donation':
            self.eco_coins_awarded = 25
        self.save()

        # Update user profile
        profile = self.user.profile
        profile.eco_coins += self.eco_coins_awarded
        profile.save()

    def __str__(self):
        return f"{self.user.username} - {self.task_type}"



class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"


class Redemption(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    coins_spent = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.item_name} - {self.user.username}"


from django.db import models
from django.utils import timezone

class IssuePost(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_posts')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_posts/', blank=True, null=True)
    area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    location_details = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Issue Post'
        verbose_name_plural = 'Issue Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['area']),
        ]

    def is_liked_by(self):
        user = self.user
        return self.likes.filter(user=user).exists()

    def update_counts(self):
        """Update denormalized counts"""
        self.likes_count = self.likes.count()
        self.comments_count = self.comments.count()
        self.save(update_fields=['likes_count', 'comments_count'])


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(IssuePost, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        indexes = [
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_counts()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(IssuePost, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_counts()


# models.py

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=20, choices=[
        ('eco', 'EcoCoin Badge'),
        ('achievement', 'Achievement Badge')
    ])
    badge_name = models.CharField(max_length=100)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge_name')

    def __str__(self):
        return f"{self.user.username} - {self.badge_name}"

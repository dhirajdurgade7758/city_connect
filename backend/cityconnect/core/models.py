from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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



class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('plastic_bottles', 'Donate 100 Plastic Bottles (Recycling)'),
        ('public_awareness', 'Conduct a Public Awareness Campaign'),
        ('tree_planting', 'Participate in a Tree Planting Drive'),
        ('community_cleanup', 'Organize/Join a Community Cleanup Event'),
        ('e_waste_collection', 'Facilitate E-Waste Collection'),
        ('water_conservation', 'Implement Water Conservation Initiative'),
        ('energy_saving', 'Promote Energy Saving Practices'),
        ('composting', 'Start/Maintain a Composting Project'),
        ('other', 'Other Approved Civic Task'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text="A short, descriptive title for your task.")
    description = models.TextField(help_text="Provide details about the task you completed, including location and impact.")
    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    proof_image = models.ImageField(upload_to='tasks/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_feedback = models.TextField(blank=True, null=True) 
    
    # EcoCoin fields
    initial_eco_coins = models.PositiveIntegerField(default=0) # Coins awarded on submission
    verified_eco_coins = models.PositiveIntegerField(default=0) # Additional coins on verification
    total_eco_coins_awarded = models.PositiveIntegerField(default=0) # Sum of initial + verified

    def __str__(self):
        return f"{self.user.username} - {self.get_task_type_display()}"

    def save(self, *args, **kwargs):
        # Set initial coins based on task type if not already set
        if not self.pk: # Only on creation
            initial_rewards = {
                'plastic_bottles': 15,
                'public_awareness': 10,
                'tree_planting': 20,
                'community_cleanup': 25,
                'e_waste_collection': 30,
                'water_conservation': 20,
                'energy_saving': 18,
                'composting': 22,
                'other': 5,
            }
            self.initial_eco_coins = initial_rewards.get(self.task_type, 5)

            self.total_eco_coins_awarded = self.initial_eco_coins
            self.user.eco_coins += self.initial_eco_coins
            self.user.save()

        super().save(*args, **kwargs)

    def award_additional_eco_coins(self):
        # Award additional coins upon admin verification
        if not self.is_verified: # Only if not already verified
            verified_rewards = {
                'plastic_bottles': 35,
                'public_awareness': 40,
                'tree_planting': 30,
                'community_cleanup': 25,
                'e_waste_collection': 20,
                'water_conservation': 30,
                'energy_saving': 32,
                'composting': 28,
                'other': 15,
            }
            self.verified_eco_coins = verified_rewards.get(self.task_type, 15)

            self.total_eco_coins_awarded += self.verified_eco_coins
            self.user.eco_coins += self.verified_eco_coins
            self.user.save()
            self.is_verified = True # Mark as verified after awarding
            self.save(update_fields=['is_verified', 'verified_eco_coins', 'total_eco_coins_awarded'])


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



class IssuePost(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    DEPARTMENT_CHOICES = [
        ('public_works', 'Public Works Department'),
        ('water_supply', 'Water Supply Department'),
        ('waste_management', 'Waste Management Department'),
        ('electricity', 'Electricity Department')
    ]

    id = models.AutoField(primary_key=True, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_posts')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_posts/', blank=True, null=True)
    area = models.CharField(max_length=100)
    location_details = models.CharField(max_length=200, blank=True, null=True, help_text="Specific location details (e.g., 'Near City Park, Sector 10')")
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, help_text="Select the relevant department for this issue.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

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
            models.Index(fields=['department']), # New index for department
        ]

    def is_liked_by(self):
        user = self.user
        """Check if the post is liked by the current user"""
        if not user.is_authenticated:
            return False
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
    
class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(IssuePost, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"

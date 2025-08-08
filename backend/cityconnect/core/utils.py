from .models import UserBadge, IssuePost
from core import models 
from django.db.models import Count


def unlock_badge(user, badge_name, badge_type):
    if not UserBadge.objects.filter(user=user, badge_name=badge_name).exists():
        UserBadge.objects.create(user=user, badge_name=badge_name, badge_type=badge_type)

def get_badge_info(eco_coins, user=None):
    if eco_coins >= 500:
        badge = ("Planet Protector", "warning", "🪐")
    elif eco_coins >= 200:
        badge = ("Eco Champion", "primary", "🌳")
    elif eco_coins >= 100:
        badge = ("Eco Warrior", "success", "🌿")
    elif eco_coins >= 50:
        badge = ("Green Starter", "info", "🌱")
    else:
        badge = ("Newcomer", "secondary", "🐣")

    if user:
        unlock_badge(user, badge[0], 'eco')

    return badge

def get_user_badges(user):
    badges = []

    post_count = IssuePost.objects.filter(user=user).count()
    top_post_likes = IssuePost.objects.filter(user=user).annotate(like_count=Count('likes')).order_by('-like_count').first()
    max_likes = top_post_likes.likes.count() if top_post_likes else 0

    if post_count >= 1:
        unlock_badge(user, "🥇 First Post", 'achievement')
        badges.append("🥇 First Post")
    if post_count >= 10:
        unlock_badge(user, "🏅 10 Posts", 'achievement')
        badges.append("🏅 10 Posts")
    if user.eco_coins >= 100:
        unlock_badge(user, "💯 100 EcoCoins", 'achievement')
        badges.append("💯 100 EcoCoins")
    if max_likes >= 10:
        unlock_badge(user, "🔥 10 Likes on a Post", 'achievement')
        badges.append("🔥 10 Likes on a Post")

    return badges

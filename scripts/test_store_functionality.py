import os
import sys
import django
from datetime import date, timedelta

# Add the project directory to Python path
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityconnect.settings')
django.setup()

from store.models import StoreOffer, Redemption
from core.models import User

def test_store_functionality():
    """Test store functionality"""
    
    print("Testing Store Functionality")
    print("=" * 40)
    
    # Test 1: Check if offers exist
    offers = StoreOffer.objects.filter(is_active=True)
    print(f"Active offers: {offers.count()}")
    
    if offers.exists():
        for offer in offers[:3]:  # Show first 3 offers
            print(f"- {offer.name}: {offer.coins_required} coins, {offer.stock} in stock")
    
    # Test 2: Check if users have coins
    users_with_coins = User.objects.filter(eco_coins__gt=0)
    print(f"\nUsers with coins: {users_with_coins.count()}")
    
    # Test 3: Create test user if needed
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'eco_coins': 500,
            'role': 'citizen'
        }
    )
    
    if created:
        test_user.set_password('test123')
        test_user.save()
        print(f"Created test user with {test_user.eco_coins} coins")
    else:
        print(f"Test user exists with {test_user.eco_coins} coins")
    
    # Test 4: Check redemptions
    redemptions = Redemption.objects.all()
    print(f"\nTotal redemptions: {redemptions.count()}")
    
    if redemptions.exists():
        recent_redemption = redemptions.first()
        print(f"Most recent: {recent_redemption.user.username} redeemed {recent_redemption.offer.name}")
    
    # Test 5: Check offer availability
    available_offers = [offer for offer in offers if offer.is_available()]
    print(f"\nAvailable offers: {len(available_offers)}")
    
    # Test 6: Simulate redemption (dry run)
    if available_offers and test_user.eco_coins >= available_offers[0].coins_required:
        offer = available_offers[0]
        print(f"\nSimulation: {test_user.username} can redeem '{offer.name}'")
        print(f"Cost: {offer.coins_required} coins")
        print(f"User has: {test_user.eco_coins} coins")
        print(f"After redemption: {test_user.eco_coins - offer.coins_required} coins")
    else:
        print(f"\nSimulation: Cannot redeem - insufficient coins or no available offers")
    
    print("\nStore functionality test completed!")

if __name__ == '__main__':
    test_store_functionality()

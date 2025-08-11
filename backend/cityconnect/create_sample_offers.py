import os
import django
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityconnect.settings')
django.setup()

from django.contrib.auth import get_user_model
from store.models import StoreOffer

User = get_user_model()

def create_sample_offers():
    print("Creating sample store offers...")

    # Get or create a user to be the 'added_by' for offers
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpassword', role='admin')
        print("Created a new admin user: admin")

    today = date.today()

    offers_to_create = [
        {
            'name': 'Local Cafe Discount',
            'description': 'Get 20% off your next coffee at City Brew Cafe!',
            'coins_required': 50,
            'offer_type': 'shop_offer',
            'location_name': '123 Main St, Cityville',
            'location_map_url': 'https://maps.google.com/?q=City+Brew+Cafe',
            'stock': 100,
            'start_date': today - timedelta(days=7),
            'end_date': today + timedelta(days=30),
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Community Garden Seed Pack',
            'description': 'Redeem for a free pack of organic vegetable seeds for your garden.',
            'coins_required': 30,
            'offer_type': 'eco_reward',
            'location_name': 'City Community Garden',
            'location_map_url': 'https://maps.google.com/?q=Community+Garden',
            'stock': 50,
            'start_date': today - timedelta(days=10),
            'end_date': today + timedelta(days=60),
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Charity Donation Match',
            'description': 'We will match your EcoCoin donation to the local animal shelter.',
            'coins_required': 100,
            'offer_type': 'donor_gift',
            'location_name': 'Online / City Animal Shelter',
            'location_map_url': '',
            'stock': 20,
            'start_date': today - timedelta(days=5),
            'end_date': today + timedelta(days=45),
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Local Music Festival Ticket',
            'description': 'One free ticket to the annual City Sounds Music Festival!',
            'coins_required': 200,
            'offer_type': 'event_ticket',
            'location_name': 'City Park Amphitheater',
            'location_map_url': 'https://maps.google.com/?q=City+Park+Amphitheater',
            'stock': 10,
            'start_date': today + timedelta(days=15),
            'end_date': today + timedelta(days=20),
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Expired Offer Example',
            'description': 'This offer is no longer valid.',
            'coins_required': 10,
            'offer_type': 'shop_offer',
            'location_name': 'Old Shop',
            'location_map_url': '',
            'stock': 5,
            'start_date': today - timedelta(days=30),
            'end_date': today - timedelta(days=1), # Expired yesterday
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Out of Stock Item',
            'description': 'A popular item that ran out.',
            'coins_required': 75,
            'offer_type': 'eco_reward',
            'location_name': 'Eco Center',
            'location_map_url': '',
            'stock': 0, # Out of stock
            'start_date': today - timedelta(days=10),
            'end_date': today + timedelta(days=30),
            'is_active': True,
            'added_by': admin_user,
        },
        {
            'name': 'Future Event Ticket',
            'description': 'Ticket for an event next month.',
            'coins_required': 150,
            'offer_type': 'event_ticket',
            'location_name': 'Community Hall',
            'location_map_url': '',
            'stock': 20,
            'start_date': today + timedelta(days=30), # Starts in the future
            'end_date': today + timedelta(days=35),
            'is_active': True,
            'added_by': admin_user,
        },
    ]

    for offer_data in offers_to_create:
        # Remove 'added_by' from data for create, then assign
        added_by_user = offer_data.pop('added_by')
        offer, created = StoreOffer.objects.get_or_create(
            name=offer_data['name'],
            defaults={**offer_data, 'added_by': added_by_user}
        )
        if created:
            print(f"Created offer: {offer.name}")
        else:
            print(f"Offer already exists: {offer.name}")
            # Update existing offer if needed
            for key, value in offer_data.items():
                setattr(offer, key, value)
            offer.added_by = added_by_user # Ensure added_by is set
            offer.save()

    print("Sample offers creation complete.")

if __name__ == '__main__':
    create_sample_offers()

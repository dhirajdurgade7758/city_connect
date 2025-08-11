import os
import django

# 1. Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityconnect.settings')  # replace with your project name
django.setup()

from core.models import IssuePost

# Map of title -> new description (3+ lines each)
updated_descriptions = {
    "Potholes on Main Street": """Large potholes have appeared after heavy rains. 
They are causing traffic jams and damaging vehicles. 
If left unattended, these potholes may expand further and pose a risk to pedestrians as well.""",

    "Low Water Pressure in Sector 4": """Residents are experiencing very low water pressure since last week. 
Daily chores such as cooking and cleaning have become difficult. 
The issue seems to be worsening, affecting even early morning supply hours.""",

    "Garbage Collection Delays": """Garbage has not been collected for over a week. 
The smell is unbearable and is attracting stray dogs and rodents. 
Nearby shop owners have also complained about reduced footfall due to the foul environment.""",

    "Street Light Not Working": """Street light on main road has been out for 10 days. 
The area is dark and unsafe for pedestrians, especially late at night. 
Local businesses say customers are avoiding the area after sunset.""",

    "Broken Footpath Tiles": """Several tiles on the footpath are broken or missing. 
Elderly citizens and children are finding it hard to walk safely. 
A few minor accidents have already been reported by residents.""",

    "Water Leakage on Main Road": """A major pipeline burst has caused water to flood the road. 
Traffic is being diverted, leading to long delays during peak hours. 
The constant water flow is also damaging the road surface and nearby shop entrances.""",

    "Overflowing Dustbin": """Public dustbin is overflowing with trash and has not been emptied in days. 
Passersby are forced to throw waste on the street, creating a mess. 
The area now attracts flies and has a strong foul odor throughout the day.""",

    "Power Fluctuations at Night": """Frequent voltage fluctuations occur every evening. 
Electronics are at risk of damage and several households have reported appliance failures. 
The fluctuations also cause frequent tripping of power supply in some houses.""",

    "Cracked Road Divider": """Road divider has cracks and loose stones that can come loose. 
This poses a danger to two-wheeler riders and cars alike. 
Heavy vehicles hitting the divider could worsen the damage quickly.""",

    "Contaminated Water Supply": """Tap water smells bad and looks muddy. 
Many residents are reporting stomach issues and fear a waterborne disease outbreak. 
The contamination appears to be constant and affects multiple blocks in the area."""
}

# Update descriptions
for title, new_desc in updated_descriptions.items():
    try:
        issue = IssuePost.objects.get(title=title)
        issue.description = new_desc
        issue.save(update_fields=['description'])
        print(f"✅ Updated: {title}")
    except IssuePost.DoesNotExist:
        print(f"⚠️ Not found: {title}")

print("🎯 All descriptions updated successfully.")

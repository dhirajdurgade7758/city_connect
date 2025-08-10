from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from .models import StoreOffer, Redemption
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import json

@login_required
def store_view(request):
    """Enhanced store view with filtering and search capabilities"""
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')
    sort_by = request.GET.get('sort', 'name')
    # category_filter = request.GET.get('category', 'all')
    # sort_by = request.GET.get('sort', 'name')
    
    # Base queryset
    offers = StoreOffer.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )
    
    # Apply search filter
    if search_query:
        offers = offers.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter != 'all':
        offers = offers.filter(offer_type=category_filter)
    
    # Apply sorting
    if sort_by == 'coins_asc':
        offers = offers.order_by('coins_required')
    elif sort_by == 'coins_desc':
        offers = offers.order_by('-coins_required')
    elif sort_by == 'stock':
        offers = offers.order_by('-stock')
    else:  # default to name
        offers = offers.order_by('name')
    
    # Group by type for template
    shop_offers = offers.filter(offer_type='shop_offer')
    donor_gifts = offers.filter(offer_type='donor_gift')
    event_tickets = offers.filter(offer_type='event_ticket')
    eco_rewards = offers.filter(offer_type='eco_reward')
    
    context = {
        'shop_offers': shop_offers,
        'donor_gifts': donor_gifts,
        'event_tickets': event_tickets,
        'eco_rewards': eco_rewards,
        'search_query': search_query,
        'category_filter': category_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'store/store.html', context)

@login_required
def redeem_offer(request, offer_id):
    """Enhanced redeem offer with better error handling"""
    offer = get_object_or_404(StoreOffer, id=offer_id)
    
    # Validation checks
    if request.user.eco_coins < offer.coins_required:
        messages.error(request, f"You need {offer.coins_required - request.user.eco_coins} more EcoCoins to redeem this offer.")
        return redirect('store_view')
    
    if not offer.is_available():
        messages.error(request, "This offer is no longer available.")
        return redirect('store_view')
    
    try:
        # Deduct coins and reduce stock in a transaction
        from django.db import transaction
        
        with transaction.atomic():
            # Refresh user data to prevent race conditions
            request.user.refresh_from_db()
            
            # Double-check coins after refresh
            if request.user.eco_coins < offer.coins_required:
                messages.error(request, "Insufficient EcoCoins.")
                return redirect('store_view')
            
            # Deduct coins
            request.user.eco_coins -= offer.coins_required
            request.user.save()
            
            # Reduce stock
            offer.stock -= 1
            offer.save()
            
            # Create redemption entry
            redemption = Redemption.objects.create(
                user=request.user,
                offer=offer,
                coins_spent=offer.coins_required
            )
            
        messages.success(request, f"Successfully redeemed {offer.name}! Check your voucher below.")
        return redirect('redemption_voucher', redemption.id)
        
    except Exception as e:
        messages.error(request, "An error occurred during redemption. Please try again.")
        return redirect('store_view')

@login_required
def redemption_voucher(request, redemption_id):
    """Display redemption voucher"""
    redemption = get_object_or_404(Redemption, id=redemption_id, user=request.user)
    return render(request, 'store/voucher.html', {'redemption': redemption})

@login_required
def download_voucher_pdf(request, redemption_id):
    """Generate and download PDF voucher"""
    redemption = get_object_or_404(Redemption, id=redemption_id, user=request.user)
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    filename = f"voucher_{redemption.offer.name.replace(' ', '_')}_{redemption.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Colors
    primary_color = HexColor('#28a745')
    secondary_color = HexColor('#6c757d')
    
    # Header
    p.setFillColor(primary_color)
    p.rect(0, height - 100, width, 100, fill=1)
    
    p.setFillColor('white')
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredText(width/2, height - 40, "EcoCoin Store")
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredText(width/2, height - 65, "Redemption Voucher")
    
    # Voucher details
    y_position = height - 150
    p.setFillColor('black')
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y_position, f"Offer: {redemption.offer.name}")
    
    y_position -= 30
    p.setFont("Helvetica", 12)
    p.drawString(50, y_position, f"Description: {redemption.offer.description}")
    
    y_position -= 25
    p.drawString(50, y_position, f"Location: {redemption.offer.location_name}")
    
    y_position -= 25
    p.drawString(50, y_position, f"Coins Spent: {redemption.coins_spent}")
    
    y_position -= 25
    p.drawString(50, y_position, f"Voucher Code: {redemption.voucher_code}")
    
    y_position -= 25
    p.drawString(50, y_position, f"Redeemed On: {redemption.redeemed_at.strftime('%B %d, %Y at %H:%M')}")
    
    y_position -= 25
    p.drawString(50, y_position, f"Valid Until: {redemption.offer.end_date.strftime('%B %d, %Y')}")
    
    # Terms and conditions
    y_position -= 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Terms & Conditions:")
    
    terms = [
        "• This voucher is valid for one-time use only",
        "• Present this voucher at the specified location",
        "• Cannot be exchanged for cash or other offers",
        "• Valid only until the expiration date mentioned above"
    ]
    
    p.setFont("Helvetica", 10)
    for term in terms:
        y_position -= 20
        p.drawString(70, y_position, term)
    
    # Footer
    p.setFillColor(secondary_color)
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredText(width/2, 50, "Thank you for using EcoCoin Store!")
    p.drawCentredText(width/2, 35, "For support, contact us at support@ecocoin.com")
    
    p.showPage()
    p.save()
    
    return response

@login_required
@require_http_methods(["POST"])
def toggle_wishlist(request, offer_id):
    """Toggle offer in user's wishlist (placeholder for future implementation)"""
    offer = get_object_or_404(StoreOffer, id=offer_id)
    
    # This would typically interact with a Wishlist model
    # For now, we'll just return a success response
    
    return JsonResponse({
        'success': True,
        'message': 'Wishlist updated',
        'in_wishlist': True  # This would be the actual status
    })

@login_required
def quick_view_offer(request, offer_id):
    """Get offer details for quick view modal"""
    offer = get_object_or_404(StoreOffer, id=offer_id)
    
    data = {
        'id': offer.id,
        'name': offer.name,
        'description': offer.description,
        'coins_required': offer.coins_required,
        'location_name': offer.location_name,
        'location_map_url': offer.location_map_url,
        'stock': offer.stock,
        'end_date': offer.end_date.strftime('%B %d, %Y'),
        'image_url': offer.image.url if offer.image else None,
        'is_available': offer.is_available(),
        'can_afford': request.user.eco_coins >= offer.coins_required
    }
    
    return JsonResponse(data)

@login_required
def user_redemptions(request):
    """View user's redemption history"""
    redemptions = Redemption.objects.filter(user=request.user).order_by('-redeemed_at')
    
    # Pagination
    paginator = Paginator(redemptions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'store/redemption_history.html', {
        'redemptions': page_obj,
        'total_spent': sum(r.coins_spent for r in redemptions)
    })

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from time import localtime, strftime
# from django.core.mail import send_mail
# from django.conf import settings
from .models import Order

# Create your views here.
def index(request):
    return render(request, 'orders/index.html')

def select_movie(request):
    request.session['movie_selection_title'] = request.POST["movie_selection_title"]
    request.session['movie_selection_time'] = request.POST["movie_selection_time"]
    request.session['movie_selection_tix'] = request.POST["movie_selection_tix"]
    return redirect('/checkout')

def show_checkout(request):
    orders_made = Order.objects.filter(movie_title=request.session['movie_selection_title'], movie_time=request.session['movie_selection_time'])
    tickets_sold = 0
    for order in orders_made:
        tickets_sold += order.num_tix

    print('tickets sold:', tickets_sold)
    
    if tickets_sold >= 30:
        print('movie is soldout')
        messages.info(request, 'Sorry there are no more tickets available for this showtime!')
        return HttpResponseRedirect('/')
    else:
        total_sales = int(request.session['movie_selection_tix']) * 9
        context = {
            'movie_selection_title': request.session['movie_selection_title'],
            'movie_selection_time': request.session['movie_selection_time'],
            'movie_selection_tix': request.session['movie_selection_tix'],
            'date': strftime('%m/%d/%Y', localtime()),
            'total_sales': total_sales
        }
        return render(request, 'orders/checkout.html', context)

def show_dashboard(request):
    orders_for_ad_astra = Order.objects.filter(movie_title="Ad Astra")
    total_sales_ad_astra = 0
    total_tix_ad_astra = 0
    for order in orders_for_ad_astra:
        total_sales_ad_astra += order.order_total
        total_tix_ad_astra += order.num_tix
    print(total_tix_ad_astra)

    all_orders = Order.objects.all()
    total_revenue = 0
    total_tickets = 0
    for order in all_orders:
        total_revenue += order.order_total
        total_tickets += order.num_tix

    context = {
        'all_orders': Order.objects.all(),
        'total_sales_ad_astra': total_sales_ad_astra,
        'total_tix_ad_astra': total_tix_ad_astra,
        'total_revenue': total_revenue,
        'total_tickets': total_tickets,
    }
    return render(request, 'orders/dashboard.html', context)

def checkout(request):
    errors = Order.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/checkout')
    else:
        print('*'*50, 'processing order')
        Order.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email_address=request.POST["email"], credit_card_num=request.POST["cc"], expiry_month=request.POST["exp_month"], expiry_year=request.POST["exp_year"], sec_code=request.POST["sec_code"], movie_title=request.POST["movie"], movie_date=request.POST["date"], movie_time=request.POST["time"], num_tix=request.POST["num_tix"], order_total=request.POST["total"])

        # send_mail(
        # 'Order Confirmation',
        # request.session['movie_selection_tix'] ' ticket for ' request.session['movie_selection_title'] 'Total ' request.POST["total"],
        # 'sales@movieapp.com',
        # [request.POST["email"]],
        # fail_silently=False,
        # )
        request.session.clear()
        return redirect('/')
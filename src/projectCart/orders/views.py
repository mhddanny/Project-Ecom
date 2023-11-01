from carts.models import Cart, CartItem
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from store.models import Product

from . forms import OrderForm
from . models import Order, OrderProduct, Payment 

import datetime
import json
import uuid
import midtransclient
import hashlib


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()
        
        # reduce the quantiry of the sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clarn cart
    CartItem.objects.filter(user=request.user).delete()

    # send ordered receiverd email to customer
    mail_subject = 'Thanks you for your order !'
    message = render_to_string('orders/order_vertification_email.html', {
        'user' : request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    #send order number and transaction id back to send data method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id
    }
    return JsonResponse(data)

    return render(request, 'orders/payments.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity +=cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.postcode = form.cleaned_data['postcode']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #2023020401
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            print('order', order)

            # Create Snap API instance
            snap = midtransclient.Snap(
                is_production=False,
                # server_key='SB-Mid-server-LY4us9KJJfHQywCryUtfDlCf',
                server_key=settings.MIDTRANS['SERVER_KEY'],
            )
            client_key= settings.MIDTRANS['CLIENT_KEY']
            # Build API parameter
            param = {
                "transaction_details": {
                    "order_id": order.id,
                    "gross_amount": total,
                },
                "item_details": [{
                    "id": cart_item.id,
                    "price": cart_item.product.price,
                    "quantity": cart_item.quantity,
                    "name": cart_item.product.product_name,
                }],
                "customer_details":{
                    "first_name": order.first_name,
                    "last_name": order.last_name,
                    "email": order.email,
                    "phone": order.phone
                },
                "enabled_payments": ["credit_card", "mandiri_clickpay", "cimb_clicks","bca_klikbca", "bca_klikpay", "bri_epay", "echannel", "indosat_dompetku","mandiri_ecash", "permata_va", "bca_va", "bni_va", "other_va", "gopay","kioson", "indomaret", "gci", "danamon_online"],
                "credit_card": {
                    "secure": True,
                    "bank": "bca",
                    "installment": {
                        "required": False,
                        "terms": {
                            "bni": [3, 6, 12],
                            "mandiri": [3, 6, 12],
                            "cimb": [3],
                            "bca": [3, 6, 12],
                            "offline": [6, 12]
                        }
                    },
                    "whitelist_bins": [
                        "48111111",
                        "41111111"
                    ]
                },
                "bca_va": {
                    "va_number": "12345678911",
                    "free_text": {
                        "inquiry": [
                            {
                                "en": "text in English",
                                "id": "text in Bahasa Indonesia"
                            }
                        ],
                        "payment": [
                            {
                                "en": "text in English",
                                "id": "text in Bahasa Indonesia"
                            }
                        ]
                    }
                },
                "bni_va": {
                    "va_number": "12345678"
                },
                "permata_va": {
                    "va_number": "1234567890",
                    "recipient_name": "SUDARSONO"
                },
                "callbacks": {
                    "finish": "dashboard/"
                },
                "expiry": {
                    "start_time": "2025-12-20 18:11:08 +0700",
                    "unit": "minute",
                    "duration": 9000
                },
                "custom_field1": "custom field 1 content",
                "custom_field2": "custom field 2 content",
                "custom_field3": "custom field 3 content"
            }

            print('param', param)

            transaction = snap.create_transaction(param)

            transaction_token = transaction['token']
            print('token', transaction_token)
            print('client', client_key)
            context = {
                'order': order,
                'cart_items': cart_items,
                'tax': tax,
                'total': total,
                'grand_total': grand_total,
                'token': transaction_token,
                'client': client_key,
            }

            return render(request, 'orders/payments.html', context)

        else:
            return HttpResponse('errors')
    else:
        return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_product:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_product': ordered_product,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

# @csrf_exempt  
# def callback(request):
#     serverKey = settings.MIDTRANS['SERVER_KEY']
#     has = hashlib.sha512(order_id+status_code+gross_amount+serverKey)
#     if has == request.signature_key:
#         if request.transaction_status == 'capture':
#             order = Order.objects.get(id=order_id)
#             order.is_ordered = True
#             order.save()

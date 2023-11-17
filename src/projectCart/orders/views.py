from carts.models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from store.models import Product


from . forms import OrderForm
from . models import Order, OrderProduct, Payment, OrderDelivery

import datetime
import json
import uuid
import midtransclient
import hashlib
import base64

MIDTRANS_CORE = midtransclient.CoreApi(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY'],
)

MIDTRANS_SNAP = midtransclient.Snap(
    is_production=not settings.DEBUG,
    server_key=settings.MIDTRANS['SERVER_KEY'],
    client_key=settings.MIDTRANS['CLIENT_KEY'],
)



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

def payment_proses(request):
    body = json.loads(request.body) 
    order_id = body['order_id']
    print('order_id', order_id)

    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_id)
    
    transaction_status = MIDTRANS_CORE.transactions.status(str(order_id))
    print('payment_type', transaction_status['payment_type'])
    # [5.A] Handle transaction status on your backend
    # Sample transaction_status handling logic
    if transaction_status['payment_type'] == 'credit_card':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = transaction_status['bank'],
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()
    elif transaction_status['payment_type'] == 'echannel':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = 'Mandiri Bill',
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()
    elif transaction_status['payment_type'] == 'bank_transfer':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = transaction_status['va_numbers'][0]['bank']+"_VA",
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()
    elif transaction_status['payment_type'] == 'gopay':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = 'Gopay',
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()
    elif transaction_status['payment_type'] == 'qris':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = 'Shopeepay',
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()
    elif transaction_status['payment_type'] == 'cstore':
        payment = Payment(
            user = request.user,
            payment_id = transaction_status['transaction_id'],
            payment_method = 'C-Store',
            amount_paid = transaction_status['gross_amount'],
            payment_type = transaction_status['payment_type'],
            status = transaction_status['transaction_status'],
        )
        payment.save()

    # if transaction_status['transaction_status'] == 'capture':
    #     if fraud_status == 'challenge':
    #         # TODO set transaction status on your databaase to 'challenge'
    #         None
    #     elif fraud_status == 'accept':
    #         # TODO set transaction status on your databaase to 'success'
    #         None
    # elif transaction_status['transaction_status'] == 'settlement':
    #     payment = Payment(
    #         user = request.user,
    #         payment_id = transaction_status['transaction_id'],
    #         payment_method = transaction_status['va_numbers'][0]['bank']+"_VA",
    #         amount_paid = transaction_status['gross_amount'],
    #         payment_type = transaction_status['payment_type'],
    #         status = transaction_status['transaction_status'],
    #     )
    #     payment.save()

    #     order.payment = payment
    #     order.is_ordered = True
    #     order.save()

    #     cart_items = CartItem.objects.filter(user=request.user)

    #     for item in cart_items:
    #         orderproduct = OrderProduct()
    #         orderproduct.order_id = order.id
    #         orderproduct.payment = payment
    #         orderproduct.user_id = request.user.id
    #         orderproduct.product_id = item.product_id
    #         orderproduct.quantity = item.quantity
    #         orderproduct.product_price = item.product.price
    #         orderproduct.ordered = True
    #         orderproduct.save()

    #         cart_item = CartItem.objects.get(id=item.id)
    #         product_variation = cart_item.variation.all()
    #         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    #         orderproduct.variation.set(product_variation)
    #         orderproduct.save()
            
    #         # reduce the quantiry of the sold product
    #         product = Product.objects.get(id=item.product_id)
    #         product.stock -= item.quantity
    #         product.save()

    #         # clarn cart
    #     CartItem.objects.filter(user=request.user).delete()

    #         # send ordered receiverd email to customer
    #     mail_subject = 'Thanks you for your order !'
    #     message = render_to_string('orders/order_vertification_email.html', {
    #         'user' : request.user,
    #         'order': order,
    #     })
    #     to_email = request.user.email
    #     send_email = EmailMessage(mail_subject, message, to=[to_email])
    #     send_email.send() 

    #     data = {
    #         'order_number': order.order_number,
    #         'transID': payment.payment_id
    #     }
        
    #     return JsonResponse(data)
    # elif transaction_status['transaction_status'] == 'pending':
    #     payment = Payment(
    #         user = request.user,
    #         payment_id = transaction_status['transaction_id'],
    #         payment_method = transaction_status['va_numbers'][0]['bank']+"_VA",
    #         amount_paid = transaction_status['gross_amount'],
    #         payment_type = transaction_status['payment_type'],
    #         status = transaction_status['transaction_status'],
    #     )
    #     payment.save()

    #     order.payment = payment
    #     order.is_ordered = True
    #     order.save()

    #     cart_items = CartItem.objects.filter(user=request.user)

    #     for item in cart_items:
    #         orderproduct = OrderProduct()
    #         orderproduct.order_id = order.id
    #         orderproduct.payment = payment
    #         orderproduct.user_id = request.user.id
    #         orderproduct.product_id = item.product_id
    #         orderproduct.quantity = item.quantity
    #         orderproduct.product_price = item.product.price
    #         orderproduct.ordered = True
    #         orderproduct.save()

    #         cart_item = CartItem.objects.get(id=item.id)
    #         product_variation = cart_item.variation.all()
    #         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    #         orderproduct.variation.set(product_variation)
    #         orderproduct.save()
            
    #         # reduce the quantiry of the sold product
    #         product = Product.objects.get(id=item.product_id)
    #         product.stock -= item.quantity
    #         product.save()

    #         # clarn cart
    #     CartItem.objects.filter(user=request.user).delete()

    #         # send ordered receiverd email to customer
    #     mail_subject = 'Thanks you for your order !'
    #     message = render_to_string('orders/order_vertification_email.html', {
    #         'user' : request.user,
    #         'order': order,
    #     })
    #     to_email = request.user.email
    #     send_email = EmailMessage(mail_subject, message, to=[to_email])
    #     send_email.send() 

    #     data = {
    #         'order_number': order.order_number,
    #         'transID': payment.payment_id
    #     }
        
    #     return JsonResponse(data)
    
    
    order.payment = payment
    order.is_ordered = True
    order.save()

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

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id
    }
        
    return JsonResponse(data)

def payment_midtrants(request):
    product_price = 0
    total_cost = 0
    sub_total = 0
    total =  0
    body = json.loads(request.body)
    amount = body['amount']
    
    # Generate order number
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr,mt,dt)
    current_date = d.strftime("%Y%m%d") #2023020401
        
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    cards = CartItem.objects.filter(user=request.user).all()
    for card in cards:
        product_price = (card.product.price * card.quantity)#harga price
        product = card.product.product_name
        cart_id = card.id
        quantity = card.quantity 

        # print('sub_total', sub_total)
        sub_total = sum([product_price])
        print('sub', sub_total)
    total_cost += (order.orderdelivery.cost)#total ongkos
    total += (total_cost + product_price)
    print('grand_total', total)

    # Build API parameter
    param = {
        "transaction_details": {
            "order_id": current_date + str(order.id),
            "gross_amount": amount,
        },
        # "item_details": [
        #     {
        #         "id": cart_id,
        #         "price": product_price,
        #         "quantity": quantity,
        #         "name": product,
        #         "merchant_name": "Ar-Rasyiid Store"
        #     }
        # ],
        "customer_details":{
            "first_name": order.first_name,
            "last_name": order.last_name,
            "email": order.email,
            "phone": order.phone,
            "notes": "Thank you for your purchase. Please follow the instructions to pay.",
    
        },
        "enabled_payments": [
                "credit_card", 
                "mandiri_clickpay", 
                "cimb_clicks",
                "bca_klikbca", 
                "bca_klikpay", 
                "bri_epay", 
                "echannel", 
                "indosat_dompetku",
                "mandiri_ecash", 
                "permata_va", 
                "bca_va", 
                "bni_va", 
                "other_va", 
                "gopay",
                "kioson", 
                "indomaret", 
                "gci", 
                "danamon_online",
                "Indomaret",
                "alfamart",
                "akulaku"
            ],
        "credit_card": {
            "secure": True,
            "installment": {
                "required": True,
                "terms": {
                    "bca": [3,6,12],
                    "bni": [3,6,12],
                    "mandiri": [3,6,12],
                    "cimb": [3,6,12],
                    "bri": [3,6,12],
                    "maybank": [3,6,12],
                    "mega": [3,6,12],
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
            "recipient_name": "MHD DANNY"
        },
        "echannel" : {
            "bill_info1" : "Payment For:",
            "bill_info2" : "debt",
            "bill_key" : "085272330324"
        },
        "callbacks": {
            "finish": "http://127.0.0.1:8000/orders/my_orders//"
        },
        "expiry": {
            "unit": "minute",
            "duration": 1440
        },
        "custom_field1": "Selamat Data di Toko Ar-Rasiid",
        "custom_field2": "Silahkan Melakukan Pembayaran pada waktu yang telah di tentutkan",
        "custom_field3": "Terimakasih"
        }
    err = None
    try:
        transaction = MIDTRANS_SNAP.create_transaction(param)
        transaction_token = transaction['token']
        transaction = transaction_token   
        data = {
            'data': transaction
        }
        return JsonResponse(data)
    except Exception as e:
        err = e

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    all_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity +=cart_item.quantity  
        cardID = cart_item.id

    # tax = (2 * total)/100
    grand_total = total # + tax

    client_key = settings.MIDTRANS['CLIENT_KEY']
    server_key = settings.MIDTRANS['SERVER_KEY'] 
    server_key = "Basic "+server_key+":"
    server_key_byte = server_key.encode("ascii")
    base64_string = base64.b64encode(server_key_byte)
    server= base64_string.decode("ascii")

    print('server', server)

    if request.method == 'POST':
        district = request.POST['district_id']
        total_weight = request.POST['total_weight']
        courier = request.POST['courier']
        cost = request.POST['cost']
        
        all_total = grand_total + int(cost)
        # print('dis', total_weight)
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
            data.order_note = form.cleaned_data['order_note']
            data.district_id = district
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
            delivery = OrderDelivery()
            delivery.order_id = order.id
            delivery.courier = courier
            delivery.cost = cost
            delivery.total_weight = total_weight
            delivery.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'tax': tax,
                'cost': cost,
                'total': total,
                'all_total': all_total,
                'client': client_key,
                'server': server,
                'cardID': cardID,
            }
            
            return render(request, 'orders/payments.html', context)

        else:
            messages.error(request, 'Data dont valid')
            return redirect('checkout')     
            # return HttpResponse('errors')
    else:
        return redirect('checkout')

    # return render(request, 'orders/payments.html', {'client': client_key, 'server': server})

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

        status_response = MIDTRANS_CORE.transactions.status(str(order_number)) 
        status = status_response['transaction_status']
        print('status', status)
        
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'status': status,
            'status_response': status_response,
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

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user.id, is_ordered=True).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'orders/my_order/index.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(user=request.user, order_number=order_id)
    print('order', order)
    subtotal = 0 
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    status = MIDTRANS_CORE.transactions.status(str(order.order_number))
    print('status', status)
    transaction_status = status['transaction_status']    
    print('payment_id', transaction_status)
    # payment_id = Payment.objects.get(payment_id=status['transaction_id'])
    # if transaction_status == 'settlement':
    #     payment = payment_id
    #     payment.status = status['transaction_status'],
    #     payment.save()

    # elif transaction_status == 'pending':
    #     payment = payment_id
    #     payment.status = status['transaction_status'],
    #     payment.save()

    # elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
    #     payment = payment_id
    #     payment.status = status['transaction_status'],
    #     payment.save()

    #     order.payment = payment
    #     order.is_ordered = False
    #     order.save()

    #     orderProduct = OrderProduct.objects.get(order=order.id)

    #     product = Product.objects.get(id=orderProduct.product_id)
    #     product.stock += orderProduct.quantity
    #     product.save()

    #     orderProduct.delete()

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'status': transaction_status,
        'status_response':status,
    }

    return render(request, 'orders/my_order/order_detail.html', context)
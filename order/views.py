from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import orderForm
from .models import Orders,Payment,OrderPet
from cart.models import Cart
from datetime import datetime
import uuid
import json
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Spacer
from reportlab.lib import colors
from django.conf import settings
from django.core.mail import EmailMessage


# Create your views here.
def place_order(request):
    form = orderForm()
    currrent_user = request.user
    cart_items = Cart.objects.filter(user = currrent_user)
    cart_items_count = cart_items.count()
    total_amount = request.GET.get('totalamount',0.0) # get the total Mount

    if cart_items_count <= 0:
        return redirect('pets_list')
    if request.method == "POST":
        form = orderForm(request.POST)
        data = Orders()
        if form.is_valid():
            data.user = request.user
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.phone = form.cleaned_data.get('phone')
            data.email = form.cleaned_data.get('email')
            data.address = form.cleaned_data.get('address')
            data.country = form.cleaned_data.get('country')
            data.state = form.cleaned_data.get('state')
            data.city = form.cleaned_data.get('city')
            data.total = total_amount
            data.ip = request.META.get('REMOTE_ADDR')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().fields[-1])[:5]
            orderNumber = f'ORD-{timestamp}.{unique_id}'
            data.order_bumber = orderNumber
            data.save()
            order_object = Orders.objects.get(user= request.user,order_bumber = orderNumber)
            context = {
                'orders':order_object.pk,
                'cart_item':[item.pk for item in cart_items],
                'total_amount':total_amount,
            }
            serialized_data  = json.dumps(context)
            redirect_url = reverse('order:payments') + f'?data={serialized_data}'
            return redirect(redirect_url)
            # return render(request,'order/payment_page.html',context)
           
    return render(request,"order/billing_page.html",{'form':form,'total':total_amount})


@csrf_exempt
def payments(request):
    context={}
    if request.method == "POST":
        try:
            rawdata = request.body.decode('utf-8')
            resp = json.loads(rawdata)
            payment = Payment(
                payment_id = resp['id'],
                user = request.user,
                amount_paid = resp['purchase_units'][0]['amount']['value'],
                status = resp['status']
            )
            payment.save()
            last_order_id = Orders.objects.last().id
            Orders.objects.filter(id = last_order_id).update(payment_id = payment)
            order_data = Orders.objects.get(payment_id = payment) 
            cart_items  = Cart.objects.filter(user = request.user)
            for item in cart_items:
                orderPet = OrderPet()
                orderPet.order_id = order_data
                orderPet.user = request.user
                orderPet.payment = payment
                orderPet.Pet = item.Pet
                orderPet.quantity = item.quantity
                orderPet.pet_price = item.Pet.price
                orderPet.is_ordered = True
                orderPet.save()
            
            send_order_email(order_data,cart_items)
            cart_items.delete() #remove items from cart

        except json.JSONDecodeError as e:
            return JsonResponse({'error':str(e)})
        

    else:
        serialized_data = request.GET.get('data')

        if serialized_data:
            sdata = json.loads(serialized_data)
            orders = Orders.objects.get(pk = sdata['orders']) 
            order_number = Orders.order_bumber
            cart_item = Cart.objects.filter(pk__in = sdata['cart_item'])
            total_amount = sdata['total_amount']
            context={
                'orders':orders,
                'order_number':order_number,
                'cart_item':cart_item,
                'total_amount':total_amount
            }
    return render(request,"order/payment_page.html",context)

def show_orders(request):
    auth_user = request.user
    order_data = OrderPet.objects.filter(user = auth_user)
    flag = order_data.exists() 

    status_badge_map = {
        'new':'primary',
        'pending':'warning',
        'deliverd':'success',
        'cancelled':'danger'
    }

    #Retrive order along with assosiated order item
    orders = OrderPet.objects.filter(user = auth_user).select_related('order_id','Pet').order_by('-order_id__created_at')

    #Group order by order number
    orderGroup = {}
    for order in orders:
        order_number = order.order_id.order_bumber
        # print(f'order no is {type(order_number)}')
        if order_number not in orderGroup:
            orderGroup[order_number] = {
                'order_date':order.order_id.created_at.date(),
                'status':order.order_id.status,
                'status_badge_map':status_badge_map.get(order.order_id.status,'secondary'),
                'order_number':order_number,
                'grand_total':0,
                'items':[]
            }
        orderGroup[order_number]['grand_total'] += order.pet_price
        total_price_per_item = order.quantity * order.pet_price
        orderGroup[order_number]['items'].append({
            'item_name':order.Pet.name,
            'item_price':order.pet_price,
            'quantity':order.quantity,
            'total_price_per_item':total_price_per_item
        })    
    
    context = {
        'order_group_data':orderGroup.values(),
        'flag':flag
    }
    return render(request,'order/myorders.html',context)
 
def create_order_pdf(order,cart_items):
    buffer  = BytesIO()
    doc = SimpleDocTemplate(buffer,pagesize = letter)
    elements = []
    #Add customer details
    customer_info = [
        ["Customer Name:",order.first_name],
        ["Address:",order.address],
        ["Phone:",order.phone]
    ]
    
    customer_table = Table(customer_info)
    customer_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
    ]))

    elements.append(customer_table)
    #For Spacing between Customer details & item table.
    elements.append(Spacer(0,20))

    #Adding Ordered Item
    item_data  = [["Item","Quantity","Price","Total"]]

    for item in cart_items:
        item_data.append([item.Pet.name,item.quantity,item.Pet.price,item.Pet.price*item.quantity])

    item_table  = Table(item_data,colWidths=[300,70,70,90])
    item_table.setStyle(TableStyle([
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ]))

    # main_data = [customer_table,item_table]

    elements.append(item_table)

    #Building PDf
    doc.build(elements)
    pdf_content  = buffer.getvalue()
    buffer.close()
    return pdf_content


def send_order_email(order,cart_items):
    subject = "Your Order Details"
    from_email = settings.DEFAULT_FROM_EMAIL #Local Host
    recipient_email = order.user.email

    email_body  = "Thank you for placing order, please check your order invoice attachment for your reference."
    pdf_content  = create_order_pdf(order,cart_items)

    #attachement of pdf
    pdf_attachment  = ("order_invoice.pdf",pdf_content,"application/pdf")   

    email = EmailMessage(subject,email_body,from_email,[recipient_email])
    email.content_subtype = "html"
    email.attach("order_details.pdf",pdf_content,"appication/pdf")
    email.send(fail_silently=False)




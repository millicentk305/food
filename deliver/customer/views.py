from django.shortcuts import render
#from django.http import HttpResponse
from django.views import View
from .models import MenuItem, OrderModel, Category

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        #get every item from each category
        main = MenuItem.objects.filter(category__name__contains='Main')
        starters = MenuItem.objects.filter(category__name__contains='Starters')
        desserts = MenuItem.objects.filter(category__name__contains='Desserts')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')
        #pass into context
        context = {
            'main': main,
            'starters': starters,
            'desserts': desserts,
            'drinks': drinks,
        }
        #render the remplate
        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

            for item in order_items['items']:
                price += item['price']
                item_ids.append(item['id'])

            order = OrderModel.objects.create(
                price=price,
                name = name,
                email = email,
                street = street,
                city = city,
                state = state,
                zip_code = zip_code
            )
            order.items.add(*item_ids)

            context = {
                'items': order.items['items'],
                'price': price    
            }
            return render(request,'customer/order_confirmation.html', context)
            #return HttpResponse(request,'customer/order_confirmation.html', context)
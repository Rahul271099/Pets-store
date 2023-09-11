from django.shortcuts import render,HttpResponse
from .models import pet
from django.http import Http404
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def pets_list(request):
    pets_data = pet.objects.all()
    data = {'pets_d':pets_data}
    return render(request,'first_app/list.html',data)

def pets_details(request,pk):
    query = pet.objects.filter(id=pk)
    query2 = pet.objects.all()[0:3]
    if query.exists() and query.count()==1:
        instance = query.first()
        query2
    else:
        return Http404("Pet data does not exists")
    
    context = {'data1':instance,'data2':query2}
    
    
    return render(request,'first_app/detail.html',context)

def dog_list(request):
    category_data = pet.objects.filter(animal_type = 'D')
    data_dog = {
        'object1':category_data
    }
    return render(request,'first_app/dog-list.html',data_dog)

def cat_list(request):
    category_data = pet.objects.filter(animal_type = 'C')
    cat_list = {
        'object1':category_data
    }
    return render(request,'first_app/cat-list.html',cat_list)

# def random_list_data(request,type):
#     catogery1 = pet.objects.filter(animal_type = type)

#     if type == 'C':
#         type = 'C'
#     else:
#         type = 'D'
    
#     list_random_data = {
#         'object1':catogery1
#     }
    
#     return render(request,'first_app/cat-list.html',list_random_data)

def search_results(request):
    
    search_pets = request.GET['search_pets']
    # count_pets = len(search_pets)
    # print('Count',count_pets) 
    # if count_pets < 1:
    #     return HttpResponse("0")
    # results_name = pet.objects.filter(name__icontains = search_pets)
    # results_species = pet.objects.filter(Species__icontains = search_pets)
    # results_gender = pet.objects.filter(gender__icontains = search_pets)
    # results_price = pet.objects.filter(price__gte = search_pets)
     
    search_filter = (Q(name__icontains = search_pets) | Q(Species__icontains = search_pets) | Q(breed__icontains = search_pets))
    
    
    results = pet.objects.filter(search_filter)
    
    # results = results_name.union(results_price,results_species,results_gender)  

    context = {
        'data':results,
        'query':search_pets
    }
    return render(request,'first_app/search-list.html',context)

def search_results2(request):
    if request.method == "GET":
        search_data = request.GET.get('search_pets')
        
        
       
        query = (Q(name__icontains = search_data) | Q(Species__icontains = search_data) | Q(breed__icontains = search_data))    

        result = pet.objects.filter(query)

        context = {
            'data':result,
            'query':search_data
        }
        return render(request,'first_app/search-list.html',context)
    
    else:
        return HttpResponse("Invalid Method")    
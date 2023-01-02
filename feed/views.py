from django.shortcuts import render


def home_page_view(request):
    context = {}
    
    list_of_values = []
    list_of_values.append('object1')
    list_of_values.append('object2')
    list_of_values.append('object3')
    list_of_values.append('object4')

    context['list_of_values'] = list_of_values
    return render(request, 'index.html', context)
from django.shortcuts import render

# function to return the index.html template
def get_index(request):
    return render(request, 'index.html')


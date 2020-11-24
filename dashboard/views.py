from django.shortcuts import render

# Create your views here.


class Dashboard(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hello.html')

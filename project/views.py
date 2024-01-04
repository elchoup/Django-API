from django.shortcuts import render

# Create your views here.
var jsonData = pm.response.json();
pm.environment.set("token", jsonData.access);
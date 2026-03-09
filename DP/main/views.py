import pandas as pd
from django.shortcuts import render

def index(request):
    if request.method == "POST" and request.FILES.get("datafile"):
        file = request.FILES["datafile"]

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        print(df.head())
    return render(request, 'main/index.html')

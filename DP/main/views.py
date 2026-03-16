import pandas as pd
from django.shortcuts import render


def index(request):

    labels = []
    values = []
    data = ""

    if request.method == "POST" and request.FILES.get("datafile"):

        file = request.FILES["datafile"]

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        # взимаме първите две колони
        labels = df.iloc[:, 0].tolist()
        values = df.iloc[:, 1].tolist()

        # таблица за показване в страницата
        data = df.to_html(classes="table table-bordered table-hover table-striped")

    context = {
        "labels": labels,
        "values": values,
        "data": data
    }

    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')
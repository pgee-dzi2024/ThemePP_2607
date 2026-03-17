import pandas as pd
from django.shortcuts import render


def index(request):

    labels = []
    values = []
    data = ""
    max_month = ""
    max_value = 0

    if request.method == "POST" and request.FILES.get("datafile"):

        file = request.FILES["datafile"]

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        # взимаме първите две колони
        labels = df.iloc[:, 0].tolist()
        values = df.iloc[:, 1].tolist()

        # НАЙ-СИЛЕН МЕСЕЦ
        max_index = df.iloc[:, 1].idxmax()
        max_month = df.iloc[max_index, 0]
        max_value = df.iloc[max_index, 1]

        # таблица
        data = df.to_html(classes="table table-bordered table-hover table-striped")

    context = {
        "labels": labels,
        "values": values,
        "data": data,
        "max_month": max_month,
        "max_value": max_value,
        "total": total,
        "average": average,
    }

    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')
import pandas as pd
from django.shortcuts import render


def index(request):

    labels = []
    values = []
    data = ""
    max_month = ""
    max_value = 0
    total = 0
    average = 0

    if request.method == "POST" and request.FILES.get("datafile"):

        file = request.FILES["datafile"]

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        # 1. намираме числова колона автоматично
        numeric_columns = df.select_dtypes(include=['number']).columns

        if len(numeric_columns) > 0:
            values = df[numeric_columns[0]].fillna(0).tolist()
        else:
            values = []

        #  2. намираме текстова колона (за labels)
        text_columns = df.select_dtypes(include=['object']).columns

        if len(text_columns) > 0:
            labels = df[text_columns[0]].fillna("").tolist()
        else:
            labels = [str(i) for i in range(len(values))]

        #  3. защитa (винаги числа)
        values = [float(v) for v in values]

        #  4. изчисления
        if values:
            total = sum(values)
            average = round(total / len(values), 2)

            max_index = values.index(max(values))
            max_month = labels[max_index] if labels else ""
            max_value = values[max_index]

        # таблица
        data = df.to_html(
            index=False,
            classes="table table-bordered table-striped text-center w-100"
        )

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
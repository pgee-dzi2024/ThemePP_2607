from .models import Analysis
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64


def plot_to_base64():
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    return image


@login_required
def index(request):

    labels = []
    values = []
    data = ""

    max_month = ""
    max_value = 0
    min_value = 0
    variation = 0
    total = 0
    average = 0

    uploaded_file_name = None

    line_chart = None
    pie_chart = None
    bar_chart = None
    histogram_chart = None

    df = None
    error_message = None

    if request.method == "POST":

        file = request.FILES.get("datafile")

        # 📌 КАЧВАНЕ
        if file:
            uploaded_file_name = file.name

            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)

            request.session['data'] = df.to_json()
            request.session['filename'] = file.name

        else:
            data_json = request.session.get('data')

            if data_json:
                df = pd.read_json(data_json)
                uploaded_file_name = request.session.get('filename')


        if df is not None:

            numeric_columns = df.select_dtypes(include=['number']).columns
            text_columns = df.select_dtypes(include=['object']).columns

            label_col = text_columns[0] if len(text_columns) > 0 else None
            value_col = numeric_columns[0] if len(numeric_columns) > 0 else None


            # ✅ ФИЛТЪР
            min_filter = request.POST.get("min_filter")

            if min_filter and value_col:
                try:
                    number = int(min_filter.replace("≥", "").strip())
                    df = df[df[value_col] >= number]
                except:
                    pass


            #  ГРУПИРАНЕ
            group_by = request.POST.get("group_by")

            if group_by == "month" and label_col and value_col:
                df = df.groupby(label_col)[value_col].sum().reset_index()


            if df.empty:
                error_message = "Няма резултати"

            if value_col:
                values = df[value_col].fillna(0).tolist()

            if label_col:
                labels = df[label_col].fillna("").tolist()

            values = [float(v) for v in values]


            if values:

                total = sum(values)
                average = round(total / len(values), 2)

                max_index = values.index(max(values))
                max_month = labels[max_index]

                max_value = max(values)
                min_value = min(values)
                variation = max_value - min_value

                plt.figure(figsize=(7, 4))
                plt.plot(values, marker='o')
                plt.xticks(range(len(labels)), labels, rotation=45)
                plt.title("Приходи")
                line_chart = plot_to_base64()

                plt.figure(figsize=(6, 6))
                plt.pie(values, labels=labels, autopct='%1.1f%%')
                plt.title("Разпределение")
                pie_chart = plot_to_base64()

                plt.figure(figsize=(7, 4))
                plt.bar(labels, values)
                plt.xticks(rotation=45)
                plt.title("Стълбовидна")
                bar_chart = plot_to_base64()

                plt.figure(figsize=(7, 4))
                plt.hist(values, bins=6)
                plt.title("Хистограма")
                histogram_chart = plot_to_base64()

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
        "min_value": min_value,
        "variation": variation,
        "total": total,
        "average": average,
        "uploaded_file_name": uploaded_file_name,
        "line_chart": line_chart,
        "pie_chart": pie_chart,
        "bar_chart": bar_chart,
        "histogram_chart": histogram_chart,
        "error_message": error_message,
    }

    return render(request, 'main/index.html', context)

def about(request):
    return render(request, "main/about.html")

def about(request):
    return render(request, "main/about.html")

def user_login(request):
    error = None


    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            error = "Грешно име или парола"

    return render(request, "main/login.html", {"error": error})


def register(request):
    error = None


    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1 or not password2:
            error = "Попълни всички полета"

        elif password1 != password2:
            error = "Паролите не съвпадат"

        elif User.objects.filter(username=username).exists():
            error = "Потребителят вече съществува"

        else:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect("index")

    return render(request, "main/register.html", {"error": error})


def user_logout(request):
    logout(request)
    return redirect("index")

@login_required
def history(request):
    analyses = Analysis.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "main/history.html", {"analyses": analyses})

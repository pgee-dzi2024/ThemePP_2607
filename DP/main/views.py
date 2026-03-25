from .models import Analysis
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.shortcuts import render, redirect

# AUTH
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Django + Matplotlib
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64


def plot_to_base64():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
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

    if request.method == "POST" and request.FILES.get("datafile"):

        file = request.FILES["datafile"]
        uploaded_file_name = file.name

        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                df = None

            if df is not None:

                numeric_columns = df.select_dtypes(include=['number']).columns
                values = df[numeric_columns[0]].fillna(0).tolist() if len(numeric_columns) > 0 else []

                text_columns = df.select_dtypes(include=['object']).columns
                labels = df[text_columns[0]].fillna("").tolist() if len(text_columns) > 0 else [str(i) for i in range(len(values))]

                values = [float(v) for v in values]

                if values:
                    total = sum(values)
                    average = round(total / len(values), 2)

                    max_index = values.index(max(values))
                    max_month = labels[max_index]
                    max_value = values[max_index]
                    min_value = min(values)
                    variation = max_value - min_value

                    Analysis.objects.create(
                        user=request.user,
                        filename=file.name,
                        total=total,
                        average=average
                    )
                    plt.style.use('seaborn-v0_8')

                    # LINE
                    plt.figure(figsize=(7, 4))
                    plt.plot(values, marker='o', color='#4e73df')
                    plt.xticks(range(len(labels)), labels, rotation=45)
                    plt.title("Приходи")
                    plt.grid(alpha=0.3)
                    line_chart = plot_to_base64()

                    # PIE
                    colors = [
                        "#4e73df","#1cc88a","#36b9cc","#f6c23e","#e74a3b",
                        "#6f42c1","#17a2b8","#20c997","#6610f2","#fd7e14",
                        "#28a745","#ffc107"
                    ]

                    plt.figure(figsize=(6, 6))
                    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
                    plt.title("Разпределение")
                    pie_chart = plot_to_base64()

                    # BAR
                    plt.figure(figsize=(7, 4))
                    plt.bar(labels, values, color="#1cc88a")
                    plt.xticks(rotation=45)
                    plt.title("Стълбовидна")
                    plt.grid(axis='y', alpha=0.3)
                    bar_chart = plot_to_base64()

                    # HISTOGRAM
                    plt.figure(figsize=(7, 4))
                    plt.hist(values, bins=6, color="#36b9cc")
                    plt.title("Хистограма")
                    plt.grid(alpha=0.3)
                    histogram_chart = plot_to_base64()

                data = df.to_html(
                    index=False,
                    classes="table table-bordered table-striped text-center w-100"
                )

        except Exception as e:
            print("ERROR:", e)

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
    }

    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')


# LOGIN
def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')   # ВАЖНО
        else:
            error = "Грешно име или парола"

    return render(request, 'main/login.html', {"error": error})


# REGISTER
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
            return redirect('index')   # ВАЖНО

    return render(request, 'main/register.html', {"error": error})


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def history(request):
    analyses = Analysis.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/history.html', {'analyses': analyses})
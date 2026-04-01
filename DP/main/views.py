from .models import Analysis
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64


# ======================
# 📊 ГРАФИКА → BASE64
# ======================
def plot_to_base64():
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.close()
    return image


# ======================
# 🏠 MAIN PAGE
# ======================
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

            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                elif file.name.endswith(".xlsx"):
                    df = pd.read_excel(file)
            except Exception as e:
                error_message = f"Грешка при четене: {e}"

        if df is None:
            error_message = "Няма качени данни"

        if df is not None:

            numeric_columns = df.select_dtypes(include=['number']).columns
            text_columns = df.select_dtypes(include=['object']).columns

            label_col = text_columns[0] if len(text_columns) > 0 else None
            value_col = numeric_columns[0] if len(numeric_columns) > 0 else None

            # ======================
            # ✅ ФИЛТЪР
            # ======================
            min_filter = request.POST.get("min_filter")

            if min_filter and value_col:
                try:
                    number = float(min_filter.replace("≥", "").strip())
                    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
                    df = df[df[value_col] >= number]
                except:
                    pass

            # ======================
            # ✅ ГРУПИРАНЕ ПО МЕСЕЦ
            # ======================
            group_by = request.POST.get("group_by")

            if group_by == "month":

                date_column = None

                for col in df.columns:
                    try:
                        converted = pd.to_datetime(df[col], errors='coerce')

                        if converted.notna().sum() > 0:
                            df[col] = converted
                            date_column = col
                            break
                    except:
                        continue

                if date_column and value_col:
                    df['month'] = df[date_column].dt.to_period('M').astype(str)
                    df = df.groupby('month')[value_col].sum().reset_index()
                    label_col = 'month'
                    df = df.sort_values(by='month')

            if df.empty:
                error_message = "Няма резултати"

            if value_col in df.columns:
                values = df[value_col].fillna(0).tolist()

            if label_col in df.columns:
                labels = df[label_col].fillna("").astype(str).tolist()

            values = [float(v) for v in values]

            # ======================
            # 📈 СТАТИСТИКА
            # ======================
            if values:
                total = sum(values)
                average = round(total / len(values), 2)

                max_index = values.index(max(values))
                max_month = labels[max_index]

                max_value = max(values)
                min_value = min(values)
                variation = max_value - min_value

                colors = ['#4f46e5', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#a855f7']

                # LINE
                plt.figure(figsize=(6, 3))
                plt.plot(values, marker='o', color='#4f46e5')
                plt.xticks(range(len(labels)), labels, rotation=30)
                line_chart = plot_to_base64()

                # PIE
                plt.figure(figsize=(7, 7))
                plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
                pie_chart = plot_to_base64()

                # BAR
                plt.figure(figsize=(6, 3))
                plt.bar(labels, values, color='#22c55e')
                plt.xticks(rotation=30)
                bar_chart = plot_to_base64()

                # HIST
                plt.figure(figsize=(6, 3))
                plt.hist(values, bins=6, color='#f59e0b')
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


# ======================
# 🔐 LOGIN
# ======================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")

    return render(request, "main/login.html")


# ======================
# 📝 REGISTER
# ======================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            User.objects.create_user(username=username, password=password)
            return redirect("login")

    return render(request, "main/register.html")


# ======================
# 🚪 LOGOUT
# ======================
def user_logout(request):
    logout(request)
    return redirect("login")


# ======================
# 📜 HISTORY
# ======================
@login_required
def history(request):
    return render(request, "main/history.html")

def about(request):
    return render(request, "main/about.html")
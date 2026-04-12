from .models import Analysis
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import io
import base64
import os
import uuid


# ======================
# 📊 ГРАФИКА → BASE64
# ======================
def plot_to_base64():
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
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

    uploaded_file_name = request.session.get("uploaded_file_name")

    line_chart = None
    pie_chart = None
    bar_chart = None
    histogram_chart = None
    download_ready = False

    df = None
    error_message = None

    numeric_columns = []
    text_columns = []
    date_columns = []

    selected_label_col = ""
    selected_value_col = ""
    selected_date_col = ""
    selected_agg = "sum"

    rows_count = 0
    cols_count = 0
    dtypes_info = {}
    missing_info = {}

    if request.method == "POST":
        file = request.FILES.get("datafile")
        session_file_path = request.session.get("uploaded_file_path")

        # 1) Качване на нов файл
        if file:
            uploaded_file_name = file.name

            if not (file.name.endswith(".csv") or file.name.endswith(".xlsx")):
                error_message = "Неподдържан формат. Разрешени са само .csv и .xlsx"
            else:
                uploads_dir = settings.MEDIA_ROOT / "uploads"
                os.makedirs(uploads_dir, exist_ok=True)

                ext = ".csv" if file.name.endswith(".csv") else ".xlsx"
                saved_name = f"{uuid.uuid4().hex}{ext}"
                saved_path = uploads_dir / saved_name

                with open(saved_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                request.session["uploaded_file_path"] = str(saved_path)
                request.session["uploaded_file_name"] = uploaded_file_name
                session_file_path = str(saved_path)

        # 2) Четене от последния качен файл (за филтри/групиране без нов upload)
        if session_file_path and not error_message:
            try:
                if session_file_path.endswith(".csv"):
                    df = pd.read_csv(session_file_path)
                elif session_file_path.endswith(".xlsx"):
                    df = pd.read_excel(session_file_path)
            except Exception as e:
                error_message = f"Грешка при четене на файла: {e}"

        if df is None and not error_message:
            error_message = "Няма качени данни"

        if df is not None:
            if df.empty:
                error_message = "Файлът е празен"
            else:
                rows_count, cols_count = df.shape
                dtypes_info = {col: str(dtype) for col, dtype in df.dtypes.items()}
                missing_info = {col: int(df[col].isna().sum()) for col in df.columns}

                numeric_columns = list(df.select_dtypes(include=["number"]).columns)
                text_columns = list(df.select_dtypes(include=["object"]).columns)

                # Потенциални дата-колони
                for col in df.columns:
                    parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
                    if parsed.notna().sum() > 0:
                        date_columns.append(col)

                if not numeric_columns:
                    error_message = "Няма числова колона за анализ"

        if df is not None and not error_message:
            selected_label_col = request.POST.get("label_col", "")
            selected_value_col = request.POST.get("value_col", "")
            selected_date_col = request.POST.get("date_col", "")
            selected_agg = request.POST.get("agg_func", "sum")

            if selected_agg not in ["sum", "mean"]:
                selected_agg = "sum"

            if not selected_value_col or selected_value_col not in df.columns:
                selected_value_col = numeric_columns[0] if numeric_columns else ""

            if selected_label_col and selected_label_col not in df.columns:
                selected_label_col = ""

            if not selected_label_col:
                selected_label_col = text_columns[0] if text_columns else df.columns[0]

            if selected_date_col and selected_date_col not in date_columns:
                selected_date_col = ""

            label_col = selected_label_col
            value_col = selected_value_col

            # ✅ ФИЛТЪР
            min_filter = request.POST.get("min_filter")
            if min_filter and value_col:
                try:
                    number = float(min_filter.replace("≥", "").strip())
                    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
                    df = df[df[value_col] >= number]
                except Exception:
                    error_message = "Невалиден филтър"

            # ✅ ГРУПИРАНЕ
            group_by = request.POST.get("group_by")
            if group_by == "month" and not error_message:
                date_column = selected_date_col if selected_date_col else None

                if not date_column:
                    for col in date_columns:
                        if col != value_col:
                            date_column = col
                            break

                if date_column and value_col in df.columns:
                    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
                    df = df.dropna(subset=[value_col]).copy()

                    df["_parsed_date"] = pd.to_datetime(df[date_column], errors="coerce", dayfirst=True)
                    df = df.dropna(subset=["_parsed_date"]).copy()

                    if df.empty:
                        error_message = "Няма валидни данни след групиране по месец"
                    else:
                        df["month"] = df["_parsed_date"].dt.to_period("M").astype(str)

                        if selected_agg == "mean":
                            df = df.groupby("month", as_index=False)[value_col].mean()
                        else:
                            df = df.groupby("month", as_index=False)[value_col].sum()

                        label_col = "month"
                        df = df.sort_values(by="month")
                else:
                    error_message = "Изберете валидна дата колона за групиране"

            if not error_message and (value_col not in df.columns or label_col not in df.columns):
                error_message = "Избраните колони не са валидни"

            if not error_message:
                chart_df = df[[label_col, value_col]].copy()
                chart_df[value_col] = pd.to_numeric(chart_df[value_col], errors="coerce")
                chart_df = chart_df.dropna(subset=[value_col])
                chart_df[label_col] = chart_df[label_col].fillna("").astype(str)

                if chart_df.empty:
                    error_message = "Няма валидни редове за визуализация"

            if not error_message:
                labels = chart_df[label_col].tolist()
                values = [float(v) for v in chart_df[value_col].tolist()]

                total = sum(values)
                average = round(total / len(values), 2)

                max_index = values.index(max(values))
                max_month = labels[max_index]

                max_value = max(values)
                min_value = min(values)
                variation = max_value - min_value

                colors = ["#4f46e5", "#22c55e", "#f59e0b", "#ef4444", "#06b6d4", "#a855f7"]

                # LINE
                plt.figure(figsize=(6, 3))
                plt.plot(values, marker="o", color="#4f46e5")
                plt.xticks(range(len(labels)), labels, rotation=30)
                line_chart = plot_to_base64()

                # PIE
                plt.figure(figsize=(7, 7))
                plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors)
                pie_chart = plot_to_base64()

                # BAR
                plt.figure(figsize=(6, 3))
                plt.bar(labels, values, color="#22c55e")
                plt.xticks(rotation=30)
                bar_chart = plot_to_base64()

                # HIST
                plt.figure(figsize=(6, 3))
                plt.hist(values, bins=6, color="#f59e0b")
                histogram_chart = plot_to_base64()

                # История
                Analysis.objects.create(
                    user=request.user,
                    filename=uploaded_file_name or "unknown",
                    total=round(total, 2),
                    average=average,
                )

                # Таблица за показване
                data = df.to_html(
                    index=False,
                    classes="table table-bordered table-striped text-center w-100"
                )

                # Експорт CSV
                exports_dir = settings.MEDIA_ROOT / "exports"
                os.makedirs(exports_dir, exist_ok=True)
                export_name = f"user_{request.user.id}_{uuid.uuid4().hex}.csv"
                export_path = exports_dir / export_name
                df.to_csv(export_path, index=False, encoding="utf-8-sig")
                request.session["last_export_csv_path"] = str(export_path)
                download_ready = True

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
        "numeric_columns": numeric_columns,
        "text_columns": text_columns,
        "date_columns": date_columns,
        "selected_label_col": selected_label_col,
        "selected_value_col": selected_value_col,
        "selected_date_col": selected_date_col,
        "selected_agg": selected_agg,
        "rows_count": rows_count,
        "cols_count": cols_count,
        "dtypes_info": dtypes_info,
        "missing_info": missing_info,
        "download_ready": download_ready,
    }

    return render(request, "main/index.html", context)


# ======================
# 🔐 LOGIN
# ======================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Моля, попълнете потребителско име и парола.")
            return render(request, "main/login.html")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")

        messages.error(request, "Невалидно потребителско име или парола.")

    return render(request, "main/login.html")


# ======================
# 📝 REGISTER
# ======================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Полетата са задължителни.")
            return render(request, "main/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Това потребителско име вече съществува.")
            return render(request, "main/register.html")

        if len(password) < 6:
            messages.error(request, "Паролата трябва да е поне 6 символа.")
            return render(request, "main/register.html")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Регистрацията е успешна. Влезте в профила си.")
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
    analyses = Analysis.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "main/history.html", {"analyses": analyses})


# ======================
# ⬇️ CSV DOWNLOAD
# ======================
@login_required
def download_csv(request):
    export_path = request.session.get("last_export_csv_path")

    if not export_path or not os.path.exists(export_path):
        raise Http404("Няма наличен файл за изтегляне.")

    file_handle = open(export_path, "rb")
    return FileResponse(
        file_handle,
        as_attachment=True,
        filename="analysis_export.csv",
        content_type="text/csv",
    )


# ======================
# 🧹 CLEAR CURRENT ANALYSIS SESSION
# ======================
@login_required
def clear_analysis_session(request):
    uploaded_path = request.session.pop("uploaded_file_path", None)
    export_path = request.session.pop("last_export_csv_path", None)
    request.session.pop("uploaded_file_name", None)

    for path in [uploaded_path, export_path]:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

    messages.info(request, "Сесията за анализ е изчистена.")
    return redirect("index")


def about(request):
    return render(request, "main/about.html")
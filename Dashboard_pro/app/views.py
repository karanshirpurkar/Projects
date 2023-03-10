from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from app.models import Register
from app.models import upload
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.forms import forms
import pandas as pd
import plotly.express as px
from .forms import uploadform
import requests

global selected_name, graph_data, charts
charts = []
graph_data = []
selected_name = []


def get_name(request):
    file_name = []
    next = None
    names = upload.objects.all()
    for i in names:
        file_name.append(i.file.name[5:])
    if request.method == "POST":
        selected_name.append(request.POST.get("file"))
        next = "show"
    return render(request, "./chart/filename.html", {"file_name": file_name, "next": next})


def index(request):
    return render(request, "user/home.html")
# Create your views here.


def feature(request):
    return render(request, "./user/feature.html")


def pricing(request):
    return render(request, "./user/pricing.html")


def service(request):
    return render(request, "./user/service.html")


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get("first")
        last_name = request.POST.get("last")
        city = request.POST.get("city")
        state = request.POST.get("state")
        email = request.POST.get("email")
        password = request.POST.get("password")
        call = Register(first_name=first_name, last_name=last_name, city=city,
                        state=state, email=email, password=password, date=datetime.today())
        call.save()
    return render(request, "./user/register.html")


def login_user(request):
    next = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, ("Login Successful"))
            login(request, user)
            next = "login"
        else:
            messages.success(
                request, ("There is an error in logging in, try again"))
            print("not")
            return redirect("login")
       # Return an 'invalid login' error message.
    return render(request, "./user/login.html", {"next": next})


def chart(request):
    db = pd.read_csv(
        "D://final project//new_18_night//final project//Dashboard_pro//app/data_file//car.csv")

    return render(request, "./chart/chart.html", {'df': db.head().to_html(), 'describe': db.describe().to_html(), 'keys': db.keys, 'label': label, 'data': data})


def show(request):
    name_string = "D://final project//new_18_night//final project//Dashboard_pro//media//data//" + \
        selected_name[-1]
    if selected_name[-1].endswith("csv"):
        data = pd.read_csv(name_string)
    if selected_name[-1].endswith("xls"):
        data = pd.read_excel(name_string)
    if request.method == 'POST':
        column = request.POST.get("x")
        data = data.sort_values(by=[column])

    graph_data.append(data)

    return render(request, "./chart/data_show.html", {'keys': data.keys(), 'db': data.to_html(classes='table table-striped text-center', justify='center', index=False)})


def linechart(request):
    db = graph_data[-1]
    fig_l = px.line([1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")

        fig_l = px.line(db, x=x_axis, y=y_axis, title=title)
        charts.append(fig_l.to_html())
        hint = "Provided Output"
    return render(request, "./chart/linechart.html", {'keys': db.keys(), 'fig': fig_l.to_html(), 'hint': hint})


def barchart(request):
    db = graph_data[-1]
    fig_b = px.bar([1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        color = request.POST.get("color")

        fig_b = px.bar(db, x=x_axis, y=y_axis, title=title, color=color)
        charts.append(fig_b.to_html())
        hint = "Provided Output"
    return render(request, "./chart/barchart.html", {'keys': db.keys(), 'fig': fig_b.to_html(), 'hint': hint})


def scatterchart(request):
    db = graph_data[-1]
    fig_s = px.scatter([1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        color = request.POST.get("color")

        fig_s = px.scatter(db, x=x_axis, y=y_axis, title=title, color=color)
        charts.append(fig_s.to_html())
        hint = "Provided Output"
    return render(request, "./chart/scatterchart.html", {'keys': db.keys(), 'fig': fig_s.to_html(), 'hint': hint})


def piechart(request):
    db = graph_data[-1]
    fig_p = px.pie(values=[1, 2, 3, 4], names=[
                   "Nick", "Jona", "Siri", "Jaggu"])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")

        fig_p = px.pie(db, values=x_axis, names=y_axis, title=title)
        charts.append(fig_p.to_html())
        hint = "Provided Output"
    return render(request, "./chart/piechart.html", {'keys': db.keys(), 'fig': fig_p.to_html(), 'hint': hint})


def boxchart(request):
    db = graph_data[-1]
    fig_x = px.scatter([1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        color = request.POST.get("color")

        fig_x = px.box(db, x=x_axis, y=y_axis, title=title, color=color)
        charts.append(fig_x.to_html())
        hint = "Provided Output"
    return render(request, "./chart/boxchart.html", {'keys': db.keys(), 'fig': fig_x.to_html(), 'hint': hint})


def violinechart(request):
    db = graph_data[-1]
    fig_v = px.violin([1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        color = request.POST.get("color")

        fig_v = px.violin(db, x=x_axis, y=y_axis, title=title, color=color)
        charts.append(fig_v.to_html())
        hint = "Provided Output"
    return render(request, "./chart/violinechart.html", {'keys': db.keys(), 'fig': fig_v.to_html(), 'hint': hint})


def scatter3dchart(request):
    db = graph_data[-1]
    fig_s3 = px.scatter_3d([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        z_axis = request.POST.get("z")
        color = request.POST.get("color")

        fig_s3 = px.scatter_3d(db, x=x_axis, y=y_axis,
                               z=z_axis, title=title, color=color)
        charts.append(fig_s3.to_html())
        hint = "Provided Output"
    return render(request, "./chart/scatter3dchart.html", {'keys': db.keys(), 'fig': fig_s3.to_html(), 'hint': hint})


def line3dchart(request):
    db = graph_data[-1]
    fig_l3 = px.line_3d([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4])
    hint = "Sample Chart"
    if request.method == 'POST':
        title = request.POST.get("title")
        x_axis = request.POST.get("x")
        y_axis = request.POST.get("y")
        z_axis = request.POST.get("z")

        fig_l3 = px.line_3d(db, x=x_axis, y=y_axis, z=z_axis, title=title)
        charts.append(fig_l3.to_html())
        hint = "Provided Output"
    return render(request, "./chart/line3dchart.html", {'keys': db.keys(), 'fig': fig_l3.to_html(), 'hint': hint})


def uploadfile(request):
    next = None
    if request.method == "POST":
        file = request.FILES['file']
        uploaded = upload(file=file)
        next = "uploaded"
        uploaded.save()
        messages.success(request, ("File Uploaded"))

    return render(request, "./chart/uploadfile.html", {"next": next})


def dashboard(request):
    return render(request, "./chart/dashboard.html", {"charts": charts})

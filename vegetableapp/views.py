from django.shortcuts import render, redirect
from .models import ModelVegetable, ModelImage
from .forms import FormVegetable, LoginForm, SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import request

import numpy as np
from PIL import Image
import csv
import torch
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from model import predict

@login_required
def classify(request):
    # vegetable_info = list(ModelVegetable.object.all())
    """
    with open('static/data/vegetable_dataset.csv', encoding='utf-8') as f:
        csv_data = csv.reader(f)
        data = []
        for i, data in enumerate(csv_data):
            name, price_firsthalf, price_secondhalf, price_info = data
            vegetable_info = ModelVegetable(vegetable_label=i, vegetable_name=name, vegetable_price_firsthalf=price_firsthalf, vegetable_price_secondhalf=price_secondhalf)
            vegetable_info.save()
    """
    if not request.method=='POST':
        form = FormVegetable(request.POST, request.FILES)
        return render(request, 'index.html', {'form': form})

    else:
        form = FormVegetable(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        image_name = request.FILES['image']
        image_url = f'media/documents/{image_name}'
        image = Image.open(image_url).convert('RGB')
        x = predict.transform(image) # predict.pyのtransform関数で前処理する
        x = x.unsqueeze(0) # batch 1 としての次元を最初に1つ加える
        device = torch.device('cpu')
        net = predict.Net().to(device).eval()
        net.load_state_dict(torch.load('model/vegetable_para50.pt', map_location=device))
        with torch.no_grad():
            y = net(x)
        y_proba = F.softmax(y, dim=1).max().detach().numpy() * 100
        y_proba = np.round(y_proba, 2)
        y_arg = y.argmax().detach().numpy()
        vegetable_info = ModelVegetable.objects.filter(vegetable_label = y_arg)
        if y_arg == 0:
            y_label = 'カボチャ'
        elif y_arg == 1:
            y_label = 'キュウリ'
        elif y_arg == 2:
            y_label = 'ジャガイモ'
        elif y_arg == 3:
            y_label = 'トマト'
        elif y_arg == 4:
            y_label = 'ナス'
        else:
            y_label = 'ニンジン'
        return render(request, 'result.html', {'image_url': image_url, 'vegetable_info': vegetable_info[0], 'y_label': y_label, 'y_proba': y_proba})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

class Logout(LogoutView):
    template_name = 'logout.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password)
            if new_user is not None:
                login(request,new_user)
            return redirect('index')

    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
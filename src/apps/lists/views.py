from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List

User = get_user_model()


def home_page(request):
    return render(request, "lists/home.html", {"form": ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "lists/list.html", {"list": list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.create_new(
            first_item_text=request.POST["text"],
            owner=request.user if request.user.is_authenticated else None,
        )
        return redirect(list_)
    return render(request, "lists/home.html", {"form": form})


def my_lists(request, email):
    user = User.objects.get(email=email)
    return render(request, "lists/my_lists.html", {"owner": user})

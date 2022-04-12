from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from documents import util

def my_custom_page_not_found_view(request,exception):
    return render(request,'404.html',status=404)

class UserChangeFormEdit(UserChangeForm):
    class Meta:
        model = User
        #fields = "__all__"
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserChangeFormEdit(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "User successfully updated")
            return redirect(reverse('profile_edit'))
        else:
            util.print_form_errors(request, form.errors)
            return redirect(reverse('profile_edit'))
    else:
        form = UserChangeFormEdit(instance=request.user)
        args = {'form': form}
        return render(request, 'profile_edit.html', args)


class PasswordChangeFormEdit(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeFormEdit(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password successfully changed")
            return redirect(reverse('change_password'))
        else:
            util.print_form_errors(request, form.errors)
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeFormEdit(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)

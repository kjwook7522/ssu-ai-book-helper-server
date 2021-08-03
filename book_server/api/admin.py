from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from api.models import User

class UserCreationForm(forms.ModelForm):
  student_id = forms.IntegerField(label='학번', widget=forms.NumberInput)
  email = forms.CharField(label='이메일', widget=forms.TextInput)
  name = forms.CharField(label='이름', widget=forms.TextInput)
  password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
  password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
  phone = forms.CharField(label='휴대폰 번호', widget=forms.TextInput)

  class Meta:
    model = User
    fields = '__all__'

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise ValidationError("Passwords don't match")
    return password2

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    if commit:
      user.save()
    return user


class UserChangeForm(forms.ModelForm):
  email = forms.CharField(label='이메일', widget=forms.TextInput)
  name = forms.CharField(label='이름', widget=forms.TextInput)
  phone = forms.CharField(label='휴대폰 번호', widget=forms.TextInput)
  password = ReadOnlyPasswordHashField()

  class Meta:
    model = User
    fields = '__all__'

class UserAdmin(BaseUserAdmin):
  form = UserChangeForm
  add_form = UserCreationForm

  list_display = ('student_id', 'name', 'email', 'phone', 'is_superuser', 'date_joined')
  list_filter = ()
  list_per_page = 20
  fieldsets = (
    (None, {'fields': ('name', 'email', 'phone')}),
    ('관리자 권한', {'fields': ('is_superuser',)}),
  )

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('student_id', 'email', 'name', 'password1', 'password2', 'phone'),
    }),
  )
  search_fields = ('student_id',)
  ordering = ('student_id',)
  filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
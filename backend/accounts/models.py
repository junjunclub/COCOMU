from django.contrib.auth.models import AbstractUser
from django.db import models

# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.account.utils import user_email, user_field,user_username
from django.contrib.auth.models import UserManager
from allauth.account.adapter import DefaultAccountAdapter


# Create your models here.
class User(AbstractUser):
    # User에 기본으로 포함된 필드
    # id
    # username
    # password
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined

    # 실명
    name = models.CharField(max_length=10)
    # 닉네임
    nickname = models.CharField(max_length=12)
    email = models.EmailField()
    birth = models.DateField()
    genre1 = models.IntegerField(null=True)
    genre2 = models.IntegerField(null=True)
    genre3 = models.IntegerField(null=True)
    ott = models.JSONField(null=True)
    objects = UserManager()
    # # 후순위
    # profile_img = models.ImageField()


# class CustomAccountAdapter(DefaultAccountAdapter):
#     def save_user(self, request,user,form, commit=True):
#         data = form.cleaned_data
#         first_name = data.get("first_name")
#         last_name = data.get("last_name")
#         email = data.get("email")
#         username = data.get("username")
#         name = data.get("name")
#         nickname = data.get("nickname")
#         genre1 = data.get("genre1")
#         genre2 = data.get("genre2")
#         genre3 = data.get("genre3")
#         birth = data.get("birth")

#         user_email(user,email)
#         user_username(user,username)
#         if first_name:
#             user_field(user, "first_name",first_name)
#         if last_name:
#             user_field(user, "last_name", last_name)
#         if name:
#             user_field(user, "name",name)
#         if nickname:
#             user_field(user, "nickname",nickname)
#         if genre1:
#             user_field(user, "genre1",genre1)
#         if genre2:
#             user_field(user, "genre2",genre2)
#         if genre3:
#             user_field(user, "genre3", genre3)
#         if birth:
#             user_field(user, "birth", birth)
#         if "password1" in data:
#             user.set_password(data["password1"])
#         else:
#             user.set_unusuable_password()
#         self.populate_username(request,user)
#         if commit:
#             user.save()
#         return user


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field

        user = super().save_user(request, user, form, False)

        user_field(user, "name", request.data.get("name"))
        user_field(user, "nickname", request.data.get("nickname"))
        user_field(user, "birth", request.data.get("birth"))
        user.save()
        return user

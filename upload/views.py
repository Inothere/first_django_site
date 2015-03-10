#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
import os, hashlib,run_sql
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

model=[]
salt = r'Rpk_2015^)CD!#%&('

def encode_MD5(origin,salt):
    info = origin + salt
    newinfo = hashlib.md5(info).hexdigest()
    return newinfo
model.append({'address':'eraser@163.com','password':encode_MD5('123456',salt)})

class MultiEmailField(forms.Field):
    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)

        for email in value:
            validate_email(email)
def validate_p(value):
    if not value:
        raise ValidationError(u'密码不能为空')

def validate_a(value):
    if not value:
        raise ValidationError(u'用户名不能为空')
    else:
        import re
        r = re.compile(r'[_a-z\d\-\./]+@[_a-z\d\-]+(\.[_a-z\d\-]+)*(\.(info|biz|com|edu|gov|net|am|bz|cn|cx|hk|jp|tw|vc|vn))$')

        if not r.match(value):
            raise  ValidationError(u'请输入合法的邮件地址')

class RegForm(forms.Form):
    mail_address=forms.CharField(max_length=1024,label=u'邮件地址')
    password=forms.CharField(max_length=50,label=u'密码',required=False)
    mail_address.validators.append(validate_a)
    password.validators.append(validate_p)


@csrf_exempt
def regist(request):
    all_student = get_all_student()
    if request.method=='POST':
        form = RegForm(request.POST)
        if form.is_valid():
            checked = checkAccount(request.POST.get('mail_address'),request.POST.get('password'))
            if checked:
                return render_to_response('success.html')
    else:
        form = RegForm()
    return render_to_response('uploadpage.html',{'form':form,'all_student':all_student})

def checkAccount(user,password):
    global model, salt
    isAvaliable = False
    sha1 = encode_MD5(password,salt)
    for item in model:
        if item['address'] == user and item['password']==sha1:
            isAvaliable = True
            break

    return isAvaliable

def get_all_student():
    raw=run_sql.search(simple_sql)
    jsonres=[]
    for item in raw:
        newitem = list(item)
        if item[1] =='m':
            newitem[1]=u'男'
        elif item[1] == 'f':
            newitem[1]=u'女'
        else:
            newitem[1]=u'未知'
        newitem[2]=str(item[2])
        jsonres.append(newitem)
    return jsonres

simple_sql="""select * from studentInfo
"""
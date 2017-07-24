# -*- coding: utf-8 -*-
from django import forms


from django.utils.safestring import mark_safe

class NewProject(forms.Form):
	name = forms.CharField(max_length=50)
	
class NewTime(forms.Form):
	d = forms.IntegerField()
	m = forms.CharField(max_length=10)
	
	h = forms.IntegerField()
	weekday = forms.CharField(max_length=20)
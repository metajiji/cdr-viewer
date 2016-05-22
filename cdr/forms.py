from django.contrib.admin import widgets
from .models import Asterisk
from django import forms


# class AsteriskForm(forms.Form):
    # calldate = forms.DateTimeField(widget=forms.DateTimeInput())

class AsteriskForm(forms.ModelForm):
    # calldate = forms.DateTimeField(required=False, widget=widgets.AdminSplitDateTime())
    calldate = forms.DateTimeField(required=False, widget=widgets.AdminDateWidget())

    class Meta:
        model = Asterisk
        fields = ('calldate', )
        # widgets = {
        #     # 'calldate': forms.DateTimeInput(attrs=settings.DATETIMEPICKER_ATTRS),
        #     'calldate': forms.DateTimeInput(),
        # }

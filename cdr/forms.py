from django.utils.translation import ugettext_lazy as _
from django import forms


class DateTimeForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class DurationTimeForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class AsteriskForm(forms.Form):
    rows = forms.IntegerField(max_value=50, min_value=3, required=False, label=_('Rows per page'))
    datetime = forms.CharField(required=False, label=_('Date and time range'))
    duration = forms.CharField(required=False, label=_('Duration range'))

    FILTER_CHOICES = (
        ('start', _('Starts with'),),
        ('end', _('Ends with'),),
        ('equal', _('Equal'),),
        ('contains', _('Contains'),),)
    # src_number
    src_number = forms.CharField(required=False, label=_('Src Number'))
    src_number_not = forms.BooleanField(required=False, label=_('not'))
    src_number_option = forms.ChoiceField(required=False, choices=FILTER_CHOICES)
    # dst_number
    dst_number = forms.CharField(required=False, label=_('Dst Number'))
    dst_number_not = forms.BooleanField(required=False, label=_('not'))
    dst_number_option = forms.ChoiceField(required=False, choices=FILTER_CHOICES)
    # dispatcher_number
    dispatcher_number = forms.CharField(required=False, label=_('Dispatcher Number'))
    dispatcher_number_not = forms.BooleanField(required=False, label=_('not'))
    dispatcher_number_option = forms.ChoiceField(required=False, choices=FILTER_CHOICES)

    CALL_STATUS_LIST = (
        ('INVALID_NUMBER_FORMAT', _('INVALID_NUMBER_FORMAT',)),
        ('NORMAL_CLEARING', _('NORMAL_CLEARING',)),
        ('CALL_REJECTED', _('CALL_REJECTED',)),
        ('USER_BUSY', _('USER_BUSY',)),
        ('NO_ANSWER', _('NO_ANSWER',)),)
    call_state = forms.MultipleChoiceField(required=False, choices=CALL_STATUS_LIST, label=_('Call state'),
                                           widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(AsteriskForm, self).__init__(*args, **kwargs)

        self.fields['datetime'].widget.attrs['class'] = 'form-control'
        self.fields['datetime'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss'

        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['placeholder'] = 'HH:mm:ss - HH:mm:ss'

        self.fields['src_number'].widget.attrs['class'] = 'form-control'
        self.fields['src_number_option'].widget.attrs['class'] = 'btn'

        self.fields['dst_number'].widget.attrs['class'] = 'form-control'
        self.fields['dst_number_option'].widget.attrs['class'] = 'btn'

        self.fields['dispatcher_number'].widget.attrs['class'] = 'form-control'
        self.fields['dispatcher_number_option'].widget.attrs['class'] = 'btn'

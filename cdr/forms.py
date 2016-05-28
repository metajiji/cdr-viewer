from django.utils.translation import ugettext_lazy as _
from django import forms


class DateTimeForm(forms.Form):
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)


class DurationTimeForm(forms.Form):
    start = forms.TimeField(required=False)
    end = forms.TimeField(required=False)


class AsteriskForm(forms.Form):
    rows = forms.IntegerField(max_value=50, min_value=3, required=False, label=_('Rows per page'))
    page = forms.IntegerField(required=False)
    datetime = forms.CharField(required=False, label=_('Date and time range'))
    duration = forms.CharField(required=False, label=_('Duration range'))

    FILTER_CHOICES = (
        ('start', _('Starts with'),),
        ('end', _('Ends with'),),
        ('equal', _('Equal'),),
        ('contains', _('Contains'),),)
    # src_number
    src_number = forms.CharField(required=False, label=_('Source Number'))
    src_number_not = forms.BooleanField(required=False, label=_('not'))
    src_number_option = forms.ChoiceField(required=False, choices=FILTER_CHOICES)
    # dst_number
    dst_number = forms.CharField(required=False, label=_('Destination Number'))
    dst_number_not = forms.BooleanField(required=False, label=_('not'))
    dst_number_option = forms.ChoiceField(required=False, choices=FILTER_CHOICES)

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

        self.datetime_start = None
        self.datetime_end = None

        self.duration_start = None
        self.duration_end = None

        self.fields['datetime'].widget.attrs['class'] = 'form-control'
        self.fields['datetime'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss'

        self.fields['duration'].widget.attrs['class'] = 'form-control'
        self.fields['duration'].widget.attrs['placeholder'] = 'HH:mm:ss - HH:mm:ss'

        self.fields['src_number'].widget.attrs['class'] = 'form-control'
        self.fields['src_number_option'].widget.attrs['class'] = 'btn'

        self.fields['dst_number'].widget.attrs['class'] = 'form-control'
        self.fields['dst_number_option'].widget.attrs['class'] = 'btn'

    def clean(self):
        cleaned_data = super(AsteriskForm, self).clean()

        date_time = cleaned_data.get('datetime', None)
        if date_time is not None and date_time != '':
            date_time = date_time.split()
            if len(date_time) == 5:  # field format: 'YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss'
                datetime_form = DateTimeForm(data={
                    'start': '%s %s' % (date_time[0], date_time[1]),
                    'end': '%s %s' % (date_time[3], date_time[4])
                })
                if datetime_form.is_valid():
                    self.datetime_start = datetime_form.cleaned_data.get('start')
                    self.datetime_end = datetime_form.cleaned_data.get('end')
                else:
                    self.add_error('datetime', _('datetime field is invalid, this field must be in format '
                                                 '"YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss"'))
            else:
                self.add_error('datetime', _('datetime field must be format '
                                             '"YYYY-MM-DD HH:mm:ss - YYYY-MM-DD HH:mm:ss"'))

        duration = cleaned_data.get('duration', None)
        if duration is not None and duration != '':
            duration = duration.split()
            if len(duration) == 3:  # field format: 'HH:mm:ss - HH:mm:ss'
                duration_form = DurationTimeForm(data={
                    'start': duration[0] if duration[0] != '00:00:00' else None,
                    'end': duration[2] if duration[2] != '00:00:00' else None
                })
                if duration_form.is_valid():
                    self.duration_start = duration_form.cleaned_data.get('start')
                    self.duration_end = duration_form.cleaned_data.get('end')
                else:
                    self.add_error('duration', _('duration field is invalid, this field must be format '
                                                 '"HH:mm:ss - HH:mm:ss"'))
            else:
                self.add_error('duration', _('duration field must be in format "HH:mm:ss - HH:mm:ss"'))

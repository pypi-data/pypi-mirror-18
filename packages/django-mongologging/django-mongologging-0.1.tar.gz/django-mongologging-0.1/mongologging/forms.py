import datetime

from django import forms

from .connection import LOG_FIELDS

TYPES_CHOICES = (
    ('user', 'user'),
    ('celery', 'celery')
)


class LogFilterForm(forms.Form):
    """
    Form for Logs filtering
    """
    datetime = forms.DateField(
        initial=datetime.date.today(),
        widget=forms.widgets.DateInput(format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
        required=False
    )

    type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=TYPES_CHOICES,
        required=False
    )

    obj_type = forms.CharField(required=False)
    id = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super(LogFilterForm, self).clean()
        cleaned_data = {
            field: cleaned_data[field] for field, value in cleaned_data.items() if field in LOG_FIELDS and value}
        if 'datetime' in cleaned_data:
            start = datetime.datetime.combine(cleaned_data['datetime'],
                                              datetime.datetime.min.time())
            end = start + datetime.timedelta(days=1)
            cleaned_data['datetime'] = {'$gte': start, '$lt': end}
        if 'id' in cleaned_data:
            cleaned_data['id'] = int(cleaned_data['id'])
        if 'type' in cleaned_data:
            cleaned_data.update(
                {'$or': [{'type': caller_type} for caller_type in cleaned_data.pop('type', None)]}
            )
        return cleaned_data

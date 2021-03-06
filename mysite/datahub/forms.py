# -*- coding: utf-8 -*-
from django import forms

from .models import Folder, Document


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        exclude = ('date_created', 'date_updated', 'owner')


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ('date_created', 'date_updated', 'owner')

##class DocumentForm(forms.Form):
#    docfile = forms.FileField(
#        label='Select a file',
#        help_text='max. 42 megabytes'
#    )

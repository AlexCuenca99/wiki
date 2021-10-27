from django import forms

class AddEntry(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Enter content', 'id': 'new-entry'}))

class EditEntry(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'id': 'edit-entry-title'}))
    content  = forms.CharField(label="", widget=forms.Textarea(attrs={'id': 'edit-entry'}))
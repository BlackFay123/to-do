from django import forms

class AddTaskForm(forms.Form):
    name = forms.CharField(label="Name:")
    description = forms.CharField(label="Description:")
    priority = forms.CharField(
        label="Priority:",
        widget=forms.TextInput(attrs={"placeholder": "Low, medium, high"}),
    )

class RemoveTaskForm(forms.Form):
    name = forms.CharField(label="Name:")

class EditTaskForm(forms.Form):
    id = forms.IntegerField(label="Task Number:", min_value=1)
    name = forms.CharField(label="Name:")
    description = forms.CharField(label="Description:")
    priority = forms.CharField(
        label="Priority:",
        widget=forms.TextInput(attrs={"placeholder": "Low, medium, high"}),
    )
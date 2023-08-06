#!/usr/bin/env python
# crate_anon/crateweb/userprofile/forms.py

from django.forms import ModelForm
from crate_anon.crateweb.userprofile.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['per_page', 'line_length', 'collapse_at_len',
                  'collapse_at_n_lines']

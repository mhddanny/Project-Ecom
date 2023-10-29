from django import forms
from . models import Account, UserProfile, Address, Province, City, District

class RegisterForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         "class": "form-control",
    #         "placeholder": "First Name",
    #         }
    #     ))
    # last_name = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'class' :'form-control',
    #         'placeholder': 'Last Name',
    #     }
    # ))
    # email = forms.EmailField(widget=forms.EmailInput(
    #     attrs={
    #         'class' :'form-control',
    #         'placeholder': 'Enter Password',
    #         "unique":True,
    #     }
    # ))
    # phone_number = forms.CharField(widget=forms.NumberInput(
    #     attrs={
    #         'class' :'form-control',
    #         'placeholder': 'Phone Number',
    #     }
    # ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class' :'form-control',
            'placeholder': 'Enter Password'
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class' :'form-control',
            'placeholder': 'Confirm Password'
        }
    ))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match.!"
            )

    def __init__(self, *args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={ 'invalid':("Image files only") }, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = [ 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture', 'postcode' ]
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserAddressForm(forms.ModelForm):
    # province = forms.ModelChoiceField(queryset=Province.objects.all(), empty_label="--Provice--")
    # city = forms.ModelChoiceField(queryset=city.objects.all(), empty_label="--Null--")
    # district = forms.ModelChoiceField(queryset=district.objects.all(), empty_label="--Null--")
    
    

    class Meta:
        model = Address
        fields = ['name', 'phone', 'address_line_1', 'address_line_2', 'district']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": "Name",}
        )

        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": "Phone", "text": "number"}
        )

        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": "Address Line 1"}
        )

        self.fields["address_line_2"].widget.attrs.update(
            {"class": "form-control mb-2", "placeholder": "Address Line 1"}
        )

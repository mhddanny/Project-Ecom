from django import forms

from accounts.models import Account, UserProfile
from category.models import Category
from store.models import Product, ProductPaket, ProductGallery, Variation

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

class UserCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class UserProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UserProductPaketForm(forms.ModelForm):
    class Meta:
        model = ProductPaket
        fields = '__all__'

class UserProductGaleryForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = '__all__'

class UserProductVariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'


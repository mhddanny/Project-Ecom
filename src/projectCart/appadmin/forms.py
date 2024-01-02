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
    # is_available = forms.BooleanField(
    #     required=True,
    #     disabled = False,
    #     widget=forms.widgets.CheckboxInput( 
    #         attrs={'class': 'checkbox-inline'}  
    #         ), 
    #     help_text = "I accept the terms in the License Agreement", 
    #     error_messages ={'required':'Please check the box'} 
    # )
    # images = forms.ImageField(required=False, error_messages={ 'invalid':("Image files only") }, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ('product_name', 'description', 'long_description', 'price', 'images', 'stock', 'category',)

    def __init__(self, *args, **kwargs):
        super(UserProductForm,self).__init__(*args, **kwargs)
        self.fields["product_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Name", "required": "True" }
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Short Description", "required": "True", "rows":"2","cols":"50" }
        )
        # self.fields['is_available'].widget = forms. CheckboxInput(initial=True)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProductPaketForm(forms.ModelForm):

    class Meta:
        model = ProductPaket
        fields = ('weight', 'length', 'width', 'height',)

    def __init__(self, *args, **kwargs):
        super(UserProductPaketForm,self).__init__(*args, **kwargs)
        self.fields["weight"].widget.attrs.update(
            {"class": "form-control", "placeholder": "...gram", "required": "True" }
        )
        self.fields["length"].widget.attrs.update(
            {"class": "form-control", "placeholder": "...cm", "required": "True" }
        )
        self.fields["width"].widget.attrs.update(
            {"class": "form-control", "placeholder": "...cm", "required": "True" }
        )
        self.fields["height"].widget.attrs.update(
            {"class": "form-control", "placeholder": "...cm", "required": "True" }
        )


class UserProductGaleryForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = '__all__'

class UserProductVariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'


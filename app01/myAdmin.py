from my_admin.service.sites import ModelMyAdmin,site
from app01.models import Author,AuthorDetail,Book,Publish
from django import forms


site.register(Author)
site.register(AuthorDetail)


class BookModelForm(forms.ModelForm):
    class Meta:
        errors = {
            "required":"该字段不能为空！",
        }
        model = Book
        fields = '__all__'
        error_messages = {
            "title": errors,
            "price": errors,
        }


class BookConfig(ModelMyAdmin):
    model_form_class = BookModelForm
    list_display = ["title","price","publish","authors"]
    list_display_links = ["title","price"]
    search_fields = ["title","price"]

    def patch_init(self,queryset):
        queryset.update(price = 0)
    patch_init.short_description = "批量初始化"
    actions = [patch_init]


site.register(Book,BookConfig)


class PublishConfig(ModelMyAdmin):
    list_display = ["name","city","email"]


site.register(Publish,PublishConfig)



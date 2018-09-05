from my_admin.service.sites import ModelMyAdmin,site
from app01.models import Author,AuthorDetail,Book,Publish
from django import forms
from django.utils.safestring import mark_safe
from django.conf.urls import url
from app01 import views


class AuthorConfig(ModelMyAdmin):
    # 自定制函数列--> 需求：将性别一列设置成下拉菜单，可供用户选择内容并将内容更新到数据库中
    def display_gender(self,data_obj = None,is_header = False):
        if is_header:
            return "性别"
        else:
            html = '<select class="gender" pk="{}">'.format(data_obj.pk)
            for item in Author.gender_choices:
                if data_obj.gender == item[0]:
                    option = '<option selected value="{}">{}</option>'.format(item[0],item[1])
                else:
                    option = '<option value="{}">{}</option>'.format(item[0],item[1])
                html += option
            html += '</select>'
            return mark_safe(html)
    list_display = ["name","age",display_gender]

    # 子类重写extra_url方法--> 需求：单独给Author表中添加一个新的url
    def extra_url(self):
        res = []
        add_url = url(r'^(\d+)/change_gender/$',views.change_gender)
        res.append(add_url)
        return res


site.register(Author,AuthorConfig)

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
    list_display = ["title","price","authors","publish"]
    list_display_links = ["title","price"]
    search_fields = ["title","price"]
    list_filter = ["publish","authors"]

    def patch_init(self,queryset):
        queryset.update(price = 0)
    patch_init.short_description = "批量初始化"
    actions = [patch_init]


site.register(Book,BookConfig)


class PublishConfig(ModelMyAdmin):
    list_display = ["name","city","email"]


site.register(Publish,PublishConfig)



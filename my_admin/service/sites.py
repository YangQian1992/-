from django.conf.urls import url
from django.shortcuts import render,HttpResponse
from django.db.models.fields.related import ManyToManyField
from django.utils.safestring import mark_safe
from django.urls import reverse


class ModelMyAdmin():

    def __init__(self,model):
        self.model = model

    def delete(self,data_obj = None,is_header = False):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        if is_header:
            return "操作"
        else:
            return mark_safe('<a href="{}">删除</a>'.format(reverse("{}_{}_delete".format(app_label,model_name),args=(data_obj.pk,))))

    def change(self,data_obj = None,is_header = False):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        if is_header:
            return "操作"
        else:
            return mark_safe('<a href="{}">编辑</a>'.format(reverse("{}_{}_change".format(app_label,model_name),args=(data_obj.pk,))))

    list_display = ["__str__",delete,change,]

    def listview(self,request):
        print("self-->",self)   # 当前访问模型表的配置类对象
        print("self.model-->",self.model)   # 当前访问模型表
        print("list_display-->",self.list_display)

        print("反向解析url--》",reverse("app01_book_list"))  # /my_admin/app01/book/
        print("反向解析url--》",reverse("app01_book_change",args=(1,)))  # /my_admin/app01/book/1/change/
        print("反向解析url--》",reverse("app02_food_add"))   # /my_admin/app02/food/add/
        print("反向解析url--》",reverse("app02_food_delete",args=(2,)))  # /my_admin/app02/food/2/delete/

        # 获取当前访问的模型表
        current_model = self.model._meta.model_name

        # 创建数据表格头部分
        header_list = []
        for field_or_func in self.list_display:
            # 判断 field_or_func 是否可以被调用
            if callable(field_or_func):
                add_header = field_or_func(self,is_header = True)
            else:
                # 判断 field_or_func 是否为"__str__"
                if field_or_func == "__str__":
                    # 继承默认配置类，就默认展示当前访问模型表的表名
                    add_header = self.model._meta.model_name.upper()
                else:
                    # 自定制配置类，就获取字段对象
                    field_obj = self.model._meta.get_field(field_or_func)
                    add_header = field_obj.verbose_name
            header_list.append(add_header)

        # 创建数据表格体部分
        data_list = self.model.objects.all()
        new_data_list = []
        for data_obj in data_list:
            inner_data_list = []
            for field_or_func in self.list_display:
                # 判断 field_or_func 是否可以被调用
                if callable(field_or_func):
                    field_value = field_or_func(self,data_obj)
                else:
                    # 针对继承默认配置类的模型表的list_display的值是"__str__".进行异常处理
                    try:
                        # 判断field_or_func 所对应的字段对象的类型是否为ManyToManyField
                        field_obj = self.model._meta.get_field(field_or_func)
                        if isinstance(field_obj,ManyToManyField):
                            # 多对多关系的字段需要调用all()
                            rel_obj_list = getattr(data_obj,field_or_func).all()
                            rel_data_list = [str(item) for item in rel_obj_list]
                            field_value = ",".join(rel_data_list)
                        else:
                            # 除了多对多关系以外的字段都可以直接添加，无需调用all()
                            field_value = getattr(data_obj,field_or_func)
                    except Exception as e:
                        # field_or_func 为"__str__"
                        field_value = getattr(data_obj, field_or_func)
                inner_data_list.append(field_value)
            new_data_list.append(inner_data_list)

        return render(request,"listview.html",{
                    "new_data_list":new_data_list,
                    "header_list":header_list,
                    "current_model":current_model,
                    })

    def addview(self,request):
        return HttpResponse("addview……")

    def changeview(self,request,id):
        return HttpResponse("changeview……")

    def deleteview(self,request,id):
        return HttpResponse("deleteview……")

    def get_urls_02(self):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        res = [
            url(r'^$',self.listview,name="{}_{}_list".format(app_label,model_name)),
            url(r'^add/$',self.addview,name="{}_{}_add".format(app_label,model_name)),
            url(r'^(\d+)/change/$',self.changeview,name="{}_{}_change".format(app_label,model_name)),
            url(r'^(\d+)/delete/$',self.deleteview,name="{}_{}_delete".format(app_label,model_name)),
        ]
        return res

    @property
    def urls(self):
        return self.get_urls_02(),None,None


class MyAdminSite():
    def __init__(self):
        self._registry = {}

    def register(self,model,my_admin_class = None):
        if not my_admin_class:
            my_admin_class = ModelMyAdmin
        self._registry[model] = my_admin_class(model)

    def get_urls_01(self):
        res = []
        for model,config_obj in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            add_url = url(r'^{}/{}/'.format(app_label,model_name),config_obj.urls)
            res.append(add_url)
        return res

    @property
    def urls(self):
        return self.get_urls_01(),None,None

site = MyAdminSite()
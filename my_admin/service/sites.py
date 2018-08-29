from django.conf.urls import url
from django.shortcuts import render,HttpResponse


class ModelMyAdmin():

    list_display = []

    def __init__(self,model):
        self.model = model

    def listview(self,request):
        print("self-->",self)   # 当前访问模型表的配置类对象
        print("self.model-->",self.model)   # 当前访问模型表

        print("list_display-->",self.list_display)
        data = self.model.objects.all()
        return render(request,"listview.html",{"data_list":data})

    def addview(self,request):
        return HttpResponse("addview……")

    def changeview(self,request,id):
        return HttpResponse("changeview……")

    def deleteview(self,request,id):
        return HttpResponse("deleteview……")

    def get_urls_02(self):
        res = [
            url(r'^$',self.listview),
            url(r'^add/$',self.addview),
            url(r'^(\d+)/change/$',self.changeview),
            url(r'^(\d+)/delete/$',self.deleteview),
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
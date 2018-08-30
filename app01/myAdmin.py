from my_admin.service.sites import ModelMyAdmin,site
from app01.models import Author,AuthorDetail,Book,Publish


site.register(Author)
site.register(AuthorDetail)


class BookConfig(ModelMyAdmin):
    list_display = ["title","price","publish","authors"]


site.register(Book,BookConfig)


class PublishConfig(ModelMyAdmin):
    list_display = ["name","city","email"]


site.register(Publish,PublishConfig)



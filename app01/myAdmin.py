from my_admin.service.sites import ModelMyAdmin,site
from app01.models import Author,AuthorDetail,Book,Publish


site.register(Author)
site.register(AuthorDetail)

class BookConfig(ModelMyAdmin):
    list_display = ["title","publish_date","price"]

site.register(Book,BookConfig)
site.register(Publish)



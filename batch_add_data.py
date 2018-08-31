import os


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "自定增删改查的组件.settings")
    import django
    django.setup()
    from app01 import models


    # 批量添加数据
    book_list = []
    for i in range(1,101):
        new_book_obj = models.Book(title="book_{}".format(i))
        book_list.append(new_book_obj)
    models.Book.objects.bulk_create(book_list)


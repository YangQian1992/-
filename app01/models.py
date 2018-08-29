from django.db import models


class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name="作者姓名")
    age = models.IntegerField(verbose_name="作者年龄")

    # 与AuthorDetail建立一对一的关系
    authorDetail = models.OneToOneField(to="AuthorDetail",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者表"
        verbose_name_plural = verbose_name


class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday = models.DateField(verbose_name="作者出生日期")
    telephone = models.BigIntegerField(verbose_name="作者联系方式")
    addr = models.CharField(max_length=64,verbose_name="作者联系地址")

    def __str__(self):
        return self.author.name

    class Meta:
        verbose_name = "作者详情表"
        verbose_name_plural = verbose_name


class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32,verbose_name="书籍名称")
    publish_date = models.DateField(verbose_name="出版日期")
    price = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="价格")

    # 与Publish检录一对多的关系，外键字段建立在多的一方
    publish = models.ForeignKey(to="Publish",to_field="nid",on_delete=models.CASCADE,verbose_name="出版社")
    # 与Author表建立多对多的关系，ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表
    authors = models.ManyToManyField(to='Author',verbose_name="作者")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "书籍表"
        verbose_name_plural = verbose_name


class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,verbose_name="出版社名称")
    city = models.CharField(max_length=32,verbose_name="出版社所在城市")
    email = models.EmailField(verbose_name="出版社邮箱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "出版社表"
        verbose_name_plural = verbose_name





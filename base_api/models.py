from django.db import models


class TestTable(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

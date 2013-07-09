__author__ = 'pborky'

from django.db.models import Model,CharField
from tinymce.models import HTMLField

class SiteResource(Model):
    name = CharField(max_length=100, verbose_name='Name')
    value = HTMLField(verbose_name='Value')
    def __unicode__(self):
        return u'%s' %(self.name,)
    class Meta:
        ordering = ["name"]
        verbose_name = "Site Resource"
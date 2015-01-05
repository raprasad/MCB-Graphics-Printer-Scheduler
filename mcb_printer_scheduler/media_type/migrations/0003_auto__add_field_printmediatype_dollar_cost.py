# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PrintMediaType.dollar_cost'
        db.add_column('media_type_printmediatype', 'dollar_cost',
                      self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=10, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PrintMediaType.dollar_cost'
        db.delete_column('media_type_printmediatype', 'dollar_cost')


    models = {
        'media_type.printmediatype': {
            'Meta': {'ordering': "('sort_order', 'name')", 'object_name': 'PrintMediaType'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dollar_cost': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['media_type']
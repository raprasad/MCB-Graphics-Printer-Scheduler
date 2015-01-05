# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FAQCategory'
        db.create_table('faq_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('faqs', ['FAQCategory'])

        # Adding model 'FrequentlyAskedQuestion'
        db.create_table('faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faqs.FAQCategory'], on_delete=models.PROTECT)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('id_hash', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('faqs', ['FrequentlyAskedQuestion'])


    def backwards(self, orm):
        # Deleting model 'FAQCategory'
        db.delete_table('faq_category')

        # Deleting model 'FrequentlyAskedQuestion'
        db.delete_table('faq')


    models = {
        'faqs.faqcategory': {
            'Meta': {'ordering': "('sort_order', 'name')", 'object_name': 'FAQCategory', 'db_table': "'faq_category'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'faqs.frequentlyaskedquestion': {
            'Meta': {'ordering': "('category', 'sort_order', 'question')", 'object_name': 'FrequentlyAskedQuestion', 'db_table': "'faq'"},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faqs.FAQCategory']", 'on_delete': 'models.PROTECT'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['faqs']
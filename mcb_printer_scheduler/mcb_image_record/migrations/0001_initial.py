# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageRecord'
        db.create_table('mcb_image_record', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendar_event.CalendarEvent'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id_hash', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('main_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('thumb_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mcb_image_record', ['ImageRecord'])


    def backwards(self, orm):
        # Deleting model 'ImageRecord'
        db.delete_table('mcb_image_record')


    models = {
        'calendar_event.calendarevent': {
            'Meta': {'ordering': "('-start_datetime', 'display_name')", 'object_name': 'CalendarEvent', 'db_table': "'cal_event'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'is_timeslot_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendar_event.Status']"}),
            'subclass_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'})
        },
        'calendar_event.status': {
            'Meta': {'ordering': "('sort_order', 'name')", 'object_name': 'Status', 'db_table': "'cal_event_status'"},
            'hex_color': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '99'})
        },
        'mcb_image_record.imagerecord': {
            'Meta': {'ordering': "('name', '-created')", 'object_name': 'ImageRecord', 'db_table': "'mcb_image_record'"},
            'calendar_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendar_event.CalendarEvent']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thumb_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mcb_image_record']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CalendarEvent.status'
        db.add_column('cal_event', 'status',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calendar_event.Status']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CalendarEvent.status'
        db.delete_column('cal_event', 'status_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        'calendar_event.calendarfulldaymessage': {
            'Meta': {'ordering': "('-start_datetime', 'display_name')", 'object_name': 'CalendarFullDayMessage', 'db_table': "'cal_event_day_msg'", '_ormbases': ['calendar_event.CalendarEvent']},
            'calendarevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['calendar_event.CalendarEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'message_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendar_event.CalendarFullDayMessageGroup']"})
        },
        'calendar_event.calendarfulldaymessagegroup': {
            'Meta': {'object_name': 'CalendarFullDayMessageGroup', 'db_table': "'cal_event_msg_group'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'calendar_event.calendarmessage': {
            'Meta': {'ordering': "('-start_datetime', 'display_name')", 'object_name': 'CalendarMessage', 'db_table': "'cal_event_msg'", '_ormbases': ['calendar_event.CalendarEvent']},
            'calendarevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['calendar_event.CalendarEvent']", 'unique': 'True', 'primary_key': 'True'})
        },
        'calendar_event.reservation': {
            'Meta': {'ordering': "('-start_datetime', 'display_name')", 'object_name': 'Reservation', 'db_table': "'cal_event_reservation'", '_ormbases': ['calendar_event.CalendarEvent']},
            'billing_code': ('django.db.models.fields.CharField', [], {'max_length': '39', 'blank': 'True'}),
            'calendarevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['calendar_event.CalendarEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'include_poster_tube': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lab_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'poster_tube_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'print_media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_type.PrintMediaType']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['calendar_user.CalendarUser']"})
        },
        'calendar_event.scheduledbannermessage': {
            'Meta': {'ordering': "('-start_datetime',)", 'object_name': 'ScheduledBannerMessage', 'db_table': "'cal_event_banner_msg'"},
            'banner_message': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'calendar_event.status': {
            'Meta': {'ordering': "('sort_order', 'name')", 'object_name': 'Status', 'db_table': "'cal_event_status'"},
            'hex_color': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '99'})
        },
        'calendar_user.calendaruser': {
            'Meta': {'ordering': "('user__last_name',)", 'object_name': 'CalendarUser'},
            'billing_code': ('django.db.models.fields.CharField', [], {'max_length': '39', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '150', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'is_calendar_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lab_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'media_type.printmediatype': {
            'Meta': {'ordering': "('sort_order', 'name')", 'object_name': 'PrintMediaType'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dollar_cost': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['calendar_event']
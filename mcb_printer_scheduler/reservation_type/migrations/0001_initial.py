# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DayOfWeek'
        db.create_table('res_type_day_of_week', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('day_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('reservation_type', ['DayOfWeek'])

        # Adding model 'ReservationType'
        db.create_table('res_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('day_iso_numbers', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('opening_time', self.gf('django.db.models.fields.TimeField')()),
            ('closing_time', self.gf('django.db.models.fields.TimeField')()),
            ('time_block', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('min_time_advance_notice', self.gf('django.db.models.fields.IntegerField')(default=180)),
            ('scheduling_window_in_days', self.gf('django.db.models.fields.IntegerField')(default=365)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id_hash', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('reservation_type', ['ReservationType'])

        # Adding M2M table for field days_allowed on 'ReservationType'
        m2m_table_name = db.shorten_name('res_type_days_allowed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reservationtype', models.ForeignKey(orm['reservation_type.reservationtype'], null=False)),
            ('dayofweek', models.ForeignKey(orm['reservation_type.dayofweek'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reservationtype_id', 'dayofweek_id'])


    def backwards(self, orm):
        # Deleting model 'DayOfWeek'
        db.delete_table('res_type_day_of_week')

        # Deleting model 'ReservationType'
        db.delete_table('res_type')

        # Removing M2M table for field days_allowed on 'ReservationType'
        db.delete_table(db.shorten_name('res_type_days_allowed'))


    models = {
        'reservation_type.dayofweek': {
            'Meta': {'ordering': "('day_number',)", 'object_name': 'DayOfWeek', 'db_table': "'res_type_day_of_week'"},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'day_number': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'reservation_type.reservationtype': {
            'Meta': {'ordering': "('-is_default', '-is_active')", 'object_name': 'ReservationType', 'db_table': "'res_type'"},
            'closing_time': ('django.db.models.fields.TimeField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'day_iso_numbers': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'days_allowed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reservation_type.DayOfWeek']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'min_time_advance_notice': ('django.db.models.fields.IntegerField', [], {'default': '180'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opening_time': ('django.db.models.fields.TimeField', [], {}),
            'scheduling_window_in_days': ('django.db.models.fields.IntegerField', [], {'default': '365'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'time_block': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        }
    }

    complete_apps = ['reservation_type']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PosterTubeColor'
        db.create_table('poster_tube_postertubecolor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('poster_tube', ['PosterTubeColor'])

        # Adding model 'PosterTubeType'
        db.create_table('poster_tube_postertubetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('poster_tube', ['PosterTubeType'])

        # Adding M2M table for field color_choices on 'PosterTubeType'
        m2m_table_name = db.shorten_name('poster_tube_postertubetype_color_choices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('postertubetype', models.ForeignKey(orm['poster_tube.postertubetype'], null=False)),
            ('postertubecolor', models.ForeignKey(orm['poster_tube.postertubecolor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['postertubetype_id', 'postertubecolor_id'])


    def backwards(self, orm):
        # Deleting model 'PosterTubeColor'
        db.delete_table('poster_tube_postertubecolor')

        # Deleting model 'PosterTubeType'
        db.delete_table('poster_tube_postertubetype')

        # Removing M2M table for field color_choices on 'PosterTubeType'
        db.delete_table(db.shorten_name('poster_tube_postertubetype_color_choices'))


    models = {
        'poster_tube.postertubecolor': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PosterTubeColor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'poster_tube.postertubetype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'PosterTubeType'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'color_choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['poster_tube.PosterTubeColor']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        }
    }

    complete_apps = ['poster_tube']
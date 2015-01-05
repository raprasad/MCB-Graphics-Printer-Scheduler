# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('design_links_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort_field', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('design_links', ['Organization'])

        # Adding model 'DesignLinkBase'
        db.create_table('design_links_designlinkbase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['design_links.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sort_field', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('link_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
        ))
        db.send_create_signal('design_links', ['DesignLinkBase'])

        # Adding model 'DesignLink'
        db.create_table('design_links_designlink', (
            ('designlinkbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['design_links.DesignLinkBase'], unique=True, primary_key=True)),
            ('design_link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('design_links', ['DesignLink'])

        # Adding model 'DesignImage'
        db.create_table('design_links_designimage', (
            ('designlinkbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['design_links.DesignLinkBase'], unique=True, primary_key=True)),
            ('main_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('thumb_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('design_links', ['DesignImage'])

        # Adding model 'DesignImageNonWeb'
        db.create_table('design_links_designimagenonweb', (
            ('designlinkbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['design_links.DesignLinkBase'], unique=True, primary_key=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
        ))
        db.send_create_signal('design_links', ['DesignImageNonWeb'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('design_links_organization')

        # Deleting model 'DesignLinkBase'
        db.delete_table('design_links_designlinkbase')

        # Deleting model 'DesignLink'
        db.delete_table('design_links_designlink')

        # Deleting model 'DesignImage'
        db.delete_table('design_links_designimage')

        # Deleting model 'DesignImageNonWeb'
        db.delete_table('design_links_designimagenonweb')


    models = {
        'design_links.designimage': {
            'Meta': {'ordering': "('organization', 'sort_field', 'name')", 'object_name': 'DesignImage', '_ormbases': ['design_links.DesignLinkBase']},
            'designlinkbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['design_links.DesignLinkBase']", 'unique': 'True', 'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'thumb_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'design_links.designimagenonweb': {
            'Meta': {'ordering': "('organization', 'sort_field', 'name')", 'object_name': 'DesignImageNonWeb', '_ormbases': ['design_links.DesignLinkBase']},
            'designlinkbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['design_links.DesignLinkBase']", 'unique': 'True', 'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'})
        },
        'design_links.designlink': {
            'Meta': {'ordering': "('organization', 'sort_field', 'name')", 'object_name': 'DesignLink', '_ormbases': ['design_links.DesignLinkBase']},
            'design_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'designlinkbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['design_links.DesignLinkBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'design_links.designlinkbase': {
            'Meta': {'ordering': "('organization', 'sort_field', 'name')", 'object_name': 'DesignLinkBase'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['design_links.Organization']"}),
            'sort_field': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'design_links.organization': {
            'Meta': {'ordering': "('sort_field', 'abbreviation')", 'object_name': 'Organization'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'sort_field': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['design_links']
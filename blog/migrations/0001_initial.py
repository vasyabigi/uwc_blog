# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('blog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('blog', ['Category'])

        # Adding model 'Post'
        db.create_table('blog_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Post'])

        # Adding M2M table for field categories on 'Post'
        db.create_table('blog_post_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['blog.post'], null=False)),
            ('category', models.ForeignKey(orm['blog.category'], null=False))
        ))
        db.create_unique('blog_post_categories', ['post_id', 'category_id'])

    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('blog_category')

        # Deleting model 'Post'
        db.delete_table('blog_post')

        # Removing M2M table for field categories on 'Post'
        db.delete_table('blog_post_categories')

    models = {
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'blog.post': {
            'Meta': {'ordering': "('-publish',)", 'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blog']
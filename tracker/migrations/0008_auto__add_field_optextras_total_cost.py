# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OptExtras.total_cost'
        db.add_column(u'tracker_optextras', 'total_cost',
                      self.gf('django.db.models.fields.FloatField')(default=1.0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OptExtras.total_cost'
        db.delete_column(u'tracker_optextras', 'total_cost')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tracker.customer': {
            'Meta': {'object_name': 'Customer'},
            'acct': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'}),
            'closedate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'createdate': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'tracker.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'shipset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'storage_fees': ('django.db.models.fields.FloatField', [], {'default': '0.05'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'})
        },
        u'tracker.operation': {
            'Meta': {'object_name': 'Operation'},
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Inventory']"}),
            'op_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tracker.optextras': {
            'Meta': {'object_name': 'OptExtras'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Shipment']"}),
            'total_cost': ('django.db.models.fields.FloatField', [], {}),
            'unit_cost': ('django.db.models.fields.FloatField', [], {})
        },
        u'tracker.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labor_time': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'palletized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        }
    }

    complete_apps = ['tracker']
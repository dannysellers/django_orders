# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'tracker_customer', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('acct', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=5, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('createdate', self.gf('django.db.models.fields.DateField')()),
            ('closedate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'tracker', ['Customer'])

        # Adding model 'Inventory'
        db.create_table(u'tracker_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Customer'])),
            ('itemid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('length', self.gf('django.db.models.fields.FloatField')(default=1.0, max_length=5)),
            ('width', self.gf('django.db.models.fields.FloatField')(default=1.0, max_length=5)),
            ('height', self.gf('django.db.models.fields.FloatField')(default=1.0, max_length=5)),
            ('volume', self.gf('django.db.models.fields.FloatField')(default=1.0, max_length=5)),
            ('palletized', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('arrival', self.gf('django.db.models.fields.DateField')()),
            ('departure', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('storage_fees', self.gf('django.db.models.fields.FloatField')(default=0.05)),
        ))
        db.send_create_signal(u'tracker', ['Inventory'])

        # Adding model 'Operation'
        db.create_table(u'tracker_operation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Inventory'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('finish', self.gf('django.db.models.fields.DateTimeField')()),
            ('labor_time', self.gf('django.db.models.fields.IntegerField')()),
            ('op_code', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
        ))
        db.send_create_signal(u'tracker', ['Operation'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'tracker_customer')

        # Deleting model 'Inventory'
        db.delete_table(u'tracker_inventory')

        # Deleting model 'Operation'
        db.delete_table(u'tracker_operation')


    models = {
        u'tracker.customer': {
            'Meta': {'object_name': 'Customer'},
            'acct': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'}),
            'closedate': ('django.db.models.fields.DateField', [], {}),
            'createdate': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'tracker.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'departure': ('django.db.models.fields.DateField', [], {}),
            'height': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'palletized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'storage_fees': ('django.db.models.fields.FloatField', [], {'default': '0.05'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'})
        },
        u'tracker.operation': {
            'Meta': {'object_name': 'Operation'},
            'finish': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Inventory']"}),
            'labor_time': ('django.db.models.fields.IntegerField', [], {}),
            'op_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['tracker']
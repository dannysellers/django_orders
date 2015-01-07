# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Shipment.finish'
        db.delete_column(u'tracker_shipment', 'finish')

        # Deleting field 'Shipment.start'
        db.delete_column(u'tracker_shipment', 'start')

        # Deleting field 'Shipment.item'
        db.delete_column(u'tracker_shipment', 'item_id')

        # Deleting field 'Shipment.user'
        db.delete_column(u'tracker_shipment', 'user_id')

        # Adding field 'Shipment.owner'
        db.add_column(u'tracker_shipment', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=11111, to=orm['tracker.Customer']),
                      keep_default=False)

        # Adding field 'Shipment.shipid'
        db.add_column(u'tracker_shipment', 'shipid',
                      self.gf('django.db.models.fields.IntegerField')(default=1, unique=True),
                      keep_default=False)

        # Adding field 'Shipment.palletized'
        db.add_column(u'tracker_shipment', 'palletized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Shipment.arrival'
        db.add_column(u'tracker_shipment', 'arrival',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Shipment.departure'
        db.add_column(u'tracker_shipment', 'departure',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Shipment.notes'
        db.add_column(u'tracker_shipment', 'notes',
                      self.gf('django.db.models.fields.TextField')(default='notes'),
                      keep_default=False)

        # Adding field 'Shipment.tracking_number'
        db.add_column(u'tracker_shipment', 'tracking_number',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=30),
                      keep_default=False)

        # Adding field 'Operation.notes'
        db.add_column(u'tracker_operation', 'notes',
                      self.gf('django.db.models.fields.TextField')(default='more notes'),
                      keep_default=False)

        # Deleting field 'Inventory.arrival'
        db.delete_column(u'tracker_inventory', 'arrival')

        # Deleting field 'Inventory.departure'
        db.delete_column(u'tracker_inventory', 'departure')

        # Deleting field 'Inventory.owner'
        db.delete_column(u'tracker_inventory', 'owner_id')

        # Deleting field 'Inventory.palletized'
        db.delete_column(u'tracker_inventory', 'palletized')

        # Deleting field 'Inventory.quantity'
        db.delete_column(u'tracker_inventory', 'quantity')

        # Adding field 'Inventory.shipset'
        db.add_column(u'tracker_inventory', 'shipset',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['tracker.Shipment']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Shipment.finish'
        db.add_column(u'tracker_shipment', 'finish',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Shipment.start'
        db.add_column(u'tracker_shipment', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Shipment.item'
        db.add_column(u'tracker_shipment', 'item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['tracker.Inventory']),
                      keep_default=False)

        # Adding field 'Shipment.user'
        db.add_column(u'tracker_shipment', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Shipment.owner'
        db.delete_column(u'tracker_shipment', 'owner_id')

        # Deleting field 'Shipment.shipid'
        db.delete_column(u'tracker_shipment', 'shipid')

        # Deleting field 'Shipment.palletized'
        db.delete_column(u'tracker_shipment', 'palletized')

        # Deleting field 'Shipment.arrival'
        db.delete_column(u'tracker_shipment', 'arrival')

        # Deleting field 'Shipment.departure'
        db.delete_column(u'tracker_shipment', 'departure')

        # Deleting field 'Shipment.notes'
        db.delete_column(u'tracker_shipment', 'notes')

        # Deleting field 'Shipment.tracking_number'
        db.delete_column(u'tracker_shipment', 'tracking_number')

        # Deleting field 'Operation.notes'
        db.delete_column(u'tracker_operation', 'notes')

        # Adding field 'Inventory.arrival'
        db.add_column(u'tracker_inventory', 'arrival',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'Inventory.departure'
        db.add_column(u'tracker_inventory', 'departure',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 12, 22, 0, 0)),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Inventory.owner'
        raise RuntimeError("Cannot reverse this migration. 'Inventory.owner' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Inventory.owner'
        db.add_column(u'tracker_inventory', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Customer']),
                      keep_default=False)

        # Adding field 'Inventory.palletized'
        db.add_column(u'tracker_inventory', 'palletized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Inventory.quantity'
        db.add_column(u'tracker_inventory', 'quantity',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Inventory.shipset'
        db.delete_column(u'tracker_inventory', 'shipset_id')


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
            'closedate': ('django.db.models.fields.DateField', [], {}),
            'createdate': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'tracker.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'height': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
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
            'notes': ('django.db.models.fields.TextField', [], {}),
            'op_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tracker.optextras': {
            'Meta': {'object_name': 'OptExtras'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Shipment']"}),
            'unit_cost': ('django.db.models.fields.FloatField', [], {})
        },
        u'tracker.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'arrival': ('django.db.models.fields.DateTimeField', [], {}),
            'departure': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labor_time': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'palletized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['tracker']
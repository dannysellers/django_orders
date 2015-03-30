# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WorkOrderAuditLogEntry'
        db.create_table(u'tracker_workorderauditlogentry', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_by', self.gf('audit_log.models.fields.CreatingUserField')(related_name=u'_auditlog_created_tracker_workorder_set', to=orm['auth.User'])),
            ('created_with_session_key', self.gf('audit_log.models.fields.CreatingSessionKeyField')(max_length=40, null=True)),
            ('modified_by', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_auditlog_modified_tracker_workorder_set', to=orm['auth.User'])),
            ('modified_with_session_key', self.gf('audit_log.models.fields.LastSessionKeyField')(max_length=40, null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Customer'])),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Shipment'])),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=4)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tracking', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gen_inspection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photo_inspection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item_count', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bar_code_labeling', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('custom_boxing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consolidation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('palletizing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('misc_services', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('misc_service_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('status', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('createdate', self.gf('django.db.models.fields.DateField')()),
            ('finishdate', self.gf('django.db.models.fields.DateField')(null=True)),
            (u'action_user', self.gf('audit_log.models.fields.LastUserField')(related_name=u'_workorder_audit_log_entry', to=orm['auth.User'])),
            (u'action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            (u'action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'tracker', ['WorkOrderAuditLogEntry'])

        # Adding model 'WorkOrder'
        db.create_table(u'tracker_workorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('audit_log.models.fields.CreatingUserField')(related_name=u'created_tracker_workorder_set', to=orm['auth.User'])),
            ('created_with_session_key', self.gf('audit_log.models.fields.CreatingSessionKeyField')(max_length=40, null=True)),
            ('modified_by', self.gf('audit_log.models.fields.LastUserField')(related_name=u'modified_tracker_workorder_set', to=orm['auth.User'])),
            ('modified_with_session_key', self.gf('audit_log.models.fields.LastSessionKeyField')(max_length=40, null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Customer'])),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tracker.Shipment'])),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=4)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('tracking', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gen_inspection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photo_inspection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('item_count', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bar_code_labeling', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('custom_boxing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('consolidation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('palletizing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('misc_services', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('misc_service_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('status', self.gf('django.db.models.fields.CharField')(default=0, max_length=1)),
            ('createdate', self.gf('django.db.models.fields.DateField')()),
            ('finishdate', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'tracker', ['WorkOrder'])


    def backwards(self, orm):
        # Deleting model 'WorkOrderAuditLogEntry'
        db.delete_table(u'tracker_workorderauditlogentry')

        # Deleting model 'WorkOrder'
        db.delete_table(u'tracker_workorder')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'tracker.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'created_tracker_inventory_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'modified_tracker_inventory_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory'", 'to': u"orm['tracker.Customer']"}),
            'shipset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory'", 'to': u"orm['tracker.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'storage_fees': ('django.db.models.fields.FloatField', [], {'default': '0.1'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'})
        },
        u'tracker.inventoryauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'InventoryAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_inventory_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'_auditlog_created_tracker_inventory_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_auditlog_modified_tracker_inventory_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_auditlog_inventory'", 'to': u"orm['tracker.Customer']"}),
            'shipset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_auditlog_inventory'", 'to': u"orm['tracker.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'storage_fees': ('django.db.models.fields.FloatField', [], {'default': '0.1'}),
            'volume': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'}),
            'width': ('django.db.models.fields.FloatField', [], {'default': '1.0', 'max_length': '5'})
        },
        u'tracker.itemoperation': {
            'Meta': {'object_name': 'ItemOperation'},
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'created_tracker_itemoperation_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['tracker.Inventory']"}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'modified_tracker_itemoperation_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'op_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'})
        },
        u'tracker.optextras': {
            'Meta': {'object_name': 'OptExtras'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extras'", 'to': u"orm['tracker.Shipment']"}),
            'total_cost': ('django.db.models.fields.FloatField', [], {}),
            'unit_cost': ('django.db.models.fields.FloatField', [], {})
        },
        u'tracker.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'created_tracker_shipment_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labor_time': ('django.db.models.fields.IntegerField', [], {}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'modified_tracker_shipment_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shipments'", 'to': u"orm['tracker.Customer']"}),
            'palletized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'tracker.shipmentauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'ShipmentAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_shipment_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'arrival': ('django.db.models.fields.DateField', [], {}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'_auditlog_created_tracker_shipment_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'departure': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'labor_time': ('django.db.models.fields.IntegerField', [], {}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_auditlog_modified_tracker_shipment_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'_auditlog_shipments'", 'to': u"orm['tracker.Customer']"}),
            'palletized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shipid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'tracker.shipoperation': {
            'Meta': {'object_name': 'ShipOperation'},
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'created_tracker_shipoperation_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'modified_tracker_shipoperation_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'op_code': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'operations'", 'to': u"orm['tracker.Shipment']"})
        },
        u'tracker.workorder': {
            'Meta': {'object_name': 'WorkOrder'},
            'bar_code_labeling': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consolidation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'created_tracker_workorder_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'createdate': ('django.db.models.fields.DateField', [], {}),
            'custom_boxing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'finishdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'gen_inspection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_count': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'misc_service_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'misc_services': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'modified_tracker_workorder_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'palletizing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo_inspection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '4'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'tracking': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tracker.workorderauditlogentry': {
            'Meta': {'ordering': "(u'-action_date',)", 'object_name': 'WorkOrderAuditLogEntry'},
            u'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_workorder_audit_log_entry'", 'to': u"orm['auth.User']"}),
            'bar_code_labeling': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consolidation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created_by': ('audit_log.models.fields.CreatingUserField', [], {'related_name': "u'_auditlog_created_tracker_workorder_set'", 'to': u"orm['auth.User']"}),
            'created_with_session_key': ('audit_log.models.fields.CreatingSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'createdate': ('django.db.models.fields.DateField', [], {}),
            'custom_boxing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'finishdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'gen_inspection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'item_count': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'misc_service_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'misc_services': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_by': ('audit_log.models.fields.LastUserField', [], {'related_name': "u'_auditlog_modified_tracker_workorder_set'", 'to': u"orm['auth.User']"}),
            'modified_with_session_key': ('audit_log.models.fields.LastSessionKeyField', [], {'max_length': '40', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Customer']"}),
            'palletizing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo_inspection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '4'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tracker.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '1'}),
            'tracking': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['tracker']
from __future__ import division

import mock
import uuid
import math

from django.conf import settings

from zc_common.events.utils import event_payload


class GlobalIndexRebuildTestMixin(object):
    index_rebuild_event_task = None
    resource_index_rebuild_task = None
    model = None
    attributes = []
    resource_type = None
    event_name = None
    serializer = None

    # Optional
    queryset = None
    objects_count = 10
    default_batch_size = 50
    custom_batch_size = 5

    def setUp(self):
        super(GlobalIndexRebuildTestMixin, self).setUp()
        self.create_test_data()
        self._queryset = self.queryset if self.queryset else self.model.objects.all()

    def create_test_data(self):
        raise NotImplementedError("Override this method to create test data")

    @mock.patch('zc_common.events.emit.emit_microservice_event')
    @mock.patch('zc_common.events.emit.save_to_s3file')
    def test_emitting_event_with_default_batch_size__pass(self, mock_save_to_s3file, mock_emit_microservice_event):
        self.resource_index_rebuild_task()

        events_count = int(math.ceil(self.objects_count / self.default_batch_size))
        self.assertEqual(mock_save_to_s3file.call_count, events_count)
        self.assertEqual(mock_emit_microservice_event.call_count, events_count)

    @mock.patch('zc_common.events.emit.emit_microservice_event')
    @mock.patch('zc_common.events.emit.save_to_s3file')
    def test_emitting_event_with_custom_batch_size__pass(self, mock_save_to_s3file, mock_emit_microservice_event):
        self.resource_index_rebuild_task(batch_size=self.custom_batch_size)

        events_count = int(math.ceil(self.objects_count / self.custom_batch_size))
        self.assertEqual(mock_save_to_s3file.call_count, events_count)
        self.assertEqual(mock_emit_microservice_event.call_count, events_count)

    @mock.patch('zc_common.events.emit.emit_microservice_event')
    @mock.patch('zc_common.events.emit.save_to_s3file')
    def test_emitting_event_with_correct_attributes__pass(self, mock_save_to_s3file, mock_emit_microservice_event):
        total_events = int(math.ceil(self.objects_count / self.default_batch_size))
        s3_keys = [str(uuid.uuid4()) for i in xrange(total_events)]
        mock_save_to_s3file.side_effect = s3_keys

        self.resource_index_rebuild_task()

        events_count = 0
        while events_count < total_events:
            start_index = events_count * self.default_batch_size
            end_index = start_index + self.default_batch_size

            data = []

            for instance in self._queryset.order_by('id')[start_index:end_index]:
                instance_data = self.serializer.__func__(instance)

                for attr in self.attributes:
                    msg = 'Attribute {} not found in serialized model instance. data: {}'
                    self.assertTrue(attr in instance_data, msg.format(attr, instance_data))

                data.append(instance_data)

            mock_save_to_s3file.assert_any_call(data, settings.AWS_INDEXER_BUCKET_NAME)

            s3_key = s3_keys[events_count]
            payload = event_payload(self.resource_type, None, None, {'s3_key': s3_key})
            mock_emit_microservice_event.assert_any_call(self.event_name, **payload)
            events_count += 1

    @mock.patch('zc_common.events.emit.emit_microservice_event')
    @mock.patch('zc_common.events.emit.save_to_s3file')
    def test_filtering_data_works__pass(self, mock_save_to_s3file, mock_emit_microservice_event):
        # If both model and queryset are defined, this test ensures filters applied on the queryset returns less
        # objects than using model.objects.all()
        if self.queryset and self.model:
            msg = 'Both queryset and model.objects.all() returns same objects count. ' \
                  'Make sure processed objects differ when using both querysets. ' \
                  'Otherwise, set queryset to None.'
            self.assertTrue(self.queryset.count() < self.model.objects.count(), msg)

    @mock.patch('zc_common.events.emit.emit_microservice_event')
    @mock.patch('zc_common.events.emit.save_to_s3file')
    def test_event_not_emitted_from_received_index_rebuild_event_with_different_resource_type__pass(
            self, mock_save_to_s3file, mock_emit_microservice_event):

        self.index_rebuild_event_task(resource_type='Some Other Undefined Resource Type',
                                      meta={'batch_size': self.custom_batch_size})

        mock_save_to_s3file.assert_not_called()
        mock_emit_microservice_event.assert_not_called()

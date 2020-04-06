from unittest.mock import patch

from celery import Celery

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from ..tasks import (    
    run_contracts_sync,
    send_contract_notifications,
    update_contracts_esi,
    update_contracts_pricing,
    update_location,
    update_locations
)
from .testdata import create_contract_handler_w_contracts
from ..utils import set_test_logger, NoSocketsTestCase


MODULE_PATH = 'freight.tasks'
logger = set_test_logger(MODULE_PATH, __file__)
app = Celery('myauth')


def get_invalid_user_pk() -> int:
    return max(User.objects.values_list('pk', flat=True)) + 1


@patch(MODULE_PATH + '.ContractHandler.update_contracts_esi')
class TestUpdateContractsEsi(NoSocketsTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.handler, cls.user = create_contract_handler_w_contracts()

    def test_exception_when_no_contract_handler(
        self, mock_update_contracts_esi
    ):
        self.handler.delete()
        with self.assertRaises(ObjectDoesNotExist):
            update_contracts_esi()
    
    def test_minimal_run(self, mock_update_contracts_esi):        
        update_contracts_esi()
        self.assertTrue(mock_update_contracts_esi.called)
    
    def test_run_with_user(self, mock_update_contracts_esi):        
        update_contracts_esi(user_pk=self.user.pk)
        self.assertTrue(mock_update_contracts_esi.called)
        args, kwargs = mock_update_contracts_esi.call_args
        self.assertEqual(kwargs['user_pk'], self.user)

    def test_run_with_invalid_user(self, mock_update_contracts_esi):        
        update_contracts_esi(user_pk=get_invalid_user_pk())
        self.assertTrue(mock_update_contracts_esi.called)
        args, kwargs = mock_update_contracts_esi.call_args
        self.assertIsNone(kwargs['user_pk'])


@patch(MODULE_PATH + '.Contract.objects.send_notifications')
class TestSendContractNotifications(NoSocketsTestCase):
    
    def test_normal_run(self, mock_send_notifications):
        send_contract_notifications()
        self.assertTrue(mock_send_notifications.called)

    def test_exceptions_are_handled(self, mock_send_notifications):
        mock_send_notifications.side_effect = RuntimeError        
        send_contract_notifications()
        self.assertTrue(mock_send_notifications.called)


class TestRunContractsSync(NoSocketsTestCase):
    
    @patch(MODULE_PATH + '.update_contracts_esi')
    @patch(MODULE_PATH + '.send_contract_notifications')
    def test_normal_run(
        self, mock_send_contract_notifications, mock_update_contracts_esi
    ):
        app.conf.task_always_eager = True
        run_contracts_sync()
        app.conf.task_always_eager = False
        self.assertTrue(mock_update_contracts_esi.si.called)
        self.assertTrue(mock_send_contract_notifications.si.called)


@patch(MODULE_PATH + '.Contract.objects.update_pricing')
class TestUpdateContractsPricing(NoSocketsTestCase):
    
    def test_normal_run(self, mock_update_pricing):
        update_contracts_pricing()
        self.assertTrue(mock_update_pricing.called)

    def test_exceptions_are_handled(self, mock_update_pricing):
        mock_update_pricing.side_effect = RuntimeError        
        update_contracts_pricing()
        self.assertTrue(mock_update_pricing.called)


@patch(MODULE_PATH + '.ContractHandler.esi_client')
@patch(MODULE_PATH + '.Location.objects.update_or_create_from_esi')    
class TestUpdateLocation(NoSocketsTestCase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_contract_handler_w_contracts()
    
    def test_normal_run(self, mock_update_or_create_from_esi, mock_esi_client):
        update_location(1022167642188)
        self.assertTrue(mock_esi_client.called)
        self.assertTrue(mock_update_or_create_from_esi.called)

    def test_exceptions_are_handled(
        self, mock_update_or_create_from_esi, mock_esi_client
    ):
        update_location(99)
        self.assertFalse(mock_esi_client.called)
        self.assertFalse(mock_update_or_create_from_esi.called)

    def test_update_locations(
        self, mock_update_or_create_from_esi, mock_esi_client
    ):
        app.conf.task_always_eager = True
        update_locations([1022167642188, 60003760])
        app.conf.task_always_eager = False
        self.assertEqual(mock_update_or_create_from_esi.call_count, 2)
        call_args_1, call_args_2 = mock_update_or_create_from_esi.call_args_list
        _, kwargs_1 = call_args_1
        _, kwargs_2 = call_args_2
        self.assertEqual(kwargs_1['location_id'], 1022167642188)
        self.assertEqual(kwargs_2['location_id'], 60003760)

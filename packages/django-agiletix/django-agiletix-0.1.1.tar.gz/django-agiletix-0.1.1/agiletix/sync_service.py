
import logging
logger = logging.getLogger('agiletix')

import json

from agiletixapi import AgileSalesAPI
from agiletixapi.models import Event

from agiletix.settings import AGILE_SETTINGS as SETTINGS


class AgileSyncManager(object):

    def sync_recieved_events(self, agile_events):
        pass


class AgileSyncService(object):

    def __init__(self):
        self._registry = []

    def register_sync_manager(self, manager):
        self._registry.append(manager())

    def sync_events(self, start_date, end_date):

        api = AgileSalesAPI(
            base_url=SETTINGS['AGILE_BASE_URL'],
            app_key=SETTINGS['AGILE_APP_KEY'],
            user_key=SETTINGS['AGILE_USER_KEY'],
            corp_org_id=SETTINGS['AGILE_CORP_ORG_ID']
        )
        response = api.event_list(start_date=start_date, end_date=end_date)

        if not response.success:
            logger.error("Unable to import: event list call failed: {0}".format(response.error.message))
            return False

        agile_events = [Event(n) for n in response.data]

        for sync_manager in self._registry:
            sync_manager.sync_recieved_events(agile_events)



sync_service = AgileSyncService()


def register(manager):
    sync_service.register_sync_manager(manager)


def sync_events(start_date, end_date):
    sync_service.sync_events(start_date, end_date)


def update_event(event_org_id, event_id, data):
    sync_service.update_event(event_org_id, event_id, data)


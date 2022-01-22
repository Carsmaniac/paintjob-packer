from datetime import date, datetime
from dateutil.tz import tzutc
import json
from requests.auth import HTTPBasicAuth
from requests import sessions

from rudder_analytics.version import VERSION
from rudder_analytics.utils import remove_trailing_slash

_session = sessions.Session()


def post(write_key, host=None, timeout=15, **kwargs):
    """Post the `kwargs` to the API"""
    body = kwargs
    body["sentAt"] = datetime.utcnow().replace(tzinfo=tzutc()).isoformat()
    url = remove_trailing_slash(host or 'https://hosted.rudderlabs.com') + '/v1/batch'
    auth = HTTPBasicAuth(write_key, '')
    data = json.dumps(body, cls=DatetimeSerializer)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'rudderstack-python/' + VERSION
    }

    res = _session.post(url, data=data, auth=auth,
                        headers=headers, timeout=timeout)

    if res.status_code == 200:
        return res

    try:
        payload = res.json()
        raise APIError(res.status_code, payload['code'], payload['message'])
    except ValueError:
        raise APIError(res.status_code, 'unknown', res.text)


class APIError(Exception):

    def __init__(self, status, code, message):
        self.message = message
        self.status = status
        self.code = code

    def __str__(self):
        msg = "[Rudder] {0}: {1} ({2})"
        return msg.format(self.code, self.message, self.status)


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)

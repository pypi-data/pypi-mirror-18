import datetime
from logging import warning

import requests

from leanplum import messages


class Leanplum:
    """Access the Leanplum API. https://www.leanplum.com"""
    BASE_URL = 'https://www.leanplum.com/api'
    user_id = None
    device_id = None
    api_version = '1.0.6'

    _simple_url_template = '{base_url}?appId={app_id}&clientKey={client_key}&apiVersion={api_version}'

    def __init__(self, app_id, client_key, api_version=None, dev_mode=False):
        """Add your appId and clientKey. If you are using development key, set dev_mode=True.
        :param app_id: Your Leanplum appId.
        :param client_key: Your Leanplum clientKey (production or development).
        :param api_version: Leanplum API version to use defaults to 1.0.6. Should not need to change.
        :param dev_mode: Set to True to access the development environment. Defaults to False.
        """
        self.app_id = app_id
        self.client_key = client_key
        self.dev_mode = dev_mode
        if api_version is not None:
            self.api_version = api_version

    def set_user_id(self, user_id):
        """Set the current userId
        :param user_id: The userId you use to identify your users in Leanplum.
        """
        self.user_id = user_id

    def set_device_id(self, device_id):
        """Set the current deviceId.
        :param user_id: The deviceId you use to identify devices in Leanplum.
        """
        self.device_id = device_id

    def start(self, arguments=None):
        """Start a session. You must have called `set_user_id` or you must include `userId` in the arguments.
        Additionally, if you set `deviceId` in your arguments, it will be set for the entire session.
        :param arguments: See the Leanplum docs for arguments structure:
            https://www.leanplum.com/dashboard#/<your-id>/help/setup/api.
        :return: The response object.
        """
        if arguments is None:
            arguments = {}
        self._set_session_properties_from_start_arguments(arguments)
        arguments.update({'action': 'start'})
        return self._request(arguments)

    def stop(self):
        """Start a session. You must have called `set_user_id` or you must include `userId` in the arguments.
        :param arguments: See the Leanplum docs for arguments structure:
            https://www.leanplum.com/dashboard#/<your-id>/help/setup/api.
        :return: The response object.
        """
        return self._request({'action': 'stop'})

    def set_user_attributes(self, user_attributes):
        """Call the API with the setUserAttribute action
        https://www.leanplum.com/dashboard#/<your-id>/help/docs/api?section=setUserAttributes
        :return: The unwrapped response object from Leanplum.
        """
        user_attributes.update({'action': 'setUserAttributes'})
        return self._request(user_attributes)

    def track(self, event_name, track_arguments):
        """Call the API with the track action
        https://www.leanplum.com/dashboard#/<your-id>/help/docs/api?section=track
        :return: The response object.
        """
        track_arguments.update({
            'action': 'track',
            'event': event_name,
        })
        return self._request(track_arguments)

    def multi(self, data):
        """Call the  API with the multi action
        https://www.leanplum.com/dashboard#/<your-id>/help/docs/api?section=multi
        :return: The response object.
        """
        if self.device_id is None:
            if self.user_id is None:
                raise Exception(messages.USER_ID_OR_DEVICE_ID_NEEDED)
            self.device_id = self.user_id

        for d in data:
            if self.dev_mode:
                d['devMode'] = True
            if d.get('deviceId') is None:
               d['deviceId'] = self.device_id
            if self.user_id and d.get('userId') is None:
                d['userId'] = self.user_id

        arguments = {'action': 'multi', 'data': data}
        return self._request(arguments)

    def send_message(self, message_id, user_id=None, device_id=None, values=None, force=False):
        """Send a message to a user or device
        :param message_id: From the Leanplum website, www.leanplum.com/dashboard#/{APP_ID}/messaging/{MESSAGE_ID}
        :param user_id: Use either user_id or device_id to target the message. If user_id is set, device_id is ignored.
        :param device_id: Use either user_id or device_id to target the message
        :return: The unwrapped response.
        """
        assert user_id is not None or device_id is not None, messages.USER_ID_OR_DEVICE_ID_NEEDED
        arguments = {
            'action': 'sendMessage',
            'messageId': message_id,
            'force': force
        }
        if user_id:
            arguments['userId'] = user_id
        elif device_id:
            arguments['device_id'] = device_id
        if values:
            arguments['values'] = values
        return self._request(arguments)

    def _request(self, request_body):
        """POST a request to the Leanplum Api.
        :param request_body: Request body as a dict.
        :return: The parsed JSON response.
        """
        response = requests.post(
            self._get_url(),
            json=self._get_combined_arguments(request_body),
            headers=self._get_headers()
        )

        try:
            return response.json()['response'][0]
        except [AttributeError, KeyError]:
            return response.json()

    def _get_url(self):
        """Create the request URL based on the current values of the class.
        :return: The request URL.
        """
        url_params = {
            'base_url': self.BASE_URL,
            'app_id': self.app_id,
            'client_key': self.client_key,
            'api_version': self.api_version
        }
        return self._simple_url_template.format(**url_params)

    def _get_combined_arguments(self, action_arguments):
        """Combine the action arguments with the default arguments from the class, and the current timestamp
        :return: The combined default and action arguments.
        """
        default_arguments = dict()
        if self.dev_mode:
            default_arguments['devMode'] = True
        if self.user_id is not None:
            default_arguments['userId'] = self.user_id
        if self.device_id is not None:
            default_arguments['deviceId'] = self.device_id
        if action_arguments.get('time') is None:
            default_arguments['time'] = self._get_current_timestamp()
        default_arguments.update(action_arguments)
        return default_arguments

    def _get_headers(self):
        """Get the request headers.
        :return: The request headers as a dict.
        """
        return {'Content-Type': 'application/json'}

    def _set_session_properties_from_start_arguments(self, arguments):
        """Update user_id and device_id, or raise error / warning if not set"""
        new_user_id = arguments.get('userId')
        if new_user_id is not None:
            self.user_id = new_user_id
        elif self.user_id is None:
            raise Exception(messages.USER_ID_NEEDED_IN_ARGS)

        new_device_id = arguments.get('deviceId')
        if new_device_id is not None:
            self.device_id = new_device_id
        elif self.device_id is None:
            warning(messages.UNSET_DEVICE_ID)

    def _get_current_timestamp(self):
        """Return the number of seconds since the Epoch"""
        epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
        return (datetime.datetime.now(tz=datetime.timezone.utc) - epoch).total_seconds()

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import jsonschema
from oslo_log import log as logging
import six
from six.moves.urllib import parse as urlparse

from senlin.api.common import wsgi
from senlin.common import context
from senlin.common import exception as exc
from senlin.common.i18n import _
from senlin.drivers import base as driver_base
from senlin.objects import base as obj_base
from senlin.objects.requests import receivers as vorr
from senlin.rpc import client as rpc

LOG = logging.getLogger(__name__)


class WebhookMiddleware(wsgi.Middleware):
    """Middleware for authenticating webhook triggering requests.

    This middleware authenticates the webhook trigger requests and then
    rebuild the request header so that the request will successfully pass
    the verification of keystone auth_token middleware.
    """
    def process_request(self, req):
        # We only handle POST requests
        if req.method != 'POST':
            return

        # Extract webhook (receiver) ID and params
        results = self._parse_url(req.url)
        if not results:
            return

        (receiver_id, params) = results

        dbctx = context.RequestContext(is_admin=True)
        rpcc = rpc.EngineClient()

        try:
            norm_req = obj_base.SenlinObject.normalize_req(
                'ReceiverGetRequest', {'identity': receiver_id})
            obj = vorr.ReceiverGetRequest.obj_from_primitive(norm_req)
            jsonschema.validate(norm_req, obj.to_json_schema())
        except (ValueError) as ex:
            raise exc.HTTPBadRequest(six.text_type(ex))
        except jsonschema.exceptions.ValidationError as ex:
            raise exc.HTTPBadRequest(six.text_type(ex.message))
        receiver = rpcc.call2(dbctx, 'receiver_get2', obj)

        svc_ctx = context.get_service_context()
        kwargs = {
            'auth_url': svc_ctx['auth_url'],
            'username': svc_ctx['username'],
            'user_domain_name': svc_ctx['user_domain_name'],
            'password': svc_ctx['password']
        }
        kwargs.update(receiver['actor'])

        # Get token and fill it into the request header
        token = self._get_token(**kwargs)
        req.headers['X-Auth-Token'] = token

    def _parse_url(self, url):
        """Extract receiver ID from the request URL.

        Parse a URL of format: http://host:port/webhooks/id/trigger?V=1&k=v
        :param url: The URL from which the request is received.
        """
        parts = urlparse.urlparse(url)
        p = parts.path.split('/')

        # expected: ['', 'v1', 'webhooks', 'webhook-id', 'trigger']
        if len(p) != 5:
            return None

        if any((p[0] != '', p[2] != 'webhooks', p[4] != 'trigger')):
            return None

        qs = urlparse.parse_qs(parts.query)
        if 'V' not in qs:
            return None
        qs.pop('V')
        params = dict((k, v[0]) for k, v in qs.items())
        return p[3], params

    def _get_token(self, **kwargs):
        """Get a valid token based on the credential provided.

        :param cred: Rebuilt credential dictionary for authentication.
        """
        try:
            token = driver_base.SenlinDriver().identity.get_token(**kwargs)
        except Exception as ex:
            LOG.exception(_('Webhook failed authentication: %s.'),
                          six.text_type(ex))
            raise exc.Forbidden()

        return token

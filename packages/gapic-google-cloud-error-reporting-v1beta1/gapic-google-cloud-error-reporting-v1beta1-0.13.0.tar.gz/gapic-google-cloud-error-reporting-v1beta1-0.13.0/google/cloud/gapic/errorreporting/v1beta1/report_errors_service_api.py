# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/devtools/clouderrorreporting/v1beta1/report_errors_service.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.devtools.clouderrorreporting.v1beta1 ReportErrorsService API."""

import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.gapic.errorreporting.v1beta1 import enums
from google.devtools.clouderrorreporting.v1beta1 import report_errors_service_pb2


class ReportErrorsServiceApi(object):
    """An API for reporting error events."""

    SERVICE_ADDRESS = 'clouderrorreporting.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _CODE_GEN_NAME_VERSION = 'gapic/0.1.0'

    _GAX_VERSION = pkg_resources.get_distribution('google-gax').version

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    _PROJECT_PATH_TEMPLATE = path_template.PathTemplate('projects/{project}')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return cls._PROJECT_PATH_TEMPLATE.render({'project': project, })

    @classmethod
    def match_project_from_project_name(cls, project_name):
        """Parses the project from a project resource.

        Args:
          project_name (string): A fully-qualified path representing a project
            resource.

        Returns:
          A string representing the project.
        """
        return cls._PROJECT_PATH_TEMPLATE.match(project_name).get('project')

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 metadata_transformer=None,
                 ssl_creds=None,
                 scopes=None,
                 client_config=None,
                 app_name='gax',
                 app_version=_GAX_VERSION):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.Channel`): A ``Channel`` instance through
            which to make calls.
          ssl_creds (:class:`grpc.ChannelCredentials`): A
            ``ChannelCredentials`` instance for use with an SSL-enabled
            channel.
          client_config (dict):
            A dictionary for call options for each method. See
            :func:`google.gax.construct_settings` for the structure of
            this data. Falls back to the default config if not specified
            or the specified config is missing data points.
          metadata_transformer (Callable[[], list]): A function that creates
             the metadata for requests.
          app_name (string): The codename of the calling service.
          app_version (string): The version of the calling service.

        Returns:
          A ReportErrorsServiceApi object.
        """
        if scopes is None:
            scopes = self._ALL_SCOPES
        if client_config is None:
            client_config = {}
        goog_api_client = '{}/{} {} gax/{} python/{}'.format(
            app_name, app_version, self._CODE_GEN_NAME_VERSION,
            self._GAX_VERSION, platform.python_version())
        metadata = [('x-goog-api-client', goog_api_client)]
        default_client_config = json.loads(
            pkg_resources.resource_string(
                __name__, 'report_errors_service_client_config.json').decode())
        defaults = api_callable.construct_settings(
            'google.devtools.clouderrorreporting.v1beta1.ReportErrorsService',
            default_client_config,
            client_config,
            config.STATUS_CODE_NAMES,
            kwargs={'metadata': metadata})
        self.report_errors_service_stub = config.create_stub(
            report_errors_service_pb2.ReportErrorsServiceStub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            metadata_transformer=metadata_transformer,
            scopes=scopes)

        self._report_error_event = api_callable.create_api_call(
            self.report_errors_service_stub.ReportErrorEvent,
            settings=defaults['report_error_event'])

    # Service calls
    def report_error_event(self, project_name, event, options=None):
        """
        Report an individual error event.
        This endpoint accepts <strong>either</strong> an OAuth token,
        <strong>or</strong> an
        <a href=\"https://support.google.com/cloud/answer/6158862\">API key</a>
        for authentication. To use an API key, append it to the URL as the value of
        a ``key`` parameter. For example:
        <pre>POST https://clouderrorreporting.googleapis.com/v1beta1/projects/example-project/events:report?key=123ABC456</pre>

        Example:
          >>> from google.cloud.gapic.errorreporting.v1beta1 import report_errors_service_api
          >>> from google.devtools.clouderrorreporting.v1beta1 import report_errors_service_pb2
          >>> api = report_errors_service_api.ReportErrorsServiceApi()
          >>> project_name = api.project_path('[PROJECT]')
          >>> event = report_errors_service_pb2.ReportedErrorEvent()
          >>> response = api.report_error_event(project_name, event)

        Args:
          project_name (string): [Required] The resource name of the Google Cloud Platform project. Written
            as ``projects/`` plus the
            `Google Cloud Platform project ID <https://support.google.com/cloud/answer/6158840>`_.
            Example: ``projects/my-project-123``.
          event (:class:`google.devtools.clouderrorreporting.v1beta1.report_errors_service_pb2.ReportedErrorEvent`): [Required] The error event to be reported.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        request = report_errors_service_pb2.ReportErrorEventRequest(
            project_name=project_name, event=event)
        self._report_error_event(request, options)

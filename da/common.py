"""
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function
import argparse
import json
import logging
import os
import random
import sys
import time
import _constants
import auth

import google_auth_httplib2
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient import http
from googleapiclient import model

# Authenticate and return the Content API service
def init(argv, doc):
  """A simple initialization routine for the Content API samples.

  Args:
    argv: list of string, the command-line parameters of the application.
    doc: string, description of the application. Usually set to __doc__.

  Returns:
    A tuple of (service, config), where service is the service object and
    config is the configuration JSON in Python form.
  """
  config = {}
  config_file = os.path.join('content', _constants.CONFIG_FILE)
  config = json.load(open(config_file, 'r'))

  credentials = auth.authorize(config)
  auth_http = google_auth_httplib2.AuthorizedHttp(
    credentials, http=http.set_user_agent(
        http.build_http(), _constants.APPLICATION_NAME))
  service = discovery.build(
    _constants.SERVICE_NAME, _constants.SERVICE_VERSION, http=auth_http)

  # Now that we have a service object, fill in anything missing from the
  # configuration using API calls.
  retrieve_remaining_config_from_api(service, config)

  return (service, config)


def retrieve_remaining_config_from_api(service, config):
  """Retrieves any missing configuration information using API calls.

  This function can fill in the following configuration fields:
  * merchantId

  It will also remove or overwrite existing values for the following fields:
  * isMCA
  * websiteUrl

  Args:
    service: Content API service object
    config: dictionary, Python representation of config JSON.
  """
  authinfo = service.accounts().authinfo().execute()
  account_ids = authinfo.get('accountIdentifiers')
  if not account_ids:
    print('The currently authenticated user does not have access to '
          'any Merchant Center accounts.')
    sys.exit(1)
  if 'merchantId' not in config:
    first_account = account_ids[0]
    config['merchantId'] = int(first_account.get('merchantId', 0))
    if not config['merchantId']:
      config['merchantId'] = int(first_account['aggregatorId'])
    print('Using Merchant Center %d for running samples.' %
          config['merchantId'])
  merchant_id = config['merchantId']
  config['isMCA'] = False
  # The requested Merchant Center can only be an MCA if we are a
  # user of it (and thus have access) and it is listed as an
  # aggregator in authinfo.
  for account_id in authinfo['accountIdentifiers']:
    if ('aggregatorId' in account_id and
        int(account_id['aggregatorId']) == merchant_id):
      config['isMCA'] = True
      break
    if ('merchantId' in account_id and
        int(account_id['merchantId']) == merchant_id):
      break
  if config['isMCA']:
    print('Merchant Center %d is an MCA.' % config['merchantId'])
  else:
    print('Merchant Center %d is not an MCA.' % config['merchantId'])
  account = service.accounts().get(
      merchantId=merchant_id, accountId=merchant_id).execute()
  config['websiteUrl'] = account.get('websiteUrl')
  if not config['websiteUrl']:
    print('No website for Merchant Center %d.' % config['merchantId'])
  else:
    print('Website for Merchant Center %d: %s' % (config['merchantId'],
                                                  config['websiteUrl']))


def is_mca(config):
  """Returns whether or not the configured account is an MCA."""
  return config.get('isMCA', False)


def check_mca(config, should_be_mca, msg=None):
  """Checks that the configured account is an MCA or not based on the argument.

  If not, it exits the program early.

  Args:
    config: dictionary, Python representation of config JSON.
    should_be_mca: boolean, whether or not we expect an MCA.
    msg: string, message to use instead of standard error message if desired.
  """
  if should_be_mca != is_mca(config):
    if msg is not None:
      print(msg)
    else:
      print('For this sample, you must%s use a multi-client account.' %
            '' if should_be_mca else ' not')
    sys.exit(1)
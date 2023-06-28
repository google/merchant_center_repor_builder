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

import pprint
import json
import sys

import google.auth
import google_auth_httplib2
import google.auth.impersonated_credentials
from googleapiclient.discovery import build

from db import connect_with_connector
from sqlalchemy.orm import sessionmaker

import google_auth_httplib2
from models import Disapproval
import _constants
import common


def main(argv):
  
  # Authenticate and construct service.
  service, config, _ = common.init(argv, __doc__)
  merchant_id = config['merchantId']
  EXTRA_SCOPES = ['https://www.googleapis.com/auth/content']
  source_credentials, project_id = google.auth.default(scopes=EXTRA_SCOPES)
  auth_http = google_auth_httplib2.AuthorizedHttp(source_credentials)
  
  service = build(
      _constants.SERVICE_NAME, _constants.SERVICE_VERSION, http=auth_http
  )

  query = f"""
          SELECT
  product_view.id,
  product_view.offer_id,
  product_view.title,
  product_view.brand,
  product_view.currency_code,
  product_view.price_micros,
  product_view.language_code,
  product_view.condition,
  product_view.channel,
  product_view.availability,
  product_view.shipping_label,
  product_view.gtin,
  product_view.item_group_id,
  product_view.creation_time,
  product_view.expiration_date,
  product_view.aggregated_destination_status,
  product_view.item_issues
FROM ProductView
WHERE product_view.aggregated_destination_status = 'NOT_ELIGIBLE_OR_DISAPPROVED'
          """

  req_body = {'query': query}

  # Build request
  request = service.reports().search(merchantId=merchant_id, body=req_body)

  # Send request
  result = request.execute()
  result = result['results']
  batches = []
  batch_id = 0
  for row in result:
    batch_id = batch_id + 1
    batches.append({
        'batchId': batch_id,
        'merchantId': merchant_id,
        'method': 'get',
        'productId': row.get('productView').get('id'),
    })
    
  Session = sessionmaker(bind=connect_with_connector())
  session = Session()
  print('Got Product Ids')
  request = service.productstatuses().custombatch(body={'entries': batches})
  response = request.execute()
  # Check to ensure the result is not an empty object
  if bool(response):
    for row in response.get('entries'):
      product_status = row.get('productStatus')
      title = product_status.get('title')
      issues = product_status.get('itemLevelIssues')
      issue_date = product_status.get('creationDate')
      for issue in issues:
        disapproval = issue.get('description')
        link = issue.get('documentation')
        description = issue.get('detail')
        status = issue.get('servability')
      disapproval = Disapproval(
          name=title,
          description=description,
          status=status,
          merchant_id=merchant_id,
          offer_id=title,
          issue_date=issue_date,
          link=link,
      )
      print(disapproval)
      session.add(disapproval)
    session.commit()
  else:
    print('Your search query returned no results.')

if __name__ == '__main__':
  main(sys.argv)
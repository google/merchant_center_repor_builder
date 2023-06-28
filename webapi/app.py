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

import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests

measurement_id = 'G-xxx'
api_secret = 'xxxx'

product_disapprovals = [
    {
      "name": "Mismatched domain with product URL [ads redirect]",
      "code": "TBX-0023",
      "severity": "critical",
      "productCount": 200,
      "cta": {
        "doc": "https://support.google.com/merchants/answer/160050?hl=en"
      }
    },
    {
      "name": "Duplicate value [gtin]",
      "code": "TBX-0024",
      "severity": "critical",
      "productCount": 213
    },
    {
      "name": "GTIN not related to brand",
      "code": "TBX-0048",
      "productCount": 213,
      "severity": "error"
    },
    {
      "name": "Incorrect identifier [gtin]",
      "code": "TBX-02",
      "severity": "suggestion",
      "productCount": 213,
      "cta": {
        "doc": "https://testurl"
      }
    },
    {
      "name": "Incorrect product identifier [gtin]",
      "code": "TBX-0048",
      "productCount": 213,
      "severity": "error",
      "cta": {
        "doc": "https://testurl"
      }
    },
    {
      "name": "Invalid text value [gtin]",
      "code": "TBX-03",
      "severity": "error",
      "productCount": 213
    },
    {
      "name": "Invalid value [gtin]",
      "code": "TBX-0048",
      "productCount": 213,
      "severity": "suggestion"
    },
    {
      "name": "Same GTIN but differing value [brand]",
      "code": "TBX-0048",
      "productCount": 213,
      "severity": "critical",
      "cta": {
        "doc": "https://testurl"
      }
    },
    {
      "name": "Same GTIN but differing value [item group id]",
      "code": "TBX-0048",
      "productCount": 213,
      "severity": "critical"
    }
  ]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def track(client_id):
  url = f'https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}'
  params = {
      'client_id': client_id,
      'events': [
          { 'name': 'product_disapprovals_viewed' }
      ]
  }
  r = requests.post(url=url, json=params)

########## Endpoints
@app.route('/product-disapprovals')
@cross_origin()
def productDisapprovals():
    # todo: de-hardcode it when payload contains unique merchant id
    client_id = 'ABC.123'
    track(client_id)
    return product_disapprovals

@app.route('/')
@cross_origin()
def test():
    return 'test'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
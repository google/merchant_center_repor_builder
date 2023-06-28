# Copyright 2023 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# must:
gcpproject='notional-cocoa-376011'

# could:
gcpregion='us-central1'
webapiservicename='merchant-center-report-builder-webapi'
uiservicename='merchant-center-report-builder-ui'

# -------------------------------- HOST PRE-REQUISITES:
# gcloud and nodejs

# -------------------------------- START SCRIPT

echo '\n\n\n\n'
echo 'about to log into GCP'
gcloud auth login

echo '\n\n\n\n'
echo 'about to set gcp project'
gcloud config set project $gcpproject

echo '\n\n\n\n'
echo 'about to set gcp region'
gcloud config set run/region $gcpregion

echo '\n\n\n\n'
echo 'about to enable dependencies in gcloud'
gcloud services enable compute.googleapis.com

echo '\n\n\n\n'
echo 'about to deploy the webapi container'
sh webapi/deploy-webapi.sh \
  -p $gcpproject \
  -r $gcpregion \
  -s $webapiservicename

echo '\n\n\n\n'
echo 'about to get url of webapi endpoint created'
export CLOUD_RUN_SERVICE_URL=$(gcloud run services \
  --platform managed \
  describe \
  $webapiservicename \
  --region $gcpregion \
  --format="value(status.url)")

echo '\n\n\n\n'
echo 'about to set url to angular project config'
node setCloudRunWebApiEndpoint.js

echo '\n\n\n\n'
echo 'about to deploy the ui container'
sh ui/deploy-ui.sh \
  -p $gcpproject \
  -r $gcpregion \
  -s $uiservicename
# Data Quality Monitor

**Continuously validate your data with easy, customizable rules**

## Context

Data is the most important part of a modern business strategy. However, it's hard to
maintain the robust foundation necessary for supporting data-driven decisions.

Data Quality Monitor (DQM) aims to empower clients with an easy way to monitor their data.
It runs on Google Cloud Platform (GCP) and can act on any data sitting in BigQuery, including
exports from various Google Ads & Marketing Platform connectors. The checks/rules are
configured with a simple JSON file and managed with scheduled Cloud Workflows. The output are
logs that can be visualized and monitored for subsequent action. We also provide templates
for common use cases.

## Disclaimer

* MC ReporBuilder is fully owned and managed by you, within your GCP project.
* MC ReporBuilder is open-source and free - you only pay for the underlying GCP resource usage.

## [Installation](docs/install.md)

MC ReporBuilder is deployed using the Google Cloud cli.

Required: Simply configure and run the orchestrator.sh file.
Optional: Google Analytics basic tracking can be configured at the top of app.py


### [Configuration](docs/config.md)

DQM is configured with simple JSON files, stored on Google Cloud Storage.

You can read more in the [configuration docs](docs/config.md).

### [Usage](docs/usage.md)

DQM can be automated with [Cloud Scheduler](https://cloud.google.com/scheduler).

It outputs extensive logging, which can be leveraged for notifications or dashboards.

You can read more in the [usage docs](docs/usage.md).

## [Development](docs/devel.md)

We provide DQM as an open-source solution, so you can contribute to or expand on its features.

You can learn more in the [development docs](docs/devel.md).

## License

**This is not an officially supported Google product.**

Copyright 2023 Google LLC. This solution, including any related sample code or data, is made available on an "as is", "as available", and "with all faults" basis, solely for illustrative purposes, and without warranty or representation of any kind. This solution is experimental, unsupported and provided solely for your convenience. Your use of it is subject to your agreements with Google, as applicable, and may constitute a beta feature as defined under those agreements. To the extent that you make any data available to Google in connection with your use of the solution, you represent and warrant that you have all necessary and appropriate rights, consents and permissions to permit Google to use and process that data. By using any portion of this solution, you acknowledge, assume and accept all risks, known and unknown, associated with its usage, including with respect to your deployment of any portion of this solution in your systems, or usage in connection with your business, if at all.
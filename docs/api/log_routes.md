# Log API

## Introduction

Logs are generated when users read blog posts. Because this platform does not have authentication functionality, session cookies are used to track unique page views.

## Get Logs

To access Logs, a `GET` request must be made to the `/_api/read/logs` endpoint. By default, this returns all logs from now till the beginning of the current month (UTC time). So, for example, a GET request to `/_api/read/logs` on October 18 would return logs from October 1-October 18. A request on November 2 would return logs from November 1-November 2.

To filter results, there are optional arguments that you can make. You can combine them to further filter your results.

All results are returned as a JSON list of objects.

### Filter By Content

To filter by Content, use the `?slug=` argument.

For example, a GET request to the `/_api/read/logs?slug=example-article` endpoint would return all logs from the article with the slug `example-article`.

This can be used to monitor content's popularity over time.

### Filter By User

To filter by user, use the `?cookie_uuid=` argument.

For example, a GET request to the `/_api/read/logs?cookie_uuid=61d047b2-c1d9-4bed-b8e9-ab99316fc644` endpoint would return all logs generated by user with cookie_uuid `61d047b2-c1d9-4bed-b8e9-ab99316fc644`.

This can be used to monitor specific users' interests. Taken a step further, it could be used for some sort of recommendation engine.

### Filter By Date

To filter by date, use the `?start_date=` argument. Optionally, you can also use the `?end_date=` argument as well. If an end date is not specified, it will default to the current time. Dates are in UTC time and are expected in the YYYY-MM-DD format.

For example, a GET request to the `/_api/read/logs?start_date=2021-01-01&end_date=2021-02-01` endpoint would return all logs from January 1, 2021 to February 1, 2021. Conversely, a GET request to the `/_api/read/logs?start_date=2021-01-01` would return all logs from January 1, 2021 to now.

This can be used to monitor traffic over time.

### Combining Filters

As previously stated, filters can be combined to further refine your search.

For example:
- `/_api/read/logs?cookie_uuid=61d047b2-c1d9-4bed-b8e9-ab99316fc644&start_date=2021-09-01&end_date=2021-10-01` would give all logs from user 61d047b2-c1d9-4bed-b8e9-ab99316fc644 from September 1, 2021 to October 1, 2021.
- `/_api/read/logs?slug=example-article&start_date=2021-09-01&end_date=2021-10-01` would measure the popularity of the article with slug "example-article" from September 1, 2021 to October 1, 2021.
- `/_api/read/logs?cookie_uuid=61d047b2-c1d9-4bed-b8e9-ab99316fc644&slug=example-article&start_date=2021-09-01&end_date=2021-10-01` would show how often user 61d047b2-c1d9-4bed-b8e9-ab99316fc644 visited article "example-article" from September 1, 2021 to October 1, 2021.
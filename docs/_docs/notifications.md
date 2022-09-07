---
title: Notifying users
excerpt: How to use the notification service, and add a new one
category: Technical detail
---
## Telling participants about their matches

Having conducted a matching exercise, the next step is to let participants on the programme know that they've been matched. We use [GOV.UK Notify](https://www.gov.uk/notify) to notify participants.

The system allows you
to download a zipped folder that contains rows of CSV data. This data is in a format that works with templates we have set up in our GOV.UK Notify. You could use another email service that supports templating or mail merging, if you prefer.

The data is deleted from the system once it's been downloaded, or after a period of time. This period can be set in
seconds using the environment variable `DATA_STORAGE_PERIOD_SECS`. The task is carried out by Celery - see
`app.tasks.tasks.delete_mailing_lists_after_period`.

## Coming soon

In release 2.5.0, users will be able to rely directly on GOV.UK Notify to notify participants of their matches. Keep an eye
on our [roadmap](https://github.com/users/jonodrew/projects/1) for more details.

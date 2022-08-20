---
title: Notifying users
excerpt: How to use the notification service, and add a new one
category: Technical detail
---
## Speaking to the people

Having conducted a matching exercise, the next step is to let folks know they've been matched. The system allows you
to download a zipped folder that contains rows of data that work with our [GOV.UK Notify](gov.uk/notify) templates.
This data is deleted from the system once it's been downloaded, or after a period of time. This period can be set in
seconds using the environment variable `DATA_STORAGE_PERIOD_SECS`. The task is carried out by Celery - see
`app.tasks.tasks.delete_mailing_lists_after_period`.

## Coming soon
In release 2.5.0, users will be able to rely directly on Notify to notify participants of their matches. Keep an eye
on our [roadmap](https://github.com/users/jonodrew/projects/1) for more details.

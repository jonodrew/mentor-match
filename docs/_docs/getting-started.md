---
title: Running locally
excerpt: "How to deploy this software"
category: Getting started
---

This software requires `docker-compose` to run locally. It uses Redis as a backend and queue; Celery to process
long-running tasks, and Flask to run the web application. Docs are served with Jekyll.

By default, the service can be accessed on the following ports:

| service | port |
|---------|------|
| flask   | 5001 |
| redis   | 6379 |
| docs    | 4000 |

## Installing dependencies

You **must** install `docker-compose` to use this software. [Follow the documentation from Docker](https://docs.docker.com/desktop/) to install the required software.

Once you've done
that, you'll need to clone [this repository](https://www.github.com/jonodrew/mentor-match). You don't necessarily
need to sign up to GitHub to do this.

Once you've done that, use the command line to get to where you've cloned this repository. Then run

`docker-compose up`

You should now be able to access the service on the `localhost:` followed by the ports above. I recommend starting
with [the docs](localhost:4000), so you can come back here and keep going!

To stop the service at any time, just press the control (ctrl) key and 'c' together.

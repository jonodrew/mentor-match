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

After `docker-compose` is installed, clone [the mentor match repository](https://www.github.com/cs-mentoring/mentor-match). This repository is hosted on Github, but a Github account is not required to clone the repository.

A Github account is required if you wish to [contribute to the documentation or code](/contribute).

Use the command line to get to where you've cloned this repository.

From the repository folder, in the command line run:

```
docker-compose up
```

You should now be able to access the service on the `localhost:` followed by the ports above. I recommend starting
with [the docs](localhost:4000), so you can come back here and keep going!

To stop the service at any time, just press the control (<kbd>Ctrl</kbd>) key and <kbd>C</kbd> key together.

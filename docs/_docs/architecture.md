---
title: System architecture
excerpt: How everything fits together
category: Technical detail
---

## Meet the cast
There are four key characters in this service. The web server, which responds to requests from users. The queue,
where the web server puts demands for people to be matched. A worker machine, which picks matching tasks off the
queue and processes them. Finally, the results store, where the worker machine drops its completed matches.

While the web server waits for the task, it currently just shows a plain screen. This is definitely a bad user
experience, but I don't yet want to cram more javascript into this system. However, I accept that this probably
means doing something clever with attachments, encryption, emails, and other such things.
[Pull requests are welcome.](https://www.github.com/cs-mentoring/mentor-match)

In the current system, the web server is Flask. The queue and the results store are both played by Redis, and the
worker is Celery. There is
[a fork of this system exploring whether this could be done with AWS](https://github.com/mforner13/mentor-match). There is no doubt it
would be a damn sight more complicated, more difficult to debug, and out of date before long.

Nonetheless, I hope it works, because that is inevitably the way the world is going. And it'll be cheaper to
actually run.

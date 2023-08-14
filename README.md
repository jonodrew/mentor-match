# Mentor Match

This is a service to help mentoring programme administrators match mentors and mentees. Get in touch to find out more, or raise an issue.

It uses [this package](https://github.com/jonodrew/mentor-match-package) to calculate matches. It relies on the Munkres, or Hungarian, algorithm. The Munkres algorithm works on a grid of scores and finds the solution that makes the most people the least unhappy. That is to say, everyone will be equally unhappy with their score: any switch will make *someone* worse off.

## Roadmap

This service is free and open source. It welcomes pull requests, feature suggestions, improvements to grammar, spelling, or any other way folks want to help.

Our roadmap is hosted [here on GitHub](https://github.com/users/jonodrew/projects/1). Make feature suggestions by
raising an issue on this repo.

## Architecture
This service has three main parts: a web server, running Flask; a Celery worker; and a Redis instance. The long-running task of matching mentors and mentees is passed off to the Celery worker via Redis, which acts as the broker. Results are also stored in Redis and retrieved by the Flask app as needed.

The Flask app is very basic: mostly HTML and basic routes, with a smidgeon of javascript to keep the user interested in what's happening while they wait for their results. That needs some work **so pull requests are welcome**.

Docs are served with Jekyll.

## Setup

To use this software your local machine, you will need:
- admin rights, or at least enough rights to install stuff
- Python 3.7+
- `docker-compose`
- `git`
- a file of mentors and mentees. These files should be called "mentees.csv" and "mentors.csv", and align to the template in [the data folder](mentor_match_web/app/static/data/small). 

By default, the service can be accessed on the following ports:

| service | port |
|---------|------|
| flask   | 5001 |
| redis   | 6379 |

## Installing dependencies

You **must** install `docker-compose` to use this software. [Follow the documentation from Docker](https://docs.docker.com/desktop/) to install the required software.

After `docker-compose` is installed, clone [the mentor match repository](https://www.github.com/mentor-matching-online/mentor-match). This repository is hosted on Github, but a Github account is not required to clone the repository. 

Use the command line to get to where you've cloned this repository. 

From the repository folder, in the command line run:

```
docker-compose up
```

You should now be able to access the service on the `localhost:` followed by the ports above.

To stop the service at any time, just press the control (<kbd>Ctrl</kbd>) key and <kbd>C</kbd> key together.

You can use the randomised data in the [sample_data folder](/sample_data) to try out the system and see for yourself how quickly it matches 500 mentors and mentees. The record on my hardware is 97 seconds. I've not yet tried it by hand...

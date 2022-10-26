# Mentor Match

This is a service to help mentoring programme administrators match mentors and mentees. Right now it's specifically designed to support the Civil Service's LBGTQ+ network. It might work if you run a different network in the Civil Service. Get in touch to find out more, or raise an issue.

It uses [this package](https://github.com/jonodrew/mentor-match-package) to calculate matches. It relies on the Munkres, or Hungarian, algorithm. The Munkres algorithm works on a grid of scores and finds the solution that makes the most people the least unhappy. That is to say, everyone will be equally unhappy with their score: any switch will
make *someone* worse off.

## Roadmap

This service is free and open source. It welcomes pull requests, feature suggestions, improvements to grammar,
spelling, or any other way folks want to help.

Our roadmap is hosted [here on GitHub](https://github.com/users/jonodrew/projects/1). Make feature suggestions by
raising an issue on this repo.

## Architecture
This service has three main parts: a web server, running Flask; a Celery worker; and a Redis instance. The long-running task of matching mentors and mentees is passed off to the Celery worker via Redis, which acts as the broker. Results are also stored in Redis and retrieved by the Flask app as needed.

The Flask app is very basic: mostly HTML and basic routes, with a smidgeon of javascript to keep the user interested in what's happening while they wait for their results. That needs some work **so pull requests are welcome**.

## Setup

If you've never done Python before in your life this project might not be for you. On the other hand, I think the code is
beautiful, and I've made an effort with the documentation, and you can [find me on twitter](https://www.twitter.com/jonodrew)
if you need to ask me questions, so what the heck. Let's get stuck in.

You will need:

- Python 3.7+
- admin rights, or at least enough rights to install stuff
- `git`
- a file of mentors and mentees. These files should be called "mentees.csv" and "mentors.csv", and align to the template in [the data folder](mentor_match_web/app/static/data/small)
  - you can add any columns you want, but if you change any of the existing column headings things will go sideways
    quickly. So don't do that

Start by [cloning this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository).
Then [set up a virtual environment](https://docs.python.org/3/library/venv.html), to make sure the things you're about to
install don't mess around with your base system.

On a Mac, run the following commands:

```
python3 -m venv /path/to/new/virtual/environment
source /path-to-new-virtual-environment/bin-activate
```

Now install the requirements for this project: `pip install -r requirements.txt`

This software is best run in Docker, because it needs Redis and a Celery worker. You'll need to install `Docker` and
`docker-compose`. [Docker instructions](https://docs.docker.com/engine/install/) and
[docker-compose instructions](https://docs.docker.com/compose/install/). Once you've got those two installed, you'll need to run `docker-compose up -d` to get things running, and `docker-compose down` to stop them again. You should see the app running at http://127.0.0.1:5001

Once you have the app running in your browser, you will be redirected to `/login`. The credentials for logging in locally are:
  ```
  Username: CSLGBT
  Password: HorseBatteryStapleCorrect
  ```

You can use the randomised data in the [sample_data folder](/sample_data) to try out the system and see for yourself how quickly it matches 500 mentors and mentees. The record on my hardware is 97 seconds. I've not yet tried it by hand...

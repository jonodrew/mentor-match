# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Users can now edit the weightings, but only for specific attributes, and for the pre-existing calculation



[2.5.0]

### Added
This release adds the notification workflow, using GOV.UK Notify. Getting from the "matching" to the "notification"
workflow is a little rough, and we expect that to be fixed up in the next patch release.

The user interface has once again been designed and implemented by @johnpeart.

We've also added some really nice docs, and so they're being added to this release too - two for the price of one,
you lucky people. As ever the entire system can be brought up with `docker-compose up`. Check out the docs on
`localhost:4000`. Documentation is so important for an open-source system like ours, so additions to that are just
as welcome as code changes.

## [3.0.0] - 2022-06-26

### Changed

The licence for this code has changed from MIT to Open Government Licence. This should not radically change how you
use the software, but because it is a licence change it is breaking - hence the major bump

## [2.4.0] - 2022-06-26

### Added

- This change exposes a route that, on a `POST` request:
  - reads a cookie `task-id`, which is the folder where the output is stored
  - receives a form from the request, which has a `template-id`, a `reply-id`, a `service`, and an `api-key`
  - the `service` defaults to Notify, so for the moment that choice doesn't need to be coded into the system
  - it creates the appropriate client for the `service`, and then sends every participant, in both files in the
    output folder, the `template-id` email using each row in the file as the personalisation
  - the emails are handed off to Celery to take care of
  - this does not yet take account of any other templates: for example, templates where no matches have been made.
    These `template-id`s would need to be passed, somehow, from the frontend. Alternatively, a template could be
    designed that comprises big `if ...then` blocks



## [2.3.3] - 2022-06-25

### Changed

- the underlying package has been bumped, but we'd already taken advantage of the warnings and fixed everything up

## [2.3.2] - 2022-06-25

### Added

- the flask application, accessed via `current_app`, now exposes the current version of this software at
  `current_app.config["VERSION]`

## [2.3.1] - 2022-06-20

### Added

- This release adds an interface exposing the functionality we built in 2.3.0

## [2.3.0] - 2022-06-19

### Changed
- The system now uses pickle under the hood, so please be careful - if you've not secured the connections between
  the machines you're running this on you could really get yourself into trouble.
- However, it has made it significantly faster - a single matching exercise is now down to just 40s, from a best of
  97s when we were using JSON to serialize data.

### Added

- This is the big one. We've added functionality that will creep up an `UnmatchedBonus`. This functionality is
  useful if you want to ensure everyone gets at least one mentor. It calculates a lot of values - one client is
  calculating 37 different iterations of a three-round program, requiring 111 rounds of matching - so it takes a bit
  longer to calculate. Exposing this functionality in the front end will be patched very soon, but in the meantime
  dig around in the routes section or add a `"pairing": True` key-value pair to your JSON call to the appropriate
  endpoint.
- Given the huge amount of processing happening, this functionality takes a lot longer than you're expecting. It's
  enough time to make several cups of tea - on my hardware, it's clocking in at around 7 or 8 minutes. That's a long
  time to stare at the same screen. We'll be updating the frontend to give more feedback soon, but for the moment,
  either check the logs from celery or accept that you'll be here a little while.
- A note about the approach: I could have built a system that iterated over potential outcomes sequentially,
  stopping when it got to the approach that scored above a specific threshold. I see two problems with this. First,
  assuming that each matching process takes _n_ seconds, in the worst case iterating upwards takes _Mn_ seconds. In
  the best case, of course, it takes _n_ seconds!
- My approach batches up the number of approaches into chunks of ten (_M_/10) that are done simultaneously (_Mn_/10).
  This is therefore generally faster, although not in the case where the first outcome is the one we want. Given
  that I can't predict things will be perfect every time, I've opted for the apparently longer approach.

## [2.2.0] - 2022-05-26

### Changed

- The weightings in the `base_rules` was wrong. This is now fixed

## [2.1.0] - 2022-05-20

### Changed

- The `CSMentee`/`CSMentor` classes now expose `target_profession` and `current_profession` as properties. This
  doesn't impact the running of the service.

## [2.0.2] - 2022-05-19

### Changed

- the spreadsheet output filenames have changed from "mentee" to "csmentee" and "mentor" to "csmentor"

## [2.0.0] - 2022-05-08

### Changed

- The spreadsheet outputs have radically changed. This aligns with changes needed by the CSLGBTQ+ network for the next
  round of mentoring. In future releases, I'm going to try to generalise these changes so that other networks can
  use the system with greater ease. However, if you relied on the old spreadsheet, **DO NOT UPDATE TO THIS VERSION**.
  The new headings are:

| first name | last name | email address | number of matches | mentor only | mentee only | both mentor and mentee | match details |
|------------|-----------|---------------|-------------------|-------------|-------------|------------------------|---------------|

- the weightings have also changed:

| quality                    | old weighting | new weighting |
|----------------------------|---------------|---------------|
| exactly 2 grades different | 6             | 12            |
| exactly 1 grade different  | 3             | 9             |
| target profession          | 5             | 10            |
| characteristic match       | 4             | 6             |

## [1.1.0]

### Added

- New classes! There's now a CSMentor and a CSMentee, to reflect the specific needs of these users.

### Changed

- The input spreadsheet has changed again, which is why this is a minor update on 1.0.2. This reflects the 2022/23
  round of mentoring, where we're including more data and tweaking how we match people

## [1.0.2] - 2022-04-15

## Changed

- There's now a mapping function to convert the csv file the CS LGBT+ network uses into the format required by the
  underlying library. Remember to update this when the headings in the csv file change.

## [1.0.0] - 2022-03-12
Welcome to version 1 of this interface to the mentor-matching project! Thanks to a change in the underlying package we use, we've had to make a bit of a tweak to the package. So we figured why not actually write a changelog for this, for the first time ever?

### Added
- Default weightings for the matchings. These can be found in [the `run_task` route](mentor_match_web/app/main/routes.py)

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Users can now edit the weightings, but only for specific attributes, and for the pre-existing calculation

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
- Default weightings for the matchings. These can be found in [the `run_task` route](./app/main/routes.py)

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Users can now edit the weightings, but only for specific attributes, and for the pre-existing calculation

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

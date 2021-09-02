# Mentor Match

This is a package to help match mentees and mentors. It's specifically designed for a volunteer programme I support, but you could probably extend or alter it to suit whatever you're doing.

It uses [this implementation of Munkres](https://github.com/bmc/munkres) to find the most effective pairings. The Munkres algorithm works on a grid of scores.

## Scoring

Full details of how the matches are calculated can be read in the code itself.
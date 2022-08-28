# Mentor-match infrastructure

This folder contains infrastructure for deploying this project into AWS. It is a work in progress and should be
treated as such until version 2.6.0 is released

## Architecture

A state machine orchestrates the various tasks that we use to find the right matches. It looks like this:
![](../../../Downloads/stepfunctions_graph.png)

If a user has chosen to take the best matches, but with fewer people being matched, the path is simple: we run the
data processing code. If the user has chosen to have more people matched, but with slightly worse overall matches,
our task is to find the approach that results in the best case in that scenario. We do this by running every
possible permutation of data and unmatched bonus, then reduce all those results back down to the single best outcome.

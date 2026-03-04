# Exercises - Chapter 01

## Basic
1. Add one more intent in v1 (for example: `status`).
2. In v2, append a timestamp field to the envelope.

## Intermediate
1. In v3, add an explicit `validation` event between ingress and act.
2. Record message latency in milliseconds inside the final result.

## Challenge
Implement a tiny replay function that re-runs lifecycle events from saved envelopes.

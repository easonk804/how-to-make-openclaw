# Exercises - Chapter 02

## Basic
1. Add a new channel (`slack`) in v1 routing.
2. Add a new rule in v2 for `channel=webchat`.

## Intermediate
1. In v3, support `transform_only` adapters that do not send outputs.
2. Add adapter metrics: dispatch count per adapter.

## Challenge
Implement a fallback chain: if primary adapter fails, dispatch to backup adapter.

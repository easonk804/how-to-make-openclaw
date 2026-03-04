# Exercises - Chapter 03

## Basic
1. Add a `tenant` dimension into session key generation.
2. Make v2 cap history length to 8 messages.

## Intermediate
1. Add a `per-channel` strategy in v3.
2. Add `session_reset` when message includes keyword `reset`.

## Challenge
Implement scoped session migration: move existing session history from `main` to `per-peer` without losing messages.

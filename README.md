# Waymo Scene Verifier

A mini V&V tool for the Waymo Open Dataset — parses driving
scenes, runs automated checks to flag edge cases, and reports scenario
coverage on a dashboard.

![Labeled front-camera frame](https://github.com/user-attachments/assets/be2afc57-3d94-4512-ae80-1aaaddfb2a3a))

## Why
AV testing depends on knowing WHAT scenarios you've
covered and whether the data is trustworthy. This tool explores both.

## Status / Roadmap
Your 5 phases as checkboxes (✅ Phase 0, ✅ Phase 1, ...)

## Stack
Colab, Python, waymo-open-dataset, pandas,
Matplotlib, Streamlit (planned)

## Setup notes (the war stories — do NOT skip this section)
- Package pins jaxlib 0.4.13 (no Python 3.12 wheels) → installed with
  --no-deps per waymo-open-dataset issue #868
- protobuf conflict triangle: TF 2.20 needs >=5.28, others need <6 →
  resolved at protobuf 5.29.1 (constraint intersection)

## Findings log
- Frame from segment 10017090168044687777: metadata says "sunny,"
  camera shows wet road + fog. Labels need verification — which is
  the point of this project.

# Waymo Scene Verifier

A verification and validation (V&V) tool built on the [Waymo Open Dataset](https://waymo.com/open).
It parses autonomous driving scenes, extracts scene metadata into a queryable
database, runs an automated check suite to flag edge cases and coverage gaps,
and reports findings on a live dashboard.

**Live dashboard:** https://waymo-scene-verifier-vlsaxgrezfew3egm7sa4yj.streamlit.app/

![Dashboard screenshot](dashboard_screenshot.png)

## Architecture

The pipeline flows in one direction. Raw sensor data is parsed once into
structured metadata, and every downstream stage (checks, reporting, dashboard)
reads only the structured tables. Checks and reporting are fully decoupled
from parsing.

## Metadata pipeline

- Parses Waymo Perception Dataset segments (TFRecord and protobuf formats)
- Extracts per segment metadata: segment ID, time of day, weather, location,
  and object counts (vehicles, pedestrians, cyclists) from labeled data
- Stores results in SQLite and CSV for querying and downstream checks
- Re-runnable end to end. The database write is idempotent, so repeated runs
  do not duplicate rows

## Automated checks

The suite includes two kinds of checks: scene level checks that flag
individual segments, and dataset level checks that flag coverage gaps in the
sample as a whole. Every check returns findings in a common format
(`check_id`, `segment_id`, `severity`, `description`). A runner executes all
checks and collects the findings into a defect report (`findings.csv`).

| Check | Level | What it flags | Severity | Rationale |
|-------|-------|---------------|----------|-----------|
| C1 | Scene | Pedestrian count exceeds threshold (6) | warning | Crowded scenes are high risk for perception systems. A threshold of six represents roughly two small family groups in one scene, beyond incidental foot traffic. |
| C2 | Scene | Cyclists present | info | Vulnerable road users are priority test scenarios: fast moving, small profile, high occlusion risk. |
| C3 | Scene | Zero vehicles in scene | warning | An empty road scene may indicate a data issue or an unusual location worth review. |
| C4 | Dataset | No non daytime segments in sample | warning | A sample with zero night coverage cannot catch night driving regressions. |
| C5 | Dataset | No adverse weather segments in sample | warning | A sample with zero rain or fog coverage cannot catch adverse weather regressions. |

Checks that find nothing return no findings, so a clean dataset produces an
empty defect report.

## Current findings (5 segment sample)

| Check | Segment | Severity | Finding |
|-------|---------|----------|---------|
| C1 | 10023947602400723454_1120... | warning | 27 pedestrians exceeds threshold of 6 |
| C2 | 10072140764565668044_4060... | info | 1 cyclist, vulnerable road user present |
| C4 | ALL | warning | 0 of 5 segments are non daytime, no night coverage in sample |
| C5 | ALL | warning | 0 of 5 segments have adverse weather, no coverage in sample |

Key result: the automated checks confirmed that this dataset slice has zero
night coverage and zero adverse weather coverage. This sample cannot catch
night or rain regressions. Surfacing coverage gaps like these before a test
campaign relies on the data is a core function of a verification tool.

## Stack

- Python (pandas, numpy)
- waymo-open-dataset, the official parser for TFRecord and protobuf segment files
- SQLite for the queryable metadata store
- Streamlit for the dashboard, hosted on Streamlit Cloud
- Google Colab as the parsing environment (dataset files are roughly 1 GB each)

## Run locally

`cd waymo-scene-verifier`
`pip install -r requirements.txt`
`streamlit run app.py`


## Limitations and future work

Validated on a 5 segment development sample. The pipeline, checks, and runner
scale to the full dataset (roughly 2,000 segments) without modification; only
the download loop grows. Planned improvements:

- Per frame maximum object counts. Current counts come from the first frame,
  and objects enter and exit across a segment's roughly 200 frames
- Occlusion proxy checks for dense scenes where objects are likely to block
  the camera's view of other objects
- Camera frame drill down view in the dashboard
- Severity weighted coverage scoring across larger samples

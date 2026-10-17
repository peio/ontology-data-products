# Ontology-Driven Data Products

Workshop materials for **AI Week Frankfurt, October 2026**.

How leading data publishers build data products on top of ontologies and knowledge
graphs — and how AI accelerates every step of the pipeline, from requirements to
integration.

## What you will take away

- **Case studies** of leading data publishers with real data products built using this approach
- **A hands-on tutorial** for building the data product pipeline end to end
- **This repository**, with the code and data used in the workshop
- **A value model** for estimating the drivers and measurable benefits of the approach

## Agenda

| # | Part | Material |
|---|------|----------|
| 1 | Current state — the data product catalog of a leading European data company | [docs/01-current-state.md](docs/01-current-state.md) |
| 2 | State of the art — what leading data providers do (S&P Global, Bloomberg) | [docs/02-state-of-the-art.md](docs/02-state-of-the-art.md) |
| 3 | ROI drivers — return-on-investment hypothesis and value drivers | [docs/03-roi-drivers.md](docs/03-roi-drivers.md) |
| 4 | Tutorial — the data product pipeline | [tutorial/](tutorial/README.md) |
| 5 | Target state — what already works, measurable outcomes | [docs/05-target-state.md](docs/05-target-state.md) |

## The pipeline

```text
Elicitation → Modelling → Mapping → Ingesting → Indexing & Retrieving → Integrating
```

| Step | Folder |
|------|--------|
| Elicitation of requirements | [tutorial/01-elicitation](tutorial/01-elicitation/) |
| Modelling | [tutorial/02-modelling](tutorial/02-modelling/) |
| Mapping | [tutorial/03-mapping](tutorial/03-mapping/) |
| Ingesting | [tutorial/04-ingesting](tutorial/04-ingesting/) |
| Indexing and retrieving | [tutorial/05-indexing-retrieving](tutorial/05-indexing-retrieving/) |
| Integrating | [tutorial/06-integrating](tutorial/06-integrating/) |

## Repository layout

```text
docs/        Talk material: case studies, ROI drivers, target state
tutorial/    Step-by-step pipeline, one folder per step
data/        Sample source data used in the tutorial
slides/      Presentation slides
```

## Prerequisites

_To be completed once the tutorial tooling is fixed._

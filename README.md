# Ontology-Driven Data Products

Workshop materials for **AI Week Frankfurt, October 2026**.

How leading data publishers build data products on top of ontologies and knowledge
graphs — and how AI accelerates the work, from requirements to a tested knowledge
graph.

## What you will take away

- **Case studies** of leading data publishers with real data products built using this approach
- **A hands-on tutorial** that builds and tests an ontology for the EURO STOXX 50 constituents, step by step
- **This repository**, with the code and data used in the workshop
- **A value model** for estimating the drivers and measurable benefits of the approach

## Agenda

| # | Part | Material |
|---|------|----------|
| 1 | Current state — the data product catalog of a leading European data company | |
| 2 | State of the art — what leading data providers do (S&P Global, Bloomberg) | [literature/](literature/README.md#links) |
| 3 | ROI drivers — return-on-investment hypothesis and value drivers | [literature/](literature/README.md#slide-decks) |
| 4 | Tutorial — a tested ontology for the EURO STOXX 50 constituents | [tutorial/](tutorial/README.md) |
| 5 | Target state — what already works, measurable outcomes | |
## The tutorial

The [tutorial](tutorial/README.md) builds a small OWL ontology for the 50 EURO STOXX 50
constituents, linked to the ICB industry taxonomy (SKOS), following the nine steps of
the Graphwise ontology-engineer methodology. It maps the source CSVs to RDF, validates
the result with SHACL and checks it against two sets of competency questions:
robustness tests and business questions with a precomputed answer key.

Every design decision, and what was rejected, is recorded in the
[decision log](tutorial/decision-log.md). The `tutorial/` folder is self-contained and
holds the authoritative copy of all data; see [tutorial/data](tutorial/data/README.md)
for sources and licences.

## Claude Code plugin

This repository is also a Claude Code plugin marketplace. It ships the
**graphwise-ontology** plugin, which contains the
[graphwise-ontology-engineer](plugins/graphwise-ontology/skills/graphwise-ontology-engineer/SKILL.md) skill:
it designs OWL/RDFS/SKOS ontologies as Turtle files, reusing standard vocabularies
(DCAT, Dublin Core, PROV-O, Schema.org, SKOS, FOAF, FIBO) and testing them with
SHACL shapes and SPARQL competency-question queries. See
[SEQUENCE.md](plugins/graphwise-ontology/skills/graphwise-ontology-engineer/SEQUENCE.md) for the steps it follows.

Install it from inside Claude Code:

```text
/plugin marketplace add peio/ontology-data-products
/plugin install graphwise-ontology@ontology-data-products
```

Then ask Claude to model a domain, for example _"Design an ontology for wine and
food pairing"_. The skill triggers on its own; you can also call it directly as
`/graphwise-ontology:graphwise-ontology-engineer`.

To pick up a newer version later, run `/plugin marketplace update ontology-data-products`.

## Repository layout

```text
tutorial/                    EURO STOXX 50 tutorial: data, ontology, shapes, queries, scripts, reports
literature/                  Methodology papers, slide decks and links
plugins/graphwise-ontology/  The installable Claude Code plugin (manifest and skills)
.claude-plugin/              Marketplace manifest
```

## Prerequisites

To run the tutorial you need Python 3.10 or later:

```bash
cd tutorial
pip install -r requirements.txt
python scripts/map_csv.py
python scripts/make_answer_key.py
python scripts/run_tests.py
```

GraphDB is optional: everything runs locally with rdflib, pySHACL and owlrl. The
[tutorial README](tutorial/README.md#load-into-graphdb) explains how to load the
result into GraphDB.

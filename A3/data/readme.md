# JSON Configuration format

**This document describes the required JSON file formats for the Cost Allocation Tool.**


    Directory Structure
    data/
    ├── room_types.json
    ├── space_keywords.json
    ├── cost_rates.json
    ├── weights_default.json
    └── custom_data/
        ├── cost_rates.json
        └── custom_weights.json

## room_types.json — Room Type Definitions

**Purpose: Defines room types.**

**Format:**

    [
    "OFFICE",
    "MEETING_ROOM",
    "LABORATORY",
    "KITCHEN",
    "RESTROOM",
    "CORRIDOR",
    "STORAGE"
    ]


Rules:

Json format

## space_keywords.json — Space Classification

Purpose: Maps IFC Space names to room types.

Format:

    {
    "OFFICE": ["office", "kontor", "arbeidsplass", "workstation"],
    "MEETING_ROOM": ["meeting", "conference", "møte", "konferanse"],
    "LABORATORY": ["lab", "laboratory", "laboratorium", "forsknings"],
    "KITCHEN": ["kitchen", "kjøkken", "pantry"],
    "RESTROOM": ["restroom", "toilet", "bathroom", "wc", "dush"],
    "CORRIDOR": ["corridor", "hallway", "gang", "korridor"],
    "STORAGE": ["storage", "lager", "arkiv", "closet"]
    }


Rules:

- Keys must exist in room_types.json

- Classification is substring-based

No match → "UNCLASSIFIED"

Examples:

    "Office 101" → OFFICE

    "Chemistry Lab" → LABORATORY

    "Random Space" → UNCLASSIFIED

## cost_rates.json — Cost Rates

**Purpose: Defines cost rates per m².**

Format:

    {
    "electricity": 15.50,
    "water": 5.25,
    "cleaning": 8.20,
    "maintenance": 12.00,
    "heating": 10.75,
    "security": 3.50
    }

## weights_default.json — Cost Allocation Weights

**Purpose: Defines how different room types distribute cost.**

Format:

    {
    "OFFICE": {
        "electricity": 1.0,
        "water": 0.8,
        "cleaning": 1.2,
        "maintenance": 1.0,
        "heating": 0.9,
        "security": 1.1
    }
    }



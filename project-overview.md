Project Proposal – Personal Recipe Manager with Nutrition Integration
1. The Big Idea

The goal of this project is to build a personal recipe management software that allows users to create, store, and organize their own recipe collection. Users will manually enter recipes, including ingredients, measurements, and instructions. The software will use a nutrition API (such as Edamam, Spoonacular, or USDA FoodData Central) to automatically retrieve calorie information and potentially other nutritional data.

The system will support sorting and filtering by:

Calories

Ingredient count

Alphabetical order

Specific included/excluded ingredients

Users will effectively build their own custom personal recipe book, generated dynamically based on their preferences and pantry.

Minimum Viable Product (MVP)

Users can add recipes with:

Title

Ingredients + amounts

Instructions

Recipes are stored in a local file or small database (JSON, SQLite, etc.).

Users can sort recipes by:

Alphabetical order

Ingredient count

Users can filter recipes by included/excluded ingredients.

Stretch Goals

Integrate a nutrition API to automatically calculate:

Calories

Other macros (carbs, fat, protein)

Add pantry stock tracking and recipe suggestions based on available ingredients

Support exporting the recipe book (PDF, markdown, etc.)

Add a simple GUI (Tkinter, PyQt, or a web interface)

Allow users to upload images of recipes

2. Learning Objectives
Shared Team Learning Goals

Learn how to design a multi-feature software system using good software design principles (modularity, planning, documentation).

Practice using APIs for live data and authentication.

Learn how to store and manage user-generated data persistently.

Work with GitHub collaboratively (branches, merges, pull requests).

Individual Learning Goals

Student A:

Improve Python skills with functions, classes, and file handling.

Learn to work with external REST APIs (JSON parsing, rate limits, API keys).

3. Implementation Plan
Step 1 — Data Model Design

Define how recipes are stored (likely JSON or SQLite).

Decide on a class structure (e.g., Recipe, Ingredient, RecipeBook).

Step 2 — Core Functionality

Implement functions for adding, editing, deleting, and viewing recipes.

Implement sorting and filtering algorithms.

Test with sample data.

Step 3 — API Investigation

Explore potential nutrition APIs:

Edamam Nutrition Analysis API

Spoonacular Nutrition API

USDA FoodData Central

Test requests and get example JSON responses.
Implement a wrapper to retrieve calorie info.

Step 4 — Integration

Connect ingredient data to the API

Calculate total calories per recipe

Display results in the UI or console

Step 5 (Optional) — UI / Extra Features

Build a simple GUI or web interface

Add pantry-tracking features

Add export features (PDF, markdown, etc.)

4. Project Schedule (4–5 Weeks)
Week 1

Finalize idea

Research APIs

Create GitHub repository

Design data structures

Week 2

Implement recipe storage

Add sorting and filtering

Set up local data persistence

Week 3

Connect nutrition API

Implement calorie calculation

Test interface thoroughly

Week 4

Add optional features (pantry, GUI)

Improve UI/UX

Documentation + cleanup

Week 5

Final testing

Prepare presentation/demo

Submit final project

5. Risks and Limitations

API Limitations: Free API tiers may restrict daily requests or require keys; caching may be needed.

Nutrition Accuracy: Depends on ingredient consistency and API interpretation.

Time Constraints: Stretch features may be removed if the schedule is tight.

User Input Variability: Inconsistent ingredient formatting could affect parsing and calorie retrieval.

"""
Handles persistent storage of recipes using JSON files.
"""

import json
import os
from pathlib import Path
from typing import List, Optional

from .models import Recipe


class RecipeStorage:
    """Manages recipe storage in a JSON file."""
    
    def __init__(self, storage_file: str = "recipes.json"):
        """Initialize storage with a JSON file path."""
        self.storage_file = storage_file
        self._ensure_storage_file()
    
    def _ensure_storage_file(self) -> None:
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.storage_file):
            self._write_recipes([])
    
    def _read_recipes(self) -> List[dict]:
        """Read recipes from JSON file."""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_recipes(self, recipes: List[dict]) -> None:
        """Write recipes to JSON file."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, indent=2, ensure_ascii=False)
    
    def add_recipe(self, recipe: Recipe) -> None:
        """Add a new recipe to storage."""
        recipes = self._read_recipes()
        recipes.append(recipe.to_dict())
        self._write_recipes(recipes)
    
    def get_all_recipes(self) -> List[Recipe]:
        """Retrieve all recipes from storage."""
        recipes_data = self._read_recipes()
        return [Recipe.from_dict(data) for data in recipes_data]
    
    def get_recipe_by_title(self, title: str) -> Optional[Recipe]:
        """Retrieve a recipe by its title."""
        recipes = self.get_all_recipes()
        for recipe in recipes:
            if recipe.title.lower() == title.lower():
                return recipe
        return None
    
    def update_recipe(self, old_title: str, updated_recipe: Recipe) -> bool:
        """Update an existing recipe. Returns True if successful."""
        recipes_data = self._read_recipes()
        for i, recipe_data in enumerate(recipes_data):
            if recipe_data["title"].lower() == old_title.lower():
                recipes_data[i] = updated_recipe.to_dict()
                self._write_recipes(recipes_data)
                return True
        return False
    
    def delete_recipe(self, title: str) -> bool:
        """Delete a recipe by title. Returns True if successful."""
        recipes_data = self._read_recipes()
        original_count = len(recipes_data)
        recipes_data = [
            r for r in recipes_data
            if r["title"].lower() != title.lower()
        ]
        if len(recipes_data) < original_count:
            self._write_recipes(recipes_data)
            return True
        return False
    
    def clear_all(self) -> None:
        """Clear all recipes from storage."""
        self._write_recipes([])


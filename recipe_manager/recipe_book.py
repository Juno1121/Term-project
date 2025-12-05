"""
RecipeBook class for managing and organizing recipes.
"""

from typing import List, Optional, Callable
from enum import Enum

from .models import Recipe
from .storage import RecipeStorage


class SortBy(Enum):
    """Enumeration for sorting options."""
    ALPHABETICAL = "alphabetical"
    INGREDIENT_COUNT = "ingredient_count"
    CALORIES = "calories"


class RecipeBook:
    """Main class for managing a collection of recipes."""
    
    def __init__(self, storage: Optional[RecipeStorage] = None):
        """Initialize RecipeBook with optional storage."""
        self.storage = storage or RecipeStorage()
        self._recipes: List[Recipe] = []
        self._load_recipes()
    
    def _load_recipes(self) -> None:
        """Load recipes from storage."""
        self._recipes = self.storage.get_all_recipes()
    
    def add_recipe(self, recipe: Recipe) -> None:
        """Add a new recipe to the book."""
        self._recipes.append(recipe)
        self.storage.add_recipe(recipe)
    
    def get_recipe(self, title: str) -> Optional[Recipe]:
        """Get a recipe by title."""
        return self.storage.get_recipe_by_title(title)
    
    def update_recipe(self, old_title: str, updated_recipe: Recipe) -> bool:
        """Update an existing recipe."""
        success = self.storage.update_recipe(old_title, updated_recipe)
        if success:
            self._load_recipes()  # Reload to sync
        return success
    
    def delete_recipe(self, title: str) -> bool:
        """Delete a recipe by title."""
        success = self.storage.delete_recipe(title)
        if success:
            self._load_recipes()  # Reload to sync
        return success
    
    def get_all_recipes(self) -> List[Recipe]:
        """Get all recipes."""
        return self._recipes.copy()
    
    def sort_recipes(self, sort_by: SortBy, reverse: bool = False) -> List[Recipe]:
        """Sort recipes by the specified criteria."""
        recipes = self._recipes.copy()
        
        if sort_by == SortBy.ALPHABETICAL:
            recipes.sort(key=lambda r: r.title.lower(), reverse=reverse)
        elif sort_by == SortBy.INGREDIENT_COUNT:
            recipes.sort(key=lambda r: r.get_ingredient_count(), reverse=reverse)
        elif sort_by == SortBy.CALORIES:
            # Sort by calories, putting None values at the end
            recipes.sort(
                key=lambda r: (r.calories is None, r.calories or 0),
                reverse=reverse
            )
        
        return recipes
    
    def filter_by_ingredients(
        self,
        included: Optional[List[str]] = None,
        excluded: Optional[List[str]] = None
    ) -> List[Recipe]:
        """
        Filter recipes by included/excluded ingredients.
        
        Args:
            included: List of ingredient names that must be present
            excluded: List of ingredient names that must not be present
        
        Returns:
            List of recipes matching the filter criteria
        """
        included = included or []
        excluded = excluded or []
        
        filtered = []
        for recipe in self._recipes:
            ingredient_names = [
                ing.name.lower() for ing in recipe.ingredients
            ]
            
            # Check if all included ingredients are present
            has_all_included = all(
                any(inc.lower() in name for name in ingredient_names)
                for inc in included
            )
            
            # Check if none of the excluded ingredients are present
            has_no_excluded = all(
                not any(exc.lower() in name for name in ingredient_names)
                for exc in excluded
            )
            
            if has_all_included and has_no_excluded:
                filtered.append(recipe)
        
        return filtered
    
    def search_recipes(self, query: str) -> List[Recipe]:
        """Search recipes by title or ingredient name."""
        query_lower = query.lower()
        results = []
        
        for recipe in self._recipes:
            # Search in title
            if query_lower in recipe.title.lower():
                results.append(recipe)
                continue
            
            # Search in ingredients
            for ingredient in recipe.ingredients:
                if query_lower in ingredient.name.lower():
                    results.append(recipe)
                    break
        
        return results


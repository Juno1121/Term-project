"""
Data models for the Recipe Manager application.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Ingredient:
    """Represents a single ingredient with its amount."""
    name: str
    amount: str  # e.g., "2 cups", "1 tsp", "500g"
    
    def __str__(self) -> str:
        return f"{self.amount} {self.name}"


@dataclass
class Recipe:
    """Represents a recipe with title, ingredients, and instructions."""
    title: str
    ingredients: List[Ingredient] = field(default_factory=list)
    instructions: str = ""
    calories: Optional[float] = None  # Will be populated by API integration
    
    def __str__(self) -> str:
        return self.title
    
    def get_ingredient_count(self) -> int:
        """Returns the number of ingredients in the recipe."""
        return len(self.ingredients)
    
    def to_dict(self) -> dict:
        """Converts recipe to dictionary for JSON storage."""
        return {
            "title": self.title,
            "ingredients": [
                {"name": ing.name, "amount": ing.amount}
                for ing in self.ingredients
            ],
            "instructions": self.instructions,
            "calories": self.calories
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Recipe':
        """Creates a Recipe instance from a dictionary."""
        ingredients = [
            Ingredient(name=ing["name"], amount=ing["amount"])
            for ing in data.get("ingredients", [])
        ]
        return cls(
            title=data["title"],
            ingredients=ingredients,
            instructions=data.get("instructions", ""),
            calories=data.get("calories")
        )


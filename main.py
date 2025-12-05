"""
Main entry point for the Recipe Manager application.
Launches the GUI interface by default.
"""

import sys
from recipe_manager import RecipeBook, Recipe, Ingredient, SortBy, run_gui


def print_recipe(recipe: Recipe) -> None:
    """Print a recipe in a formatted way."""
    print(f"\n{'='*60}")
    print(f"Recipe: {recipe.title}")
    print(f"{'='*60}")
    
    if recipe.calories:
        print(f"Calories: {recipe.calories:.0f}")
    
    print(f"\nIngredients ({recipe.get_ingredient_count()}):")
    for i, ingredient in enumerate(recipe.ingredients, 1):
        print(f"  {i}. {ingredient}")
    
    if recipe.instructions:
        print(f"\nInstructions:")
        print(recipe.instructions)
    print()


def add_recipe_interactive(book: RecipeBook) -> None:
    """Interactive function to add a new recipe."""
    print("\n--- Add New Recipe ---")
    title = input("Recipe title: ").strip()
    
    if not title:
        print("Error: Recipe title cannot be empty.")
        return
    
    # Check if recipe already exists
    if book.get_recipe(title):
        response = input(f"Recipe '{title}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    ingredients = []
    print("\nEnter ingredients (press Enter with empty line to finish):")
    while True:
        ingredient_input = input("Ingredient (e.g., '2 cups flour'): ").strip()
        if not ingredient_input:
            break
        
        # Simple parsing: assume format is "amount name" or just "name"
        parts = ingredient_input.rsplit(' ', 1)
        if len(parts) == 2:
            amount, name = parts
        else:
            amount = "1"
            name = parts[0]
        
        ingredients.append(Ingredient(name=name, amount=amount))
    
    instructions = input("\nInstructions (press Enter twice to finish):\n")
    lines = []
    while True:
        line = input()
        if not line and lines and not lines[-1]:
            break
        lines.append(line)
    instructions = '\n'.join(lines).strip()
    
    recipe = Recipe(
        title=title,
        ingredients=ingredients,
        instructions=instructions
    )
    
    book.add_recipe(recipe)
    print(f"\nRecipe '{title}' added successfully!")


def list_recipes(book: RecipeBook) -> None:
    """List all recipes with sorting options."""
    print("\n--- List Recipes ---")
    print("Sort by:")
    print("  1. Alphabetical")
    print("  2. Ingredient count")
    print("  3. Calories")
    print("  4. No sorting")
    
    choice = input("Choice (1-4): ").strip()
    
    if choice == "1":
        recipes = book.sort_recipes(SortBy.ALPHABETICAL)
    elif choice == "2":
        recipes = book.sort_recipes(SortBy.INGREDIENT_COUNT, reverse=True)
    elif choice == "3":
        recipes = book.sort_recipes(SortBy.CALORIES, reverse=True)
    else:
        recipes = book.get_all_recipes()
    
    if not recipes:
        print("\nNo recipes found.")
        return
    
    print(f"\nFound {len(recipes)} recipe(s):\n")
    for recipe in recipes:
        print_recipe(recipe)


def filter_recipes(book: RecipeBook) -> None:
    """Filter recipes by ingredients."""
    print("\n--- Filter Recipes ---")
    
    included_input = input("Ingredients to include (comma-separated, or press Enter): ").strip()
    excluded_input = input("Ingredients to exclude (comma-separated, or press Enter): ").strip()
    
    included = [ing.strip() for ing in included_input.split(",")] if included_input else None
    excluded = [ing.strip() for ing in excluded_input.split(",")] if excluded_input else None
    
    if not included and not excluded:
        print("No filter criteria provided.")
        return
    
    filtered = book.filter_by_ingredients(included=included, excluded=excluded)
    
    if not filtered:
        print("\nNo recipes match the filter criteria.")
        return
    
    print(f"\nFound {len(filtered)} matching recipe(s):\n")
    for recipe in filtered:
        print_recipe(recipe)


def search_recipes(book: RecipeBook) -> None:
    """Search recipes by title or ingredient."""
    print("\n--- Search Recipes ---")
    query = input("Search query: ").strip()
    
    if not query:
        print("No search query provided.")
        return
    
    results = book.search_recipes(query)
    
    if not results:
        print(f"\nNo recipes found matching '{query}'.")
        return
    
    print(f"\nFound {len(results)} matching recipe(s):\n")
    for recipe in results:
        print_recipe(recipe)


def delete_recipe(book: RecipeBook) -> None:
    """Delete a recipe."""
    print("\n--- Delete Recipe ---")
    title = input("Recipe title to delete: ").strip()
    
    if not title:
        print("Error: Recipe title cannot be empty.")
        return
    
    if book.delete_recipe(title):
        print(f"Recipe '{title}' deleted successfully!")
    else:
        print(f"Recipe '{title}' not found.")


def main():
    """Main application loop."""
    book = RecipeBook()
    
    print("="*60)
    print("Personal Recipe Manager")
    print("="*60)
    
    while True:
        print("\nMain Menu:")
        print("  1. Add recipe")
        print("  2. List recipes")
        print("  3. Filter recipes")
        print("  4. Search recipes")
        print("  5. Delete recipe")
        print("  6. Exit")
        
        choice = input("\nChoice (1-6): ").strip()
        
        if choice == "1":
            add_recipe_interactive(book)
        elif choice == "2":
            list_recipes(book)
        elif choice == "3":
            filter_recipes(book)
        elif choice == "4":
            search_recipes(book)
        elif choice == "5":
            delete_recipe(book)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def main_cli():
    """Command-line interface (alternative to GUI)."""
    book = RecipeBook()
    
    print("="*60)
    print("Personal Recipe Manager")
    print("="*60)
    
    while True:
        print("\nMain Menu:")
        print("  1. Add recipe")
        print("  2. List recipes")
        print("  3. Filter recipes")
        print("  4. Search recipes")
        print("  5. Delete recipe")
        print("  6. Exit")
        
        choice = input("\nChoice (1-6): ").strip()
        
        if choice == "1":
            add_recipe_interactive(book)
        elif choice == "2":
            list_recipes(book)
        elif choice == "3":
            filter_recipes(book)
        elif choice == "4":
            search_recipes(book)
        elif choice == "5":
            delete_recipe(book)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Launch GUI by default, or CLI if --cli flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_cli()
    else:
        run_gui()


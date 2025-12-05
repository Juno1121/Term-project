"""
Demo script to showcase the Recipe Manager functionality.
This script adds sample recipes and demonstrates sorting and filtering.
"""

from recipe_manager import RecipeBook, Recipe, Ingredient, SortBy


def create_sample_recipes():
    """Create some sample recipes for demonstration."""
    return [
        Recipe(
            title="Chocolate Chip Cookies",
            ingredients=[
                Ingredient("flour", "2 cups"),
                Ingredient("sugar", "1 cup"),
                Ingredient("butter", "1/2 cup"),
                Ingredient("chocolate chips", "1 cup"),
                Ingredient("eggs", "2"),
                Ingredient("vanilla extract", "1 tsp")
            ],
            instructions="1. Mix dry ingredients\n2. Cream butter and sugar\n3. Add eggs and vanilla\n4. Combine wet and dry ingredients\n5. Fold in chocolate chips\n6. Bake at 375°F for 10-12 minutes"
        ),
        Recipe(
            title="Simple Pasta",
            ingredients=[
                Ingredient("pasta", "8 oz"),
                Ingredient("olive oil", "2 tbsp"),
                Ingredient("garlic", "2 cloves"),
                Ingredient("salt", "1 tsp")
            ],
            instructions="1. Boil pasta according to package directions\n2. Heat olive oil in pan\n3. Sauté garlic until fragrant\n4. Toss pasta with oil and garlic\n5. Season with salt"
        ),
        Recipe(
            title="Vegetable Stir Fry",
            ingredients=[
                Ingredient("broccoli", "2 cups"),
                Ingredient("carrots", "1 cup"),
                Ingredient("bell peppers", "1 cup"),
                Ingredient("soy sauce", "2 tbsp"),
                Ingredient("ginger", "1 tsp"),
                Ingredient("garlic", "2 cloves"),
                Ingredient("vegetable oil", "1 tbsp")
            ],
            instructions="1. Heat oil in wok\n2. Add garlic and ginger\n3. Stir fry vegetables until crisp-tender\n4. Add soy sauce\n5. Serve hot"
        ),
        Recipe(
            title="Scrambled Eggs",
            ingredients=[
                Ingredient("eggs", "3"),
                Ingredient("butter", "1 tbsp"),
                Ingredient("salt", "pinch"),
                Ingredient("pepper", "pinch")
            ],
            instructions="1. Beat eggs with salt and pepper\n2. Heat butter in pan\n3. Pour in eggs\n4. Scramble until cooked to desired consistency"
        )
    ]


def main():
    """Run the demo."""
    print("="*60)
    print("Recipe Manager - Demo")
    print("="*60)
    
    # Create a new RecipeBook
    book = RecipeBook()
    
    # Add sample recipes
    print("\n[+] Adding sample recipes...")
    sample_recipes = create_sample_recipes()
    for recipe in sample_recipes:
        book.add_recipe(recipe)
        print(f"  [OK] Added: {recipe.title}")
    
    # Show all recipes
    print(f"\n[INFO] Total recipes: {len(book.get_all_recipes())}")
    
    # Demonstrate sorting
    print("\n" + "="*60)
    print("SORTING DEMONSTRATION")
    print("="*60)
    
    print("\n1. Sorted Alphabetically:")
    sorted_alphabetical = book.sort_recipes(SortBy.ALPHABETICAL)
    for recipe in sorted_alphabetical:
        print(f"   - {recipe.title}")
    
    print("\n2. Sorted by Ingredient Count (most ingredients first):")
    sorted_by_count = book.sort_recipes(SortBy.INGREDIENT_COUNT, reverse=True)
    for recipe in sorted_by_count:
        print(f"   - {recipe.title} ({recipe.get_ingredient_count()} ingredients)")
    
    # Demonstrate filtering
    print("\n" + "="*60)
    print("FILTERING DEMONSTRATION")
    print("="*60)
    
    print("\n1. Recipes containing 'eggs':")
    filtered_with_eggs = book.filter_by_ingredients(included=["eggs"])
    for recipe in filtered_with_eggs:
        print(f"   - {recipe.title}")
    
    print("\n2. Recipes containing 'garlic' but NOT 'butter':")
    filtered_complex = book.filter_by_ingredients(
        included=["garlic"],
        excluded=["butter"]
    )
    for recipe in filtered_complex:
        print(f"   - {recipe.title}")
    
    # Demonstrate search
    print("\n" + "="*60)
    print("SEARCH DEMONSTRATION")
    print("="*60)
    
    print("\nSearching for 'chocolate':")
    search_results = book.search_recipes("chocolate")
    for recipe in search_results:
        print(f"   - {recipe.title}")
    
    print("\nSearching for 'pasta':")
    search_results = book.search_recipes("pasta")
    for recipe in search_results:
        print(f"   - {recipe.title}")
    
    # Show a detailed recipe
    print("\n" + "="*60)
    print("RECIPE DETAIL VIEW")
    print("="*60)
    recipe = book.get_recipe("Chocolate Chip Cookies")
    if recipe:
        print(f"\nRecipe: {recipe.title}")
        print(f"Ingredients ({recipe.get_ingredient_count()}):")
        for i, ing in enumerate(recipe.ingredients, 1):
            print(f"  {i}. {ing}")
        print(f"\nInstructions:\n{recipe.instructions}")
    
    print("\n" + "="*60)
    print("Demo complete! Recipes saved to recipes.json")
    print("="*60)
    print("\nTo use the interactive interface, run: python main.py")


if __name__ == "__main__":
    main()


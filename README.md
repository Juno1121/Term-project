# Personal Recipe Manager

A Python-based recipe management system that allows users to create, store, and organize their personal recipe collection with support for sorting, filtering, and future nutrition API integration.

**Team member:** Juno Park

## Features

### MVP (Current Implementation)
- ✅ Add, edit, delete, and view recipes
- ✅ Store recipes in JSON format
- ✅ Sort recipes by:
  - Alphabetical order
  - Ingredient count
  - Calories (when available)
- ✅ Filter recipes by included/excluded ingredients
- ✅ Search recipes by title or ingredient name

### Planned Features (Stretch Goals)
- 🔄 Nutrition API integration (Edamam, Spoonacular, or USDA FoodData Central)
- 🔄 Pantry stock tracking
- 🔄 Recipe suggestions based on available ingredients
- 🔄 Export functionality (PDF, markdown)
- 🔄 GUI interface (Tkinter, PyQt, or web)
- 🔄 Image upload support

## Project Structure

```
Term-project/
├── recipe_manager/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── models.py           # Data models (Recipe, Ingredient)
│   ├── storage.py          # JSON storage management
│   └── recipe_book.py      # RecipeBook class with sorting/filtering
├── main.py                  # Command-line interface entry point
├── requirements.txt         # Python dependencies
├── project-overview.md      # Project proposal and plan
└── README.md               # This file
```

## Installation

1. Clone the repository
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies (currently none required for MVP):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

The application provides an interactive menu:
1. **Add recipe** - Create a new recipe with ingredients and instructions
2. **List recipes** - View all recipes with sorting options
3. **Filter recipes** - Filter by included/excluded ingredients
4. **Search recipes** - Search by title or ingredient name
5. **Delete recipe** - Remove a recipe from your collection
6. **Exit** - Quit the application

## Data Storage

Recipes are stored in `recipes.json` in the project root directory. This file is automatically created when you add your first recipe.

## Development Status

- **Week 1-2**: ✅ Core functionality and data storage
- **Week 3**: 🔄 API integration (in progress)
- **Week 4-5**: 🔄 Additional features and polish

## License

This is a term project for educational purposes.

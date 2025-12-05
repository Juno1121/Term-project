"""
GUI interface for the Recipe Manager using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, List
from .recipe_book import RecipeBook, SortBy
from .models import Recipe, Ingredient


class RecipeDialog:
    """Dialog window for adding/editing recipes."""
    
    # Common measurement units
    MEASUREMENTS = [
        "", "cup", "cups", "tbsp", "tsp", "oz", "lb", "g", "kg", 
        "ml", "l", "piece", "pieces", "clove", "cloves", "slice", "slices",
        "can", "cans", "package", "packages", "pinch", "dash", "dash"
    ]
    
    def __init__(self, parent, recipe: Optional[Recipe] = None):
        self.parent = parent
        self.recipe = recipe
        self.result = None
        self.ingredient_instructions = {}  # Store instructions per ingredient
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Recipe" if recipe is None else "Edit Recipe")
        self.dialog.geometry("700x850")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (850 // 2)
        self.dialog.geometry(f"700x850+{x}+{y}")
        
        self._create_widgets()
        if recipe:
            self._populate_fields()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Title
        ttk.Label(self.dialog, text="Recipe Title:", font=("Arial", 10, "bold")).pack(pady=(10, 5), padx=20, anchor="w")
        self.title_entry = ttk.Entry(self.dialog, font=("Arial", 11))
        self.title_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Main container with paned window for resizable sections
        main_paned = ttk.PanedWindow(self.dialog, orient="vertical")
        main_paned.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Ingredients frame
        ingredients_frame = ttk.LabelFrame(main_paned, text="Ingredients", padding=10)
        main_paned.add(ingredients_frame, weight=1)
        
        # Ingredients list with scrollbar (clickable)
        list_frame = tk.Frame(ingredients_frame)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.ingredients_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set, 
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        self.ingredients_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.ingredients_listbox.yview)
        
        # Bind click event to show ingredient instructions
        self.ingredients_listbox.bind("<<ListboxSelect>>", self._on_ingredient_select)
        
        # Ingredient input frame
        input_frame = tk.Frame(ingredients_frame)
        input_frame.pack(fill="x", pady=(10, 0))
        
        # Amount (number)
        ttk.Label(input_frame, text="Amount:").pack(side="left", padx=(0, 5))
        self.amount_entry = ttk.Entry(input_frame, width=8)
        self.amount_entry.pack(side="left", padx=(0, 5))
        
        # Measurement dropdown
        ttk.Label(input_frame, text="Unit:").pack(side="left", padx=(0, 5))
        self.measurement_combo = ttk.Combobox(input_frame, width=12, values=self.MEASUREMENTS, state="readonly")
        self.measurement_combo.pack(side="left", padx=(0, 10))
        self.measurement_combo.set("")
        
        # Ingredient name
        ttk.Label(input_frame, text="Ingredient:").pack(side="left", padx=(0, 5))
        self.ingredient_entry = ttk.Entry(input_frame, width=20)
        self.ingredient_entry.pack(side="left", padx=(0, 10))
        
        add_btn = ttk.Button(input_frame, text="Add", command=self._add_ingredient)
        add_btn.pack(side="left", padx=(0, 5))
        
        remove_btn = ttk.Button(input_frame, text="Remove", command=self._remove_ingredient)
        remove_btn.pack(side="left")
        
        # Instructions frame
        instructions_frame = ttk.LabelFrame(main_paned, text="Instructions", padding=10)
        main_paned.add(instructions_frame, weight=1)
        
        # Instructions header with clickable ingredients
        header_frame = tk.Frame(instructions_frame)
        header_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(header_frame, text="Click an ingredient above to add instructions for it:", 
                 font=("Arial", 9)).pack(side="left")
        
        # Selected ingredient display
        self.selected_ingredient_label = ttk.Label(header_frame, text="", font=("Arial", 9, "bold"), foreground="blue")
        self.selected_ingredient_label.pack(side="left", padx=(10, 0))
        
        # Dynamic ingredient instruction field (initially hidden)
        self.ingredient_instruction_frame = tk.Frame(instructions_frame)
        
        self.ingredient_instruction_label = ttk.Label(
            self.ingredient_instruction_frame, 
            text="", 
            font=("Arial", 9, "bold")
        )
        self.ingredient_instruction_label.pack(anchor="w", pady=(0, 5))
        
        self.ingredient_instruction_text = scrolledtext.ScrolledText(
            self.ingredient_instruction_frame, 
            height=3, 
            font=("Arial", 9),
            wrap="word"
        )
        self.ingredient_instruction_text.pack(fill="x", pady=(0, 10))
        
        # Save ingredient instruction button
        save_ing_btn = ttk.Button(
            self.ingredient_instruction_frame, 
            text="Save Instruction", 
            command=self._save_ingredient_instruction
        )
        save_ing_btn.pack(anchor="w")
        
        # Main instructions text area
        ttk.Label(instructions_frame, text="General Instructions:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 5))
        self.instructions_text = scrolledtext.ScrolledText(instructions_frame, height=6, font=("Arial", 10), wrap="word")
        self.instructions_text.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Save Recipe", command=self._save, width=18).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self._cancel, width=18).pack(side="left", padx=5)
        
        # Bind Enter key to add ingredient
        self.ingredient_entry.bind("<Return>", lambda e: self._add_ingredient())
        self.amount_entry.bind("<Return>", lambda e: self.measurement_combo.focus())
        self.measurement_combo.bind("<Return>", lambda e: self.ingredient_entry.focus())
    
    def _populate_fields(self):
        """Populate fields with existing recipe data."""
        if not self.recipe:
            return
        
        self.title_entry.insert(0, self.recipe.title)
        
        # Load all instructions into the main box (they're already formatted)
        self.instructions_text.insert("1.0", self.recipe.instructions)
        
        # Parse instructions to extract ingredient-specific ones for editing
        instructions = self.recipe.instructions
        ingredient_specific = {}
        
        # Look for patterns like "amount unit ingredient_name: instruction" or "ingredient_name: instruction"
        lines = instructions.split('\n')
        for line in lines:
            # Check if line contains an ingredient name followed by colon
            for ingredient in self.recipe.ingredients:
                # Match patterns like "2 cups flour: instruction" or "flour: instruction"
                if f"{ingredient.name}:" in line:
                    # Extract instruction after colon
                    if ":" in line:
                        instruction_part = line.split(":", 1)[1].strip()
                        ingredient_specific[ingredient.name] = instruction_part
                    break
        
        # Add ingredients and store their instructions for editing
        for ingredient in self.recipe.ingredients:
            self.ingredients_listbox.insert(tk.END, f"{ingredient.amount} {ingredient.name}")
            # Store ingredient-specific instruction if exists (for editing in the popup)
            self.ingredient_instructions[ingredient.name] = ingredient_specific.get(ingredient.name, "")
    
    def _add_ingredient(self):
        """Add ingredient to the list."""
        amount_num = self.amount_entry.get().strip()
        measurement = self.measurement_combo.get().strip()
        name = self.ingredient_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter an ingredient name.")
            return
        
        # Build amount string
        if not amount_num:
            amount_num = "1"
        
        if measurement:
            amount = f"{amount_num} {measurement}"
        else:
            amount = amount_num
        
        # Add to listbox
        display_text = f"{amount} {name}"
        self.ingredients_listbox.insert(tk.END, display_text)
        
        # Initialize empty instructions for this ingredient
        self.ingredient_instructions[name] = ""
        
        # Clear input fields
        self.amount_entry.delete(0, tk.END)
        self.measurement_combo.set("")
        self.ingredient_entry.delete(0, tk.END)
        self.amount_entry.focus()
    
    def _remove_ingredient(self):
        """Remove selected ingredient from the list."""
        selection = self.ingredients_listbox.curselection()
        if selection:
            item_text = self.ingredients_listbox.get(selection[0])
            # Extract ingredient name (everything after the amount)
            parts = item_text.split(" ", 2)
            if len(parts) >= 3:
                ingredient_name = parts[2]
            elif len(parts) == 2:
                ingredient_name = parts[1]
            else:
                ingredient_name = parts[0]
            
            # Remove from listbox and instructions dict
            self.ingredients_listbox.delete(selection[0])
            if ingredient_name in self.ingredient_instructions:
                del self.ingredient_instructions[ingredient_name]
            
            # Hide instruction frame if this was the selected ingredient
            self._hide_ingredient_instruction()
    
    def _on_ingredient_select(self, event):
        """Handle ingredient selection to show instruction field."""
        selection = self.ingredients_listbox.curselection()
        if not selection:
            self._hide_ingredient_instruction()
            return
        
        item_text = self.ingredients_listbox.get(selection[0])
        # Parse ingredient name from display text
        parts = item_text.split(" ", 2)
        if len(parts) >= 3:
            ingredient_name = parts[2]
        elif len(parts) == 2:
            ingredient_name = parts[1]
        else:
            ingredient_name = parts[0]
        
        # Show instruction frame
        self.selected_ingredient_label.config(text=f"Selected: {ingredient_name}")
        self.ingredient_instruction_label.config(text=f"Instructions for {ingredient_name}:")
        
        # Load existing instruction if any
        instruction = self.ingredient_instructions.get(ingredient_name, "")
        self.ingredient_instruction_text.delete("1.0", tk.END)
        self.ingredient_instruction_text.insert("1.0", instruction)
        
        # Store current ingredient name for saving
        self.current_ingredient_name = ingredient_name
        
        # Show the instruction frame
        if not self.ingredient_instruction_frame.winfo_ismapped():
            self.ingredient_instruction_frame.pack(fill="x", pady=(5, 0), before=self.instructions_text)
    
    def _save_ingredient_instruction(self):
        """Save instruction for the currently selected ingredient and add to main instructions box."""
        if not hasattr(self, 'current_ingredient_name'):
            return
        
        instruction = self.ingredient_instruction_text.get("1.0", tk.END).strip()
        if not instruction:
            messagebox.showwarning("Warning", "Please enter an instruction.")
            return
        
        # Get the ingredient amount from the listbox
        selection = self.ingredients_listbox.curselection()
        if selection:
            item_text = self.ingredients_listbox.get(selection[0])
            # Format: "amount ingredient_name"
            formatted_instruction = f"{item_text}: {instruction}"
        else:
            formatted_instruction = f"{self.current_ingredient_name}: {instruction}"
        
        # Get current instructions
        current_instructions = self.instructions_text.get("1.0", tk.END).strip()
        
        # Check if instruction for this ingredient already exists and replace it
        if self.current_ingredient_name in self.ingredient_instructions:
            # Remove old instruction if it exists
            old_pattern = f"{self.current_ingredient_name}:"
            lines = current_instructions.split('\n')
            new_lines = []
            for line in lines:
                if not line.strip().startswith(f"{self.current_ingredient_name}:"):
                    new_lines.append(line)
            current_instructions = '\n'.join(new_lines).strip()
        
        # Add new instruction to the main instructions box
        if current_instructions:
            # Add as new line
            new_instructions = f"{current_instructions}\n{formatted_instruction}"
        else:
            new_instructions = formatted_instruction
        
        # Update the main instructions text box
        self.instructions_text.delete("1.0", tk.END)
        self.instructions_text.insert("1.0", new_instructions)
        
        # Store in dict for tracking
        self.ingredient_instructions[self.current_ingredient_name] = instruction
        
        # Clear the ingredient instruction field
        self.ingredient_instruction_text.delete("1.0", tk.END)
        
        messagebox.showinfo("Saved", f"Instruction added to recipe for {self.current_ingredient_name}")
    
    def _hide_ingredient_instruction(self):
        """Hide the ingredient instruction frame."""
        if self.ingredient_instruction_frame.winfo_ismapped():
            self.ingredient_instruction_frame.pack_forget()
        self.selected_ingredient_label.config(text="")
        if hasattr(self, 'current_ingredient_name'):
            delattr(self, 'current_ingredient_name')
    
    def _save(self):
        """Save the recipe."""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Recipe title is required.")
            return
        
        # Parse ingredients
        ingredients = []
        for item in self.ingredients_listbox.get(0, tk.END):
            # Parse "amount unit name" or "amount name" format
            parts = item.split(" ", 2)
            if len(parts) >= 3:
                # Has unit: "2 cups flour"
                amount = f"{parts[0]} {parts[1]}"
                name = parts[2]
            elif len(parts) == 2:
                # No unit: "2 flour" or just "flour"
                amount = parts[0]
                name = parts[1]
            else:
                amount = "1"
                name = parts[0]
            ingredients.append(Ingredient(name=name, amount=amount))
        
        # Get instructions from the main instructions box (already formatted with ingredient instructions)
        instructions = self.instructions_text.get("1.0", tk.END).strip()
        
        # Preserve calories if editing
        calories = self.recipe.calories if self.recipe else None
        
        self.result = Recipe(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            calories=calories
        )
        
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()


class RecipeManagerGUI:
    """Main GUI application for Recipe Manager."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Recipe Manager")
        self.root.geometry("1000x700")
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        
        self.book = RecipeBook()
        self.current_recipes: List[Recipe] = []
        
        self._create_widgets()
        self._refresh_recipe_list()
    
    def _create_widgets(self):
        """Create the main GUI widgets."""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Personal Recipe Manager",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, width=250)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Buttons
        button_frame = tk.Frame(left_panel)
        button_frame.pack(fill="x", pady=(0, 15))
        
        add_btn = tk.Button(
            button_frame,
            text="+ Add Recipe",
            command=self._add_recipe,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        add_btn.pack(fill="x", pady=(0, 5))
        
        edit_btn = tk.Button(
            button_frame,
            text="Edit Recipe",
            command=self._edit_recipe,
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        edit_btn.pack(fill="x", pady=(0, 5))
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete Recipe",
            command=self._delete_recipe,
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        delete_btn.pack(fill="x", pady=(0, 15))
        
        # Search frame
        search_frame = ttk.LabelFrame(left_panel, text="Search", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame, font=("Arial", 10))
        self.search_entry.pack(fill="x", pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search())
        
        search_btn = ttk.Button(search_frame, text="Search", command=self._on_search)
        search_btn.pack(fill="x")
        
        # Filter frame
        filter_frame = ttk.LabelFrame(left_panel, text="Filter by Ingredients", padding=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Include:").pack(anchor="w")
        self.include_entry = ttk.Entry(filter_frame, font=("Arial", 9))
        self.include_entry.pack(fill="x", pady=(2, 8))
        
        ttk.Label(filter_frame, text="Exclude:").pack(anchor="w")
        self.exclude_entry = ttk.Entry(filter_frame, font=("Arial", 9))
        self.exclude_entry.pack(fill="x", pady=(2, 8))
        
        filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self._apply_filter)
        filter_btn.pack(fill="x", pady=(5, 0))
        
        clear_filter_btn = ttk.Button(filter_frame, text="Clear Filter", command=self._clear_filter)
        clear_filter_btn.pack(fill="x")
        
        # Sort frame
        sort_frame = ttk.LabelFrame(left_panel, text="Sort", padding=10)
        sort_frame.pack(fill="x")
        
        self.sort_var = tk.StringVar(value="none")
        ttk.Radiobutton(sort_frame, text="None", variable=self.sort_var, value="none", command=self._apply_sort).pack(anchor="w")
        ttk.Radiobutton(sort_frame, text="Alphabetical", variable=self.sort_var, value="alphabetical", command=self._apply_sort).pack(anchor="w")
        ttk.Radiobutton(sort_frame, text="Ingredient Count", variable=self.sort_var, value="ingredient_count", command=self._apply_sort).pack(anchor="w")
        ttk.Radiobutton(sort_frame, text="Calories", variable=self.sort_var, value="calories", command=self._apply_sort).pack(anchor="w")
        
        # Right panel - Recipe list
        right_panel = tk.Frame(main_container)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Recipe list frame
        list_frame = ttk.LabelFrame(right_panel, text="Recipes", padding=10)
        list_frame.pack(fill="both", expand=True)
        
        # Treeview for recipe list
        columns = ("Title", "Ingredients", "Calories")
        self.recipe_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=20)
        self.recipe_tree.heading("#0", text="")
        self.recipe_tree.heading("Title", text="Title")
        self.recipe_tree.heading("Ingredients", text="Ingredients")
        self.recipe_tree.heading("Calories", text="Calories")
        
        self.recipe_tree.column("#0", width=0, stretch=False)
        self.recipe_tree.column("Title", width=300)
        self.recipe_tree.column("Ingredients", width=150)
        self.recipe_tree.column("Calories", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.recipe_tree.yview)
        self.recipe_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recipe_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind click events to view recipe details
        self.recipe_tree.bind("<ButtonRelease-1>", lambda e: self._view_recipe())
        self.recipe_tree.bind("<Double-1>", lambda e: self._view_recipe())
        
        # Recipe details frame
        details_frame = ttk.LabelFrame(right_panel, text="Recipe Details", padding=10)
        details_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=10, font=("Arial", 10), wrap="word")
        self.details_text.pack(fill="both", expand=True)
        self.details_text.config(state="disabled")
    
    def _refresh_recipe_list(self):
        """Refresh the recipe list display."""
        # Clear existing items
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)
        
        # Get current recipes
        if not self.current_recipes:
            self.current_recipes = self.book.get_all_recipes()
        
        # Add recipes to tree
        for recipe in self.current_recipes:
            calories_str = f"{recipe.calories:.0f}" if recipe.calories else "N/A"
            self.recipe_tree.insert(
                "",
                tk.END,
                text="",
                values=(recipe.title, f"{recipe.get_ingredient_count()} items", calories_str),
                tags=(recipe.title,)
            )
        
        # Update count
        count = len(self.current_recipes)
        status_text = f"Showing {count} recipe{'s' if count != 1 else ''}"
        # Could add a status bar here if needed
    
    def _add_recipe(self):
        """Open dialog to add a new recipe."""
        dialog = RecipeDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.book.add_recipe(dialog.result)
            self._clear_filter()
            messagebox.showinfo("Success", f"Recipe '{dialog.result.title}' added successfully!")
    
    def _edit_recipe(self):
        """Open dialog to edit selected recipe."""
        selection = self.recipe_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recipe to edit.")
            return
        
        item = self.recipe_tree.item(selection[0])
        title = item["values"][0]
        
        recipe = self.book.get_recipe(title)
        if not recipe:
            messagebox.showerror("Error", "Recipe not found.")
            return
        
        dialog = RecipeDialog(self.root, recipe)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.book.update_recipe(title, dialog.result)
            self._clear_filter()
            messagebox.showinfo("Success", f"Recipe '{dialog.result.title}' updated successfully!")
    
    def _delete_recipe(self):
        """Delete selected recipe."""
        selection = self.recipe_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a recipe to delete.")
            return
        
        item = self.recipe_tree.item(selection[0])
        title = item["values"][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{title}'?"):
            if self.book.delete_recipe(title):
                self._clear_filter()
                messagebox.showinfo("Success", f"Recipe '{title}' deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete recipe.")
    
    def _view_recipe(self):
        """View details of selected recipe."""
        selection = self.recipe_tree.selection()
        if not selection:
            return
        
        item = self.recipe_tree.item(selection[0])
        title = item["values"][0]
        
        recipe = self.book.get_recipe(title)
        if not recipe:
            return
        
        # Format recipe details
        details = f"Recipe: {recipe.title}\n"
        details += "=" * 60 + "\n\n"
        
        if recipe.calories:
            details += f"Calories: {recipe.calories:.0f}\n\n"
        
        details += f"Ingredients ({recipe.get_ingredient_count()}):\n"
        for i, ingredient in enumerate(recipe.ingredients, 1):
            details += f"  {i}. {ingredient}\n"
        
        if recipe.instructions:
            details += f"\nInstructions:\n{recipe.instructions}\n"
        
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", details)
        self.details_text.config(state="disabled")
    
    def _on_search(self):
        """Handle search input."""
        query = self.search_entry.get().strip()
        if not query:
            self._clear_filter()
            return
        
        self.current_recipes = self.book.search_recipes(query)
        self._refresh_recipe_list()
        # Clear details if no results
        if not self.current_recipes:
            self.details_text.config(state="normal")
            self.details_text.delete("1.0", tk.END)
            self.details_text.config(state="disabled")
    
    def _apply_filter(self):
        """Apply ingredient filter."""
        include_text = self.include_entry.get().strip()
        exclude_text = self.exclude_entry.get().strip()
        
        included = [ing.strip() for ing in include_text.split(",")] if include_text else None
        excluded = [ing.strip() for ing in exclude_text.split(",")] if exclude_text else None
        
        if not included and not excluded:
            self._clear_filter()
            return
        
        self.current_recipes = self.book.filter_by_ingredients(included=included, excluded=excluded)
        self._refresh_recipe_list()
    
    def _clear_filter(self):
        """Clear all filters and show all recipes."""
        self.current_recipes = []
        self.search_entry.delete(0, tk.END)
        self.include_entry.delete(0, tk.END)
        self.exclude_entry.delete(0, tk.END)
        self.sort_var.set("none")
        self._refresh_recipe_list()
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state="disabled")
    
    def _apply_sort(self):
        """Apply sorting to recipe list."""
        sort_value = self.sort_var.get()
        
        if sort_value == "none":
            self.current_recipes = self.book.get_all_recipes()
        elif sort_value == "alphabetical":
            self.current_recipes = self.book.sort_recipes(SortBy.ALPHABETICAL)
        elif sort_value == "ingredient_count":
            self.current_recipes = self.book.sort_recipes(SortBy.INGREDIENT_COUNT, reverse=True)
        elif sort_value == "calories":
            self.current_recipes = self.book.sort_recipes(SortBy.CALORIES, reverse=True)
        
        self._refresh_recipe_list()


def run_gui():
    """Run the GUI application."""
    root = tk.Tk()
    app = RecipeManagerGUI(root)
    root.mainloop()


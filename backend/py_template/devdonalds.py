from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	recipeName = re.sub('-', ' ', recipeName)
	recipeName = re.sub('_', ' ', recipeName)
	recipeName = re.sub('[^A-Za-z ]', '', recipeName)
	recipeName = recipeName.title()
	recipeName = recipeName.strip()
	recipeName = re.sub('  ', ' ', recipeName)

	return recipeName if len(recipeName) > 0 else None


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook

def isRecipeValid(entry):
	requiredItems = entry.get('requiredItems')

	# all recipes must have requiredItems of type list
	if not requiredItems or type(requiredItems) != list:
		return False
	
	# keep track of the names of items that have been seen
	nameSet = set()

	# requiredItems is iterable because it's a list
	for item in requiredItems:
		# each item must have name as a str
		name = item.get('name')
		if not name or type(name) != str:
			return False 

		elif name in nameSet:
			# cant have repeated items in the same entry. just have one item with a higher quantity
			return False
		
		# each item must have quantity as an int
		quantity = item.get('quantity')
		if not quantity or type(quantity) != int:
			return False

		elif quantity <= 0:
			# quantity must be a positive integer
			return False

		# add to nameSet to keep track of existing names
		nameSet.add(name)

	# if all items are valid then the recipe is also valid
	return True

def isIngredientValid(entry):
	# this function is much simpler as there are fewer chekcs
	cookTime = entry.get('cookTime')
	if not cookTime or type(cookTime) != int:
		return False

	elif cookTime < 0:
		# cannot time travel
		return False

	return True

@app.route('/entry', methods=['POST'])
def create_entry():
	# HELLO! this was written with some assumptions of common sense, to hopefully avoid human error
	# from whoever is making the post request. this could include quantity having to be a +ve int only,
	# or no repeated requiredItems (just have one requiredItem with a higher quantity)

	entry = request.json

	# every entry must have a name
	entryName = entry.get('name')
	if not entryName:
		return 'name not found', 400

	elif type(entryName) != str:
		# name must be a str
		return 'name must be a str', 400

	elif entryName in cookbook:
		# don't allow adding an entry already present in the cookbook
		return 'entry already exists in cookbook', 400
	# every entry must have a type
	entryType = entry.get('type')
	if not entryType:
		return 'type not found', 400
	
	elif type(entryType) != str:
		# type must be a str
		return 'type must be a str', 400

	# depending on entryType, handle additional fields
	if entryType == 'recipe':
		if not isRecipeValid(entry):
			return 'invalid recipe', 400

	elif entryType == 'ingredient': 
		if not isIngredientValid(entry):
			return 'invalid ingredient', 400

	else:
		return 'invalid type', 400

	# add to cookbook
	cookbook[entryName] = entry
	
	return 'success', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)

# Class used to create an item:
class item:
  def __init__(self, name, category, description, value, quantity):
    self.name = name
    self.category = category
    self.description = description
    self.value = value
    self.quantity = quantity


# List of items:
candy = item("Candy", "Food", "Heals 250 health points.", 250, 5)
chocolates = item("Chocolates", "Feast", "Heals every party member for 250 health points.", 250, 2)
donut = item("Donut", "Food", "Heals 500 health points.", 500, 5)
french_fries= item("French Fries", "Feast","Heals every party member for 500 health points.", 500, 2)
hamburger = item("Hamburger", "Food", "Heals 1000 health points.", 1000, 1)
cheeseburgers = item("Cheeseburgers", "Feast", "Heals every party member for 1000 health points.", 1000, 1)
red_bull = item("Red Bull", "Beverage", "Restores 50 energy points.", 50, 5)
grenade = item("Grenade", "Explosive", "Deals 750 points of damage to all the enemies.", 750, 2)
dynamite = item("Dynamite", "Explosive", "Deals 1500 points of damage to all the enemies.", 1500, 1)

# Set of items:
items = [candy, chocolates, donut, french_fries, hamburger, cheeseburgers, red_bull, grenade, dynamite]

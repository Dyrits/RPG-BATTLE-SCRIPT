

# Class used to create a spell:
class spell:
  def __init__(self, name, cost, damage, description):
    self.name = name
    self.cost = cost
    self.damage = damage
    self.description = description


# # List of spells:
zap = spell("Zap", 10, 25, "Low damage electric spell. ZAP! Reduce your target precision by 40 percent for one attack.")
shock = spell("Shock", 15, 50, "Moderate damage electric spell.")
lightning_leech = spell("Lightning Leech", 30, 50, "Moderate damage electric spell, damaging the target and healing for the same ammount.")
thunder = spell("Thunder", 40, 100, "High damage electric spell.")
glow = spell("Glow", 10, 10, "Low damage fire spell. Reduce your target damage by 5 percent for 3 turns. Can be stacked.")
spark = spell("Spark", 30, 50, "Moderate damage fire spell. Your next strike attack will do double damage.")
torch = spell("Torch", 50, 75, "High damage fire spell.")
blaze = spell("Blaze", 50, 300, "Very high damage fire spell. You lose half of your remaining health. The target will become enraged.")
crazyness = spell("Crazyness", 50, 75, "High damage incantation. It makes the target upset.")
bloodfeast = spell("Bloodfeast", 20, 50, "Moderate damage incantation damaging the target and healing for the same ammount and making you enraged.")

# Spells set:
electricity = [zap, shock, lightning_leech, thunder]
fire = [glow, spark, torch, blaze]
controls = [zap, glow, spark]
vodoo = [crazyness, bloodfeast]

# Spells variables:
zap_enemy = False
glow_enemy = False
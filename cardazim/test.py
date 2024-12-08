from card import Card

name = "cardoz"
creator = "lidor"
riddle = "coming here a lot?"
solution = "yes!"
path = "/home/lidor/Cardazim/SMILE.jpg"
card = Card.create_from_path(name, creator, path, riddle, solution)
card.image.encrypt(card.solution)
data = card.serialize()
card2 = Card.deserialize(data)
if card2.image.decrypt(solution):
    card2.solution = solution
assert(repr(card) == repr(card2))
card2.image.save("card2.png", "png") # will show the same image as in path
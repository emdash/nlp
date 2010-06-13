from nlp import *

root = Object(None)

# test basic properties of objects

root.addAttribute(Object("being").setAttribute("living", True))

root.addAttribute(Object("thing").setAttribute("living", False))
root.addAttribute(Object("animal", root.getAttribute("being")))
root.addAttribute(Object("person", root.getAttribute("animal")))

assert root.getAttribute("person").getAttribute("living") == True

# test addObject interface

root.addObject("hardness")
root.addObject("hard", "hardness")
root.addObject("soft", "hardness")
root.addObject("plant", "being")
root.addObject("rock", "thing", hardness="hard")
root.addObject("feather", "thing", hardness="soft")

assert root.getAttribute("rock").getAttribute("living") == False
assert root.getAttribute("rock").getAttribute("hardness").name == "hard"
assert root.getAttribute("feather").getAttribute("hardness").name == "soft"

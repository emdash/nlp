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

# test spawn, clone, alias, copy

# get references to some objects
rock = root.getAttribute("rock")
hard = root.getAttribute("hard")
soft = root.getAttribute("soft")
thing = root.getAttribute("thing")

# spawn a new subclass of rock
igneous = rock.spawn("igneous")
igneous.setAttribute("hardness", soft)
assert igneous.getAttribute("hardness") == soft

# check that rocks have not become soft 
assert rock.getAttribute("hardness") == hard

# add a property to rock, and check that igneous inherits it
rock.setAttribute("heavy", True)
assert igneous.getAttribute("heavy") == True

# clone a new type of rock. rock properties shouldn't propagate to metamorphic
metamorphic = rock.clone("metamorphic")
rock.setAttribute("heavy", False)
assert metamorphic.getAttribute("heavy") == True

# but thing properties will
thing.setAttribute("foo", "bar")
assert metamorphic.getAttribute("foo") == "bar"

# create an alias of thing
thing2 = thing.alias("thing2")

# check that adding a property to thing2 also adds it to all things
thing2.setAttribute("silly", True)
assert igneous.getAttribute("silly") == True
assert rock.getAttribute("silly") == True
assert metamorphic.getAttribute("silly") == True
assert root.getAttribute("feather").getAttribute("silly") == True

# create a copy of the root object
root2 = root.copy("root2")

# check that root has copies of everything
assert root2.getAttribute("animal")
assert root2.getAttribute("feather")
assert root2.getAttribute("person")
assert root2.getAttribute("rock")

# check that child properties were copied too

assert root2.getAttribute("feather").getAttribute("hardness").name == "soft"

# check that source relationship holds at all levels of the copy
assert root2.source == root
assert root2.getAttribute("thing").source == thing
assert root2.getAttribute("rock").source == rock 
assert root2.getAttribute("rock").getAttribute("hardness").source == hard 

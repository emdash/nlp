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

# test actions

# create body as an alias of animal with thing as a parent. things that are
# specifically true about animals will also be true about bodies, but things
# true about beings in general will not necessarily be true about bodies

person = root.getAttribute("person")
animal = root.getAttribute("animal")
body = animal.alias("body")
body.setParent(thing)
body.setAttribute("legs", True)
person.setAttribute("legs", 2)

# for example, we can have dead bodies

dead_body = body.spawn("dead body").setAttribute("living", False)

# now we can give some useful semantics to the action "kill". The kill actions
# reparents an animal to the dead body object

kill = ReparentAction(dead_body)

# let's construct a nefarious situation in which alice kills bob

alice = person.spawn("alice")
bob = person.spawn("bob")

# ... both are vivacious bipedal creatures...

assert alice.isA(person) and alice.isA(animal)
assert bob.isA(person) and alice.isA(animal)
assert alice.getAttribute("living") == True
assert bob.getAttribute("living") == True
assert alice.getAttribute("legs") == 2
assert bob.getAttribute("legs") == 2

# ... but alice has a mean streak....

kill.perform(alice, bob)

# ... and bob had to suffer

assert bob.isA(dead_body) and not bob.isA(animal)
assert bob.getAttribute("living") == False
assert alice.isA(person) and not alice.isA(dead_body)
assert alice.getAttribute("living") == True

# ... there are some issues with this however. Assuming this was a nice clean
# killing, how many legs should bob have? It should still be two (we could
# define "Draw and quarty" which would change that attribute), but the
# ReparentAction sets the immediate parent, and thus bob is no longer a person
# and therefore has no person traits.

assert not bob.isA(person) and bob.getAttribute("legs") == True

# ... so let's back up.

bob = person.spawn("bob")

# and redefine kill. What we really mean here is that bob should no longer
# have "animal" in his ancestry, but should have "dead body" instead. we
# re-define the kill action and then have alice kill him again

kill = ReplaceAncestorAction(animal, dead_body)
kill.perform(alice, bob)

# bob should be dead, but bi-pedal nonetheless

assert bob.isA(dead_body)
assert not bob.getAttribute("living") == True
assert bob.getAttribute("legs") == 2

# a more interesting case is whether or not bob is still a person or animal.
# Certainly he should not be an animal now

assert not bob.isA(animal)

# but he should still be a person...

assert bob.isA(person)

# things that are true about people are still true about bob

person.setAttribute("hands", 2)
assert bob.getAttribute("hands") == 2

# except that kill as we've thus defined it is really just to die. alice's
# role in this isn't really recorded. Let's re-define kill yet again to record
# the fact that bob now has a killer, and alice a new victim. ideally victims
# would be a set or a sequence to reflect the fact that alice could
# potentially kill more than one person, but we'll save that for another day.

die = kill
die.name = "die"

kill = CompoundAction
    die, 
    PatientAttributeChange("killer"),
    AgentAttributeChange("victim"))

# reincarnate bob again

bob = person.spawn("bob")

kill.perform(alice, bob)

assert bob.getAttribute("living") == False
assert bob.getAttribute("killer") == alice
assert alice.getAttribute("victim") == bob

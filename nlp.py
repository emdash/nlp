# I will begin at the beginning.

class Clause(object):

    """In an abstract sense, a clause is when an agent performs an action on a
    patient. Agent and patients are Objects. I don't know yet whether an
    Action is a type of object or not."""

    def __init__(self, agent, patient, action):
        self.agent = agent.
        self.patient = patient
        self.action = action

class Object(object):

    """An object is a reference to something in a space. Objects are also
    collections of attributes. Objects can inherit attributes from parent
    objects."""

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.attributes = {}

    def getAttribute(self, name):
        if name in self.attributes:
            return self.attributes[name]
        if self.parent:
            return self.parent.getAttribute(self, name)
        return KeyError("object %s does not have attribute %s" % 
            (self.name, name)

class World(Object):

    """A world is the root object of discourse."""

    pass

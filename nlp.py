# I will begin at the beginning.

class Statement(object):

    """An instance of an action"""

    def __init__(self, agent, patient, action):
        self.agent = agent
        self.patient = patient
        self.action = action

class Action(object):
    """An action is a transformation of an object. An action is defined in
    terms of an agent, a patient, and one or more attributes."""

    def __init__(self, agent, patient):
        self.agent = agent
        self.patient = patient

    def perform(self):
        raise NotImplementedError()

class PropertyChangeAction(object):

    """Changes property p on its patient to value v"""

    def __init__(self, p, v, *args):
        Action.__init__(*args)
        self.propertyname = p
        self.value = v

    def perform(self):
        self.patient.setAttribute(self.propertyname, self.value)

class ReparentAction(Action):

    """Sets the parent of patient to p"""

    def __init__(self, p, *args):
        self.new_parent = p

    def perform(self):
        self.patient.setParent(self.new_parent)

class Object(object):

    """An object is a reference to something in a space. Objects are also
    collections of attributes. Objects can inherit attributes from parent
    objects."""

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.attributes = {}

    def setParent(self, parent):
        self.parent = parent

    def getAttribute(self, name):
        if name in self.attributes:
            return self.attributes[name]
        if self.parent:
            return self.parent.getAttribute(self, name)
        return KeyError("object %s does not have attribute %s" % 
            (self.name, name)

    def setAttribute(self, name, value):
        if not (value is None):
            self.attributes[name] = value
        else:
            del self.attributes[name]

    def __str__(self):
        return self.name

class World(Object):

    """A world is the root object of discourse."""

    pass

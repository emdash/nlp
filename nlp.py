# I will begin at the beginning.

class Statement(object):

    """An instance of an action"""

    def __init__(self, agent, patient, action):
        self.agent = agent
        self.patient = patient
        self.action = action

    def Apply(self):
        action.perform(self.agent, self.patient)

class Action(object):
    """An action is a transformation of an object. An action is defined in
    terms of an agent, a patient, and one or more attributes."""

    def perform(self, agent, patient):
        raise NotImplementedError()

class PropertyChangeAction(Action):

    """Changes property p on its patient to value v"""

    def __init__(self, p, v=None):
        self.propertyname = p
        self.value = v

class PatientAttributeChange(PropertyChangeAction):

    """set's named patient attribute to agent"""

    def perform(self, agent, patient):
        value = self.value
        if value is None:
            value = agent
        patient.setAttribute(self.propertyname, value)

class AgentAttributeChange(PropertyChangeAction):

    """set's agent attribute to patient"""

    def perform(self, agent, patient):
        value = self.value
        if value is None:
            value = patient
        agent.setAttribute(self.propertyname, value)

class ReparentAction(Action):

    """Sets the parent of patient to p"""

    def __init__(self, p):
        self.new_parent = p

    def perform(self, agent, patient):
        patient.setParent(self.new_parent)

class ReplaceAncestorAction(Action):

    """Replaces an arbitrary ancestor with a given one."""

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def perform(self, agent, patient):
        patient.replaceAncestor(self.old, self.new)

class CompoundAction(Action):

    """Group a set of actions"""

    def __init__(self, *actions):
        self.actions = actions

    def perform(self, agent, patient):
        for action in self.actions:
            action.perform(agent, patient)

class Swap(Action):

    """Swap agent and patient in child action"""

    def __init__(self, action):
        self.child = action

    def perform(self, agent, patient):
        self.child.perform(patient, agent)

class Object(object):

    """An object is a reference to something in a space. Objects are also
    collections of attributes. Objects can inherit attributes from parent
    objects."""

    def __init__(self, name, parent=None, source=None):
        self.name = name
        self.parent = parent
        self.source = source
        self.attributes = {}

    def setParent(self, parent):
        self.parent = parent

    def replaceAncestor(self, old, new):
        # This isn't as straight-forward as it would at first seem. We can't
        # simply swap the original parent for the new one where it appears in
        # the hierarchy, because it would affect other objects as well.

        # we walk the tree and construct a new chain of parents. the ability
        # to alias objects allows this new chain of parents that are identical
        # to the originals, except for their parent pointers

        # TODO: memory optimization. memoize or otherwise cache so that we
        # don't duplicate entire chains of parents when a suitable one already
        # exists

        cur = self.parent
        if cur is None:
            raise Exception("%s has no parent", patient)

        first = cur.alias()
        prev = first

        while cur != old:
            if cur is None:
                raise Exception("%s is not an ancestor of %s", self.old, patient)
            alias = cur.alias()
            if prev:
                prev.setParent(alias)
            prev = alias
            cur = cur.parent

        prev.setParent(new)
        self.setParent(first)

    def getAttribute(self, name):
        if name in self.attributes:
            return self.attributes[name]
        if self.parent:
            return self.parent.getAttribute(name)
        raise KeyError("object %s does not have attribute %s" % 
            (self.name, name))

    def setAttribute(self, name, value):
        if not (value is None):
            self.attributes[name] = value
        else:
            del self.attributes[name]
        return self

    def addAttribute(self, value):
        return self.setAttribute(value.name, value)

    def addObject(self, name, parent=None, **properties):
        try:
            parent = self.getAttribute(parent)
        except KeyError:
            parent = None

        obj = Object(name, parent, self)

        for p, v in properties.iteritems():
            if type(v) is str:
                obj.setAttribute(p, self.getAttribute(v))

        return self.addAttribute(obj)

    def spawn(self, name):
        """Return a new derived object (parent is self)"""
        if not name:
            name = self.name
        return Object(name, self, self)

    def clone(self, name=None):
        """Return a shallow copy"""
        if not name:
            name = self.name
        ret = Object(name, self.parent, self)
        for p, v in self.attributes.iteritems():
            ret.setAttribute(p, v)
        return ret

    def alias(self, name=None):
        """Returns a fully-syncrhonized copy of object. Changes to the
        attributes of either object affect both objects."""
        if not name:
            name = self.name
        ret = Object(name, self.parent, self)
        ret.attributes = self.attributes
        return ret

    def copy(self, name=None):
        """Returns a deep copy of object. All object attributes are dupliated
        in the new child"""
        if not name:
            name = self.name
        ret = Object(name, self.parent, self)
        for p, v in self.attributes.iteritems():
            if isinstance(v, Object):
                v = v.copy()
            ret.setAttribute(p, v)
        return ret

    def isA(self, category):
        if self.parent:
            if self.parent == category:
                return True
            else:
                return self.parent.isA(category)
        return False

    def has(self, quality):
        try:
            return bool(self.getAttribute(quality))
        except KeyError:
            return False

    def __eq__(self, other):
        # we compare based name, attribute. this should allow aliases with
        # identical names to appear to be the same object
        return (self.name == other.name) and (self.attributes is 
            other.attributes)

    def __str__(self):
        return self.name

    def dump(self):
        cur = self
        chain = "<"
        while cur:
            chain += "->" + str(cur)
            cur = cur.parent
        chain += ">"
        chain += "\n" + repr(self.attributes)
        return chain

from nlp import *
import sys

"""Implements a simple NLP processor using the NLP objects"""

KEYWORD = 0
OBJECT = 1
ACTION = 2
UNDEFINED = 3

class Processor(object):

    done = False
    HISTFILE="history.dat"

    prompt = "> "

    keywords = ["is", "to", "\'", "set"]

    def __init__(self):
        self.actions = {}
        self.objects = {"object" : Object("object")}

        self.dispatch_table = {
            (UNDEFINED, "is", OBJECT) : self.CreateObject,
            ("to", "\'", UNDEFINED, "is", "to", "set", UNDEFINED, "to", 
                UNDEFINED) : self.CreateAction,
            (OBJECT, ACTION, OBJECT) : self.PerfomAction,
            ("is", OBJECT, OBJECT) : self.QueryAncestor,
            (UNDEFINED, "of", OBJECT, "is", OBJECT) : self.SetProperty,
            ("what", UNDEFINED, "of", OBJECT) : self.QueryProperty,
        }

        self.history = []
        self.loadHistory()

    def printloop(self):
        while not self.done:
            sys.stdout.write(self.prompt)
            statement = sys.stdin.readline()
            print self.process(statement)
        self.saveHistory()

    def loadHistory(self):
        try:
            history = open(self.HISTFILE, "r").readlines()
            for line in history:
                self.process(line)
        except IOError:
            print "error loading history"

    def saveHistory(self):
        try:
            output = open(self.HISTFILE, "w")
            for line in self.history:
                print >> output, line
            output.close()
        except IOError:
            print "couldn't save history"

    def match(self, w):
        if w in self.keywords:
            return w
        elif w in self.actions:
            return ACTION
        elif w in self.objects:
            return OBJECT
        return UNDEFINED

    def process(self, statement):
        statement = statement.strip()

        if statement == 'quit':
            self.done = True
            return "bye"

        words = [w.strip() for w in statement.split()]
        tokens = [self.match(w) for w in words]

        return self.select(statement, words, tuple(tokens))

    def select(self, raw, words, tokens):
        print words, tokens
        dispatch = self.dispatch_table.get(tokens, None)
        if not dispatch:
            return "invalid command"
        return dispatch(raw, words)

    def CreateObject(self, raw, words):
        name = words[0]
        parent = self.objects[words[2]]
        self.objects[name] = parent.spawn(name)
        self.history.append(raw)
        return "created %s." % name

    def CreateAction(self, raw, words):
        pass

    def PerfomAction(self, raw, words):
        pass

    def QueryAncestor(self, raw, words):
        target = self.objects[words[1]]
        ancestor = self.objects[words[2]]
        if target.isA(ancestor):
            return "Yes."
        return "No."

    def SetProperty(self, raw, words):
        propname = words[0]
        target = self.objects[words[2]]
        value = self.objects[words[4]]
        target.setAttribute(propname, value)
        history.append(raw)
        return "okay."

    def QueryProperty(self, raw, words):
        propname = words[1]
        target = self.objects[words[4]]
        return target.getAttribute(propname)

if __name__ == '__main__':
    Processor().printloop()



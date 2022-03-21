
class Variable():
    name = ""
    value = None

class Constraints():


    def add(self,a,b):
        if a not in self.relations:
            self.relations[a] = self.counter
            self.counter += 1
        if type(b) != str:
            if self.relations[a] in self.values:
                assert self.values[self.relations[a]] == b
            self.values[self.relations[a]] = b
        else:
            if b not in self.relations:
                self.relations[b] = self.counter
                self.counter += 1
            #merge
         

            variableSets[relations[a]]
        
    def find(self,a):
        if a in self.relations:
            return self.relations[a]
        return None

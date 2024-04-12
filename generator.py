from clingo import Control, ast
from clingo.ast import ProgramBuilder, parse_string
from redirect import redirect_stdout_stderr
from random import random

import os


class Forge:
    def __init__(self, code):
        self.source_code = code

        self.init_control(self.source_code)

        self.relevant_atoms = []
        for signature in self.prog.symbolic_atoms.signatures:
            if signature[0] not in self.relevant_atoms:
                self.relevant_atoms.append(signature[0])
        self.relevant_atoms.sort()

        output = "\n"
        for atom in self.relevant_atoms:
            # output += "#external "+atom+ ".\n"
            output += "1{%s;-%s}1.\n" % (atom, atom)
        self.forging_code = output + self.source_code

        self.init_control(self.forging_code)

    def init_control(self, code):

        self.answer_sets = []
        self.prog = Control()
        self.prog.configuration.solve.models = 0  # to obtain all answer sets
        with redirect_stdout_stderr():
            output = self.parse_program(code)

        with open('stderr.log', 'r') as f:
            self.print_console(f.read())
        os.remove("stdout.log")
        os.remove("stderr.log")
        return output

    def parse_program(self, code):

        try: # to catch RuntimeError for syntaxic errors
            with ProgramBuilder(self.prog) as builder:
                parse_string(code, lambda statement: builder.add(statement))
            self.prog.ground([("base", [])])
            return True
        except RuntimeError:
            return False

    def run_inference(self):
        self.prog.solve(on_model=self.model_update)

    def print_code(self):
        print("============= CODE =================%s" % (self.source_code[:-1]))

    def print_relevant_atoms(self):
        print("============= RELEVANT ATOMS =======")
        output = ""
        for atom in self.relevant_atoms: # .sort():
            output += atom+", "
        print(output[:-2])

    def print_console(self, message):
        message = str(message)
        if len(message) == 0:
            return
        message = message.replace('<string>:','Line ') # took this out from clingo messages for better readibility
        print("============= CONSOLE ==============")
        print(message)

    def print_outcome(self):
        output = "number of answer sets: " + str(len(self.answer_sets)) + "\n"
        for i, answer_set in enumerate(self.answer_sets):
            output += "answer set "+ str(i+1) + ": "
            for atom in answer_set:
                output += atom + " "
            output = output[:-1] + "\n"
        output = output[:-1]
        print("============= OUTPUT ===============")
        print(output)

    def forge_data_set(self, n_rows=100, uniform=True, n_hidden=0):
        print("============= FORGE DATASET ========")

        n_templates = len(self.answer_sets)
        print("n. templates: %d" % (n_templates))

        p_templates = []
        threshold = 0
        for i in range(n_templates-1):
            if uniform:
                threshold += 1/n_templates
            else:
                ### PLEASE CHANGE ####
                r = random()
                if (r > (1/n_templates)*5): # cap for more diversity
                    r = (1/n_templates)*5
                threshold += r * (1 - threshold)
                ######################

            p_templates.append((threshold, self.answer_sets[i]))
        p_templates.append((1, self.answer_sets[n_templates-1]))

        if uniform:
            print("uniform distribution")
        else:
            print("randomly generated distribution")

        print("template: probability threshold")
        for p_template in p_templates:
            print("    %s: %.02f " % (str(p_template[1]), p_template[0]))

        hidden_atoms = []
        if n_hidden == 0:
            print("no hidden variables")
        else:
            candidates = []
            for atom in self.relevant_atoms:
                candidates.append(atom)
            for i in range(n_hidden):
                pos = round(random()*(len(candidates)-1))
                hidden_atoms.append(candidates[pos])
                candidates.remove(candidates[pos])
            print("hidden variables: "+str(hidden_atoms))

        print("n. objects: " + str(n_rows))

        print("===================================")
        print("generate a complete dataset as CSV table...")
        output = ""
        for atom in self.relevant_atoms:
            output += atom +";"
        output+="\n"
        for i in range(n_rows):
            r = random()
            for p_template in p_templates:
                if r < p_template[0]:
                    for atom in self.relevant_atoms:
                        if atom in p_template[1]:
                            output += "1;"
                        else:
                            output += "0;"
                    output+="\n"
                    break

        f = open("dataset_complete.csv", "w")
        f.write(output)
        f.close()
        print("dataset_complete.csv saved")
        print("-----------------------------------")
            
        if n_hidden > 0:
            print("generate another dataset with hidden rows as CSV table...")
            output = ""
            for atom in self.relevant_atoms:
                if atom not in hidden_atoms:
                    output += atom +";"
            output+="\n"
            for i in range(n_rows):
                r = random()
                for p_template in p_templates:
                    if r < p_template[0]:
                        for atom in self.relevant_atoms:
                            if atom not in hidden_atoms:
                                if atom in p_template[1]:
                                    output += "1;"
                                else:
                                    output += "0;"
                        output+="\n"
                        break
                        
            f = open("dataset_partial.csv", "w")
            f.write(output)
            f.close()
            print("dataset_partial.csv saved")
        print("===================================")

    def model_update(self, model):
        """mark place after clingo output"""
        answer_set = []
        for atom in model.symbols(shown=True):
            answer_set.append(str(atom))
        self.answer_sets.append(answer_set)


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    code = """
a :- b, -c, d.
a :- e, f.
a :- g.
-d :- e.
f :- a.
g :- -b, d, -c. 
b :- a, f, e.
c :- g.
-b :- e, -d.
d :- f, a.
"""
    forge = Forge(code)
    forge.print_code()
    forge.print_relevant_atoms()
    forge.run_inference()
    forge.print_outcome()
    forge.forge_data_set(uniform=False, n_rows=1000, n_hidden=3)

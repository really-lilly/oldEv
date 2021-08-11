import os
import cleanUpMethods as clean

source_dir = "/home/hellsbells/Desktop/isMassConserved"
true_dir = "/home/hellsbells/Desktop/isMassConserved-yes"
false_dir = "/home/hellsbells/Desktop/isMassConserved-no"

for file in os.listdir(source_dir):
    os.chdir(source_dir)
    ant = clean.loadAntimonyText(file)
    full_ant = clean.loadAntimonyText_noLines(file)
    for line in ant:
        if '->' in line and not line.startswith('#'):
            line = line.replace(' ', '')  # strip spaces
            # separate products and reactants by splitting at ->
            reaction = line.split('->')
            rxnType = ''
            # Get reaction type by number of reactants and products
            if '+' in reaction[0]:
                rxnType += 'bi-'
            else:
                rxnType += 'uni-'
            # Now we do the same thing for the product half
            if len(reaction) > 1:
                if '+' in reaction[1]:
                    rxnType += 'bi'
                else:
                    rxnType += 'uni'

            if rxnType == 'uni-bi':
                # Separate products and reactant
                products = reaction[1].split('+')
                reactant = reaction[0]
                if reactant == products[0] or reactant == products[1]:
                    # mass is not conserved, write to dir
                    os.chdir(false_dir)
                    with open(file, "w") as f:
                        f.write(full_ant)
                        f.close()
                    # If we find a reaction that violates mass conservation, we can move to the next model
                    break
            elif rxnType == 'bi-uni':
                reactants = reaction[0].split('+')
                product = reaction[1]
                if product == reactants[0] or product == reactants[1]:
                    # mass is not conserved, write to dir
                    os.chdir(false_dir)
                    with open(file, "w") as f:
                        f.write(full_ant)
                        f.close()
                    # If we find a reaction that violates mass conservation, we can move to the next model
                    break
        # If we've gone through every reaction without breaking out of the loop, then mass is conserved.
        os.chdir(true_dir)
        with open(file, "w") as f:
            f.write(full_ant)
            f.close()


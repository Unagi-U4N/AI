import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Create a dictionary to store the probabilities
    probabilities = {
        person: {}
        for person in people
    }

    for person in one_gene:
        probabilities[person]["1 gene"] = 0

    for person in two_genes:
        probabilities[person]["2 genes"] = 0

    for person in people:
        if person not in one_gene and person not in two_genes:
            probabilities[person]["no gene"] = 0

    for person in have_trait:
        probabilities[person]["trait"] = 0

    for person in people:
        if person not in have_trait:
            probabilities[person]["no trait"] = 0

    # Calculate the probability of having the gene for each person
    def gene_probability(person):

        # Get the parents of the person
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If the person has no parents, use the unconditional probability
        if father is None and mother is None:
            if person in one_gene:
                probabilities[person]["1 gene"] += PROBS["gene"][1]
            elif person in two_genes:
                probabilities[person]["2 genes"] += PROBS["gene"][2]
            else:
                probabilities[person]["no gene"] += PROBS["gene"][0]

        else:
            # If the person has parents, calculate the probability of having the gene
            if person in one_gene:
                probabilities[person]["1 gene"] += gene_from_parents(1, mother, father)
            elif person in two_genes:
                probabilities[person]["2 genes"] += gene_from_parents(2, mother, father)
            else:
                probabilities[person]["no gene"] += gene_from_parents(0, mother, father)
            
    def gene_from_parents(gene_num, mother, father):
        # Get the classification of the parents
        mother_gene_num = get_gene_num(mother)
        father_gene_num = get_gene_num(father)

        # If the person has no gene
        if gene_num == 0:

            # If both the parents have no gene
            if mother_gene_num == 0 and father_gene_num == 0:
                return (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
            
            # If one of the parents has one gene
            elif (mother_gene_num == 1 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 1):
                return (0.5 * (1 - PROBS["mutation"]))
            
            # If one of the parents has two genes
            elif (mother_gene_num == 2 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 2):
                return (PROBS["mutation"] * (1 - PROBS["mutation"]))
            
            # If one of the parents has two genes and the other has one gene
            elif (mother_gene_num == 2 and father_gene_num == 1) or (mother_gene_num == 1 and father_gene_num == 2):
                return (0.5 * PROBS["mutation"])
            
            # If both the parents have one gene
            elif (mother_gene_num == 1 and father_gene_num == 1):
                return (0.5 * 0.5)  

            # If both the parents have two genes  
            else:
                return (PROBS["mutation"] * PROBS["mutation"])
            
        # If the person has one gene
        elif gene_num == 1:

            # If both the parents have no gene
            if mother_gene_num == 0 and father_gene_num == 0:
                return (1 - PROBS["mutation"]) * PROBS["mutation"] + PROBS["mutation"] * (1 - PROBS["mutation"])
            
            # If one of the parents has one gene
            elif (mother_gene_num == 1 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 1):
                return (0.5 * (1 - PROBS["mutation"])) + (0.5 * PROBS["mutation"])
            
            # If one of the parents has two genes
            elif (mother_gene_num == 2 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 2):
                return ((1 - PROBS["mutation"]) * (1 - PROBS["mutation"]) + PROBS["mutation"] * PROBS["mutation"])
            
            # If one of the parents has two genes and the other has one gene
            elif (mother_gene_num == 2 and father_gene_num == 1) or (mother_gene_num == 1 and father_gene_num == 2):
                return (0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"]))
            
            # If both the parents have one gene
            elif (mother_gene_num == 1 and father_gene_num == 1):
                return (0.5 * 0.5 + 0.5 * 0.5)
            
            # If both the parents have two genes
            else:
                return (PROBS["mutation"] * (1 - PROBS["mutation"]) + (1 - PROBS["mutation"]) * PROBS["mutation"])

        # If the person has two genes
        else:

            # If both the parents have no gene
            if mother_gene_num == 0 and father_gene_num == 0:
                return PROBS["mutation"] * PROBS["mutation"]
            
            # If one of the parents has one gene
            elif (mother_gene_num == 1 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 1):
                return (0.5 * PROBS["mutation"])
            
            # If one of the parents has two genes
            elif (mother_gene_num == 2 and father_gene_num == 0) or (mother_gene_num == 0 and father_gene_num == 2):
                return (PROBS["mutation"] * (1 - PROBS["mutation"]))
            
            # If one of the parents has two genes and the other has one gene
            elif (mother_gene_num == 2 and father_gene_num == 1) or (mother_gene_num == 1 and father_gene_num == 2):
                return (0.5 * (1 - PROBS["mutation"]))
            
            # If both the parents have one gene
            elif (mother_gene_num == 1 and father_gene_num == 1):
                return (0.5 * 0.5)
            
            # If both the parents have two genes
            else:
                return (1 - PROBS["mutation"]) * (1 - PROBS["mutation"])
            

    # Get the number of genes for a person
    def get_gene_num(person):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0
        
    # Calculate the probability of having the trait for each person    
    def trait_probability(person):

        # If the person has one gene
        if person in one_gene:
            if person in have_trait:
                probabilities[person]["trait"] += PROBS["trait"][1][True]
            else:
                probabilities[person]["no trait"] += PROBS["trait"][1][False]

        # If the person has two genes
        elif person in two_genes:
            if person in have_trait:
                probabilities[person]["trait"] += PROBS["trait"][2][True]
            else:
                probabilities[person]["no trait"] += PROBS["trait"][2][False]
        
        # If the person has no gene
        else:
            if person in have_trait:
                probabilities[person]["trait"] += PROBS["trait"][0][True]
            else:
                probabilities[person]["no trait"] += PROBS["trait"][0][False]
    
    # Calculate the probability of having the gene and the trait for each person
    for person in people:
        gene_probability(person)
        trait_probability(person)

    joint_probability = 1

    # For each person, each field, multiply the all probabilities
    for person in people:
        for field in probabilities[person]:
            joint_probability *= probabilities[person][field]
    
    return joint_probability
        
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:

        # Update the probabilities
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        for field in probabilities[person]:

            # Normalize the probabilities
            total = sum(probabilities[person][field].values())

            # DIvide each value by the total to nromalize the probabilities
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total

    # raise NotImplementedError


if __name__ == "__main__":
    main()

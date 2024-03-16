import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to otpython pagerank.py corpusher pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # Do not include links to self
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probability_distribution = dict()

    # Check if the page is part of the corpus
    if page not in corpus:
        raise ValueError("Page not in corpus")

    # If the page has no outgoing links, return a probability distribution that chooses randomly among all pages with equal probability.
    if len(corpus[page]) == 0:
        for link in corpus:
            probability_distribution[link] = 1/ len(corpus)
        return probability_distribution
    
    # If the page has outgoing links, return a probability distribution that chooses randomly among all pages linked to by the given page with probability damping_factor, and with probability 1 - damping_factor, chooses randomly among all pages in the corpus.
    if len(corpus[page]) != 0:
        for link in corpus:
            probability_distribution[link] = (1 - damping_factor) / len(corpus)

        for link in corpus[page]:
            probability_distribution[link] += damping_factor / len(corpus[page])
    return probability_distribution
            
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create an empty dictionary of the number of times a page is opened
    times = {
        page: 0 for page in corpus
    }

    # Iterate n times
    for i in range(n):

        # If it is the first loop, choose a page at random
        if i == 0:
            page = random.choice(list(corpus.keys()))

        else:
            # Create a probability distribution
            probability_distribution = transition_model(corpus, page, damping_factor)

            """
            The random.choices() function is used to make a weighted random choice. 
            It takes three arguments: a list of elements to choose from, a list of
            weights corresponding to each element, and an integer k representing
            how many elements to choose. In this case, it's choosing one element
            (a page) from the list of keys (pages), with the probability of each
            page being chosen determined by the corresponding value in the
            list of values (probabilities).
            """

            page = random.choices(list(probability_distribution.keys()),
                                  list(probability_distribution.values()), k=1)[0]

        # Update the number of times the page has been opened
        times[page] += 1

    # Create a dictionary of the estimated PageRank value for each page
    pagerank = {
        page: times[page] / n for page in corpus
    }

    # for page in times:
    #     print(f"{page}: {times[page]}")

    return pagerank
   
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):

    limit = 0.001

    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create a dictionary of the number of pages in the corpus
    N = len(corpus)
    pagerank = {
        page: 1 / N for page in corpus
    }

    new_pagerank = pagerank.copy()

    # Iterate through all the pages in corpus
    while True:
        
        for page in corpus:

            # If the page has no links at all, consider all the pages in the corpus
            if len(corpus[page]) == 0:
                corpus[page] = set(corpus.keys())

            # Get a set of all the pages i, that link to the current page
            linked = set()
            for i in corpus:
                if page in corpus[i]:
                    linked.add(i)

            # If the page has no links to it, only consider the 0.15 probability
            if len(linked) == 0:
                pagerank[page] = (1 - damping_factor) / N
            
            # If the page has links to it, calculate the probability
            else:
                sum = 0

                # d SUM (PR(i) / NumLinks(i)) for i in linked
                for i in linked:
                    sum += pagerank[i] / len(corpus[i])
                new_pagerank[page] = (1 - damping_factor) / N + damping_factor * sum 

        for page in corpus:
            
            # If the difference between all the values in the new and old pagerank is less than the limit, break
            if all(abs(new_pagerank[page] - pagerank[page]) < limit for page in corpus):
                return pagerank
            
            else:
                pagerank[page] = new_pagerank[page]
        
    raise NotImplementedError


if __name__ == "__main__":
    main()
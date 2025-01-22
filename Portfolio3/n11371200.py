'''

IFN646 - Portfolio 3

- You must rename this file to be your student ID.
    For example: n123456789.py

- Your solution should not write to the output stream (do not use 'print').

- Update INPUT_GENOME and INPUT_GUIDES to reflect your allocated datasets, as per Blackboard.
    
- Do not modify the name or arguments of the declared functions. 
    
- You must modify:
    - TaskA(..)
    - TaskB(..)
    - TaskC(..)
    - SingleScore(..)
    
- Your code is subject to plagiarism checking.    

'''

import re

# Update these values
INPUT_GENOME = r"E_coli.fa"
INPUT_GUIDES = r"E_coli.fa-00-guides.txt"

# Do not change or delete.
_TASK_A_CACHE = []


def rc(dna):
    complements = str.maketrans('ACGT', 'TGCA')
    rcseq = dna.translate(complements)[::-1]
    return rcseq


def TaskA(F_GENOME):
    """
    Write your solution for Task A in this method.

    Parameters:
        - DO NOT modify the input parameters to this function
        - F_GENOME: A path to the file containing the FASTA-formatted genome

    Returns:
        - A single dimension list containing discovered off-targets

    """
    global _TASK_A_CACHE

    if len(_TASK_A_CACHE) > 0:
        return _TASK_A_CACHE
    else:
        results = []

        # Add your code here
        # double-stranded, we also have to look in the complementary sequence
        raw_genome = []
        with open(F_GENOME, 'r') as fp:
            next(fp)
            # remove the empty space
            for line in fp.readlines():
                raw_genome.append(line)
        concatenated_genome = ''.join(raw_genome)
        reverse_genome = rc(concatenated_genome)
        candidateTarget = []
        for match in re.findall('[ATCG]{21}GG', concatenated_genome):
            candidateTarget.append(match[:20])
        for match in re.findall('[ATCG]{21}GG', reverse_genome):
            candidateTarget.append(match[:20])

        results = candidateTarget
        # Cache the results to reduce run-time later
        _TASK_A_CACHE = results

        return results


def TaskB(F_GENOME, F_GUIDES):
    """
    Write your solution for Task B in this method.

    You will need to utilise your solution to Task A in order to complete Task B

    Parameters:
        - DO NOT modify the input parameters to this function
        - F_GENOME: A path to the file containing the FASTA-formatted genome
        - F_GUIDES: A path to the file containing line-separated guides

    Returns:
        - A list of lists
            - The sub-lists contain the following items (order is important):
                1. The guide sequence
                2. The number of identical off-target sites
                2. The number of off-target sites that contained one mismatch
                3. The number of off-target sites that contained two mismatches
                4. The number of off-target sites that contained three mismatches
                5. The number of off-target sites that contained four mismatches

    """
    results = []

    offtargets = TaskA(F_GENOME)

    # Add your code here
    with open(F_GUIDES, 'r') as fp:
        next(fp)
        # for each guide in guids
        for line in fp.readlines():
            guide_sequence = line.strip()[:23]
            # we then look for the complementary sequence amongst the targets
            target_sequence = guide_sequence[:20]
            result = [guide_sequence, 0, 0, 0, 0, 0]
            # compare to each offtarget
            for candidate in offtargets:
                different = 0
                if target_sequence.__eq__(candidate):
                    # if equal, add and go to next
                    result[1] += 1
                else:
                    # look for the number of difference
                    for i in range(len(candidate)):
                        if candidate[i] != target_sequence[i]:
                            different += 1
                            if different == 5:
                                break
                    if different != 5:
                        result[different + 1] += 1
            results.append(result)
    return results


def TaskC(F_GENOME, F_GUIDES):
    """
    Write your solution for Task C in this method.

    You will need to utilise your solution to Task A in order to complete Task C

    Parameters:
        - DO NOT modify the input parameters to this function
        - F_GENOME: A path to the file containing the FASTA-formatted genome
        - F_GUIDES: A path to the file containing line-separated guides

    Returns:
        - A Python list of lists
            - The sub-lists contain the following items (order is important):
                1. The guide sequence
                2. The Zhang specificity score

    """
    results = []

    offtargets = TaskA(F_GENOME)

    # Add your code here
    with open(F_GUIDES, 'r') as fp:
         next(fp)
    # Add your code here
         for line in fp.readlines():
            guide_sequence = line.strip()[:23]
            target_sequence =  guide_sequence[:20]
            total_score = 0
            result =[guide_sequence]
          
            for target in offtargets:
                #if they are identical
                if(target != target_sequence):
                    mismatch_array = []
                    pblocalisation = 0
                    #compare each base
                    while(pblocalisation <len(target_sequence) and len(mismatch_array) <5):
                        if(target_sequence[pblocalisation] != target[pblocalisation]):
                            mismatch_array.append(pblocalisation)
                        pblocalisation += 1
            #calculate the single score for the target
                if(len(mismatch_array)<5 and len(mismatch_array)>0):
                    total_score += SingleScore(mismatch_array)
            ##calculate the score for the guide
            total_score= 100/(100+total_score)*100
            result.append(total_score)
            results.append(result)


    return results


def SingleScore(mismatch_array):
    """
    Calculate the local Zhang score

    The formula was given in the week 7 lecture.
    It is the product of three terms.

    We are giving the code for the second term.
    You will need to complete the 1st and 3rd terms.

    Parameters:
        - A list of positions where mismatches exist between the candidate guide
            and off-target site. Positions are zero-indexed.

    Returns:
        - The local score

    """

    i = 0
    T1 = 1.0
    T2 = 0.0
    T3 = 0.0
    d = 0.0
    score = 0
    W = [
        0.0, 0.0, 0.014, 0.0, 0.0,
        0.395, 0.317, 0.0, 0.389, 0.079,
        0.445, 0.508, 0.613, 0.851, 0.732,
        0.828, 0.615, 0.804, 0.685, 0.583
    ]

    length = len(mismatch_array)

    ### 1st term
    # Add your code here
    for i in range(length):
        T1 = T1 * (1 - W[mismatch_array[i]])

    ### 2nd term
    if (length == 1):
        d = 19.0
    else:
        for i in range(length - 1):
            d += mismatch_array[i + 1] - mismatch_array[i]
        d = d / (length - 1)
    T2 = 1.0 / ((19.0 - d) / 19.0 * 4.0 + 1)

    ### 3rd term
    # Add your code here
    T3 = 1 / length**2

    ### Total score
    score = T1 * T2 * T3 * 100

    return score


if __name__ == '__main__':
    TaskA(INPUT_GENOME)
    TaskB(INPUT_GENOME, INPUT_GUIDES)
    TaskC(INPUT_GENOME, INPUT_GUIDES)

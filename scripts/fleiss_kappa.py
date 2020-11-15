#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Receive a CSV file having votes (in categories) for a sequence of subjects (papers)
using a number of raters (students):

        | rater 1 | rater 2 | rater 3 |
paper 1 |  cat A  |  cat B  |  cat A  |
paper 1 |  cat B  |  cat B  |  cat B  |

and computes the Fleiss Kappa agreement between annotators. Here, we implement two
types of Fleiss Kappa. The first considers all categories as unique. The second 
considers only two categories (Accept and Reject). The former is represented by
the letter 'A', and the latter is represented by any number. Thus, categories that
are represented by numbers, such as '1', '2', '3' are considered all as Reject.

To run this script using multiple categories, one can simply call:

```
$ python fleiss_kappa.py round_2_scores.csv
```

In order to run considering a binary elements, one can pass the `-b` or `--binary` 
argument to the script, as follows:

```
$ python fleiss_kappa.py -b round_2_scores.csv
```
"""
import csv
import argparse
from os.path import join
from collections import Counter
import numpy as np


def fleiss_kappa(M):
    """
    Compute the agreement between `r` rater of `N` subjects (e.g., papers)
    in `k` categories (e.g., criterias). For example, we have 6 students voting
    between 7 options ('A' to '6' as shown in the table below) for 10 papers.
    Each student assign a vote to only one category in each paper. Thus, the
    sum of all elements of the row must be equal to the number of students.
    The matrix representing these quantities is named matrix `M`, and is illustred
    below:

            || 'A' | '1' | '2' | '3' | '4' | '5' | '6' |
    ========||=====|=====|=====|=====|=====|=====|=====|
    paper 1 ||  0  |  0  |  0  |  0  |  6  |  0  |  0  |
    paper 2 ||  1  |  0  |  0  |  0  |  3  |  0  |  2  |
    paper 3 ||  3  |  0  |  0  |  0  |  0  |  0  |  3  |
      ...   ||     |     |     |     |     |     |     |
    paper 9 ||     |     |     |     |     |     |     |
    ========||=====|=====|=====|=====|=====|=====|=====|

    See `Fleiss' Kappa <https://en.wikipedia.org/wiki/Fleiss%27_kappa>`_.

    Parameters:
    -----------
    M : np.array
        Matrix containing `N`subjects by `k` categories, where `M[i,j]` contains the
        number of rates that vote that category to that subject.
    """
    N, k = M.shape  # N is # of items, k is # of categories
    n_annotators = float(np.sum(M[0, :]))  # # of annotators

    p = np.sum(M, axis=0) / (N * n_annotators)
    P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
    Pbar = np.sum(P) / N
    PbarE = np.sum(p * p)
    kappa = (Pbar - PbarE) / (1 - PbarE)
    return kappa


def convert_list_to_M(list_votes, criteria=['A', '1', '2', '3', '4', '5', '6']):
    """Convert a list of (papers x raters) votes from the CSV file into the 
    `M` matrix containing (papers x subjects) categories.

    Parameters:
    -----------
    list_votes : array
        List of votes, where each row represents a paper and each column represents
        a rater. Thus, the input has the form of:

                | rater 1 | rater 2 | rater 3 |
        paper 1 |  cat A  |  cat B  |  cat A  |
    criteria : array
        List of subjects (categories) the rates vote in.
    """
    M = []
    for paper in list_votes:
        row = [0]*len(criteria)
        count = Counter(paper)
        for i, id in enumerate(criteria):
            if id in count:
                row[i] = count[id]
        M.append(row)
    return np.array(M)


def convert_list_to_binary_M(list_votes, criteria=['A', '0']):
    """Convert a list of (papers x raters) votes from the CSV file into the 
    `M` matrix containing (papers x subjects) categories.

    Parameters:
    -----------
    list_votes : array
        List of votes, where each row represents a paper and each column represents
        a rater. Thus, the input has the form of:

                | rater 1 | rater 2 | rater 3 |
        paper 1 |  cat A  |  cat B  |  cat A  |
    criteria : array
        List of subjects (categories) the rates vote in.
    """
    M = []
    for paper in list_votes:
        row = [0]*len(criteria)
        count = Counter(paper)
        for id in count:
            if id.isdigit():
                row[1] += count[id]
            else:
                row[0] += count[id]
        M.append(row)
    return np.array(M)


def compute_fleiss_kappa(csv_file, binary=False):
    """Entire pipeline of Fleiss Kappa for a CSV file.

    Parameters:
    ----------
    csv_file : string
        Path to the CSV file containing votes for subjects.
    """
    print('Computing Fleiss Kappa for file: {}'.format(csv_file))
    with open(csv_file) as csvfile:
        reader = list(csv.reader(csvfile))
    if binary:
        M = convert_list_to_binary_M(reader, criteria=['A', '0'])
    else:
        M = convert_list_to_M(reader, criteria=['A', '1', '2', '3', '4', '5', '6'])
    kappa = fleiss_kappa(M)
    print('The value of Fleiss Kappa is: {}'.format(kappa))
    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help='CSV file containing votes for subjects.')
    parser.add_argument("--binary", '-b', action='store_true', help='Compute Kappa for binary categories (Accept|Reject).')
    args = parser.parse_args()

    compute_fleiss_kappa(args.csv_file, args.binary)
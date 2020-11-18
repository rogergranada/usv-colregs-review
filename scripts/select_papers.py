"""From a CSV file containing a list of papers, select randomly a subset.

The CSV file must have the name of the paper in the 6th position. The 
complete header of the file is as follows:

```
Responsável,Database,Tipo,Duplicado_na_linha,Downloaded,Autor(YEAR),Article,Link,Classificação
```

In case a subset has already been extracted and is in the same folder of the 
original file, the final output will exclude the already extracted papers. It is important
to note that the file containing the subset has a specific name  as `papers_round_<number>.csv`,
where `<number>` is the number corresponding to the round. Thus, if we want to extract a subset
in the second round, the file `papers_round_1.csv` must be included in the same folder as the
original file containing all papers.

To run this script, one can call:

```
$ python select_papers.py data/all_papers.csv
```

This will return 35 randomly selected papers. In case one want to select another number of papers
he can pass it though the argument `--number` (`-n`), as:

```
$ python select_papers.py -n 50 data/all_papers.csv
```

In this case, the output file will contain 50 randomly selected papers.
"""
import os
import argparse
from os.path import dirname, join, realpath, basename, splitext
import pandas as pd


def select_random(df_papers : pd.DataFrame, file_csv : str, number=35) -> pd.DataFrame:
    """Given a list of papers, select `number` random papers.

    Parameters:
    -----------
    df_papers : pandas.DataFrame
        Dataframe containing all papers.
    file_csv : string
        Path to the output CSV file.
    number : int
        Number of papers to be selected from the list.
    """ 
    selected = df_papers.sample(n=number)
    selected.to_csv(file_csv, index=False)
    return selected


def extract_papers(file_csv : str, in_round=False) -> list:
    """Extract the list of papers from a file.

    Parameters:
    -----------
    file_csv : string
        Path to the CSV file containing papers.
    in_round : boolean
        True in case papers are from `papers_round_<number>.csv` files.
    """
    print('Processing: {}'.format(file_csv))
    df = pd.read_csv(file_csv)

    nb_round = 0
    if in_round:
        nb_round = int(splitext(basename(file_csv))[0].split('_')[-1])
        print('Round {} containing {} papers.'.format(nb_round, df.shape[0]))
    else:
        print('Total of papers: {}'.format(df.shape[0]))
    return df, nb_round

def papers_round(folder_papers : str) -> str:
    """Search for papers selected in previous rounds.

    Parameters:
    -----------
    folder_papers : string
        Path to the folder containing files of previous rounds.
    """
    files = os.listdir(folder_papers)
    for fname in sorted(files):
        if 'papers_round' in fname and not fname.startswith('.~'):
            filename = join(folder_papers, fname)
            yield filename

        
def create_subset_papers(file_papers : str, nb_subset : int) -> None:
    """Create a file with a subset of `nb_papers` from the original file.

    Parameters:
    -----------
    file_papers : string
        Path to the CSV file containing the list of papers.
    nb_subset : int
        Number of papers the subset output contain.

    Output:
    -------
    Create a file named `papers_round_<number>.csv where <number> is an
    integer corresponding to the number of the round.
    """
    columns=['Article']
    file_papers = realpath(file_papers)
    input_folder = dirname(file_papers)
    df_all, _ = extract_papers(file_papers, in_round=False)

    saved = [df_all]
    for fname in papers_round(input_folder):
        df_saved, nb_round = extract_papers(fname, in_round=True)
        saved.append(df_saved)
    df_all = pd.concat(saved)
    df_all.drop_duplicates(subset=columns, keep=False, inplace=True)

    print('Number of papers after rounds: {}'.format(df_all.shape[0]))
    fileout = join(input_folder, 'papers_round_{}.csv'.format(nb_round+1))
    round_papers = select_random(df_all, fileout, number=35)
    print('Selected {} papers for round {}.'.format(round_papers.shape[0], nb_round+1))
    print('Selected papers saved at: {}'.format(fileout))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help='CSV file containing a list of papers.')
    parser.add_argument("--number", '-n', default=35, help='Number of papers to select.')
    args = parser.parse_args()

    create_subset_papers(args.csv_file, args.number)


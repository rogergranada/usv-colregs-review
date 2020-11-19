# USV-COLREGS Systematic Review

This repository contains data and code for the USV-COLREGS systematic review.


## Selecting a certain number of random papers

In order to collect a list of `n` random papers for each round, one should run:

```
python scripts/select_papers.py -n <number_of_papers> <csv_containing_all_papers>
```

In case there is already a file for a certain round, it can be placed in the same folder of the file containing all papers that the script will identify it and remove the round papers from the list of all papers.

## Computing the Fleiss Kappa agreement

To compute the [Fleiss Kappa](https://en.wikipedia.org/wiki/Fleiss%27_kappa) [1] agreement between annotators considering multiple catories (e.g., exclusion criteria 1, 2, 3, ...), one should run:

```
python scripts/fleiss_kappa.py data/<csv_containing_votes>
```

In case considering binary categories (e.g., 'A' for accept the paper and any number as a single reject), one should add the parameter `-b` or `--binary` to the call as:

```
python scripts/fleiss_kappa.py -b data/<csv_containing_votes>
```

As pointed out by Landis and Koch (1977) [2], the Kappa value can be interpreted as:

|       kappa | Interpretation           |
| ----------: | :----------------------- |
|         < 0 | Poor agreement           |
| 0.01 - 0.20 | Slight agreement         |
| 0.21 - 0.40 | Fair agreement           |
| 0.41 - 0.60 | Moderate agreement       |
| 0.61 - 0.80 | Substantial agreement    |
| 0.81 - 1.00 | Almost perfect agreement |


## References

[1] Fleiss, J. L. (1971) "Measuring nominal scale agreement among many raters." Psychological Bulletin, Vol. 76, No. 5 pp. 378–382
[2] Landis, J.R. and Koch, G.G. (1977) "The measurement of observer agreement for categorical data" in Biometrics. Vol. 33, pp. 159–174.

# NICE Explainability Deletion-test Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Model: contrastive quantum-inspired projection
- Evaluation: compare score drop after deleting top contribution terms with deleting random nonzero terms.

## Summary

| evaluated_label_assignments | top_k | random_trials | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_top_score_drop | mean_random_score_drop | drop_ratio_top_vs_random |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 158.0000 | 3.0000 | 50.0000 | 0.4831 | 0.4512 | 0.4767 | 0.0319 | 0.0064 | 4.9614 |

## Example Rows

| sample_index | label | base_score | top_deleted_score | random_deleted_score | top_score_drop | random_score_drop | top_terms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | usability | 0.4804 | 0.4655 | 0.4781 | 0.0149 | 0.0023 | use, their, successfully |
| 1 | availability | 0.4174 | 0.4174 | 0.4175 | 0.0000 | -0.0001 | accessible by, accessible, system must |
| 1 | security | 0.4472 | 0.4471 | 0.4474 | 0.0001 | -0.0002 | disputes system, users, disputes |
| 2 | operability | 0.4397 | 0.4365 | 0.4400 | 0.0032 | -0.0002 | be, to be, shall be |
| 3 | look_and_feel | 0.5459 | 0.5039 | 0.5246 | 0.0420 | 0.0213 | ship, shall simulate, simulate the |
| 4 | operability | 0.4413 | 0.4369 | 0.4409 | 0.0044 | 0.0003 | environment, operate within, of the |
| 5 | usability | 0.4852 | 0.4598 | 0.4784 | 0.0254 | 0.0068 | use, shall use, navigation |
| 6 | performance | 0.5057 | 0.4570 | 0.5016 | 0.0488 | 0.0042 | seconds, time, response time |
| 7 | availability | 0.4701 | 0.4175 | 0.4645 | 0.0526 | 0.0056 | available, be available, technical |
| 7 | fault_tolerance | 0.3905 | 0.3905 | 0.3909 | 0.0000 | -0.0004 | available, available to, will be |
| 8 | look_and_feel | 0.4439 | 0.4425 | 0.4449 | 0.0013 | -0.0011 | and, products, allow |
| 8 | usability | 0.4797 | 0.4543 | 0.4726 | 0.0255 | 0.0072 | and, shall allow, allow |
| 9 | operability | 0.4365 | 0.4365 | 0.4365 | 0.0000 | -0.0000 | user, of the, of |
| 10 | availability | 0.4752 | 0.4214 | 0.4619 | 0.0537 | 0.0132 | time, shall achieve, achieve |
| 11 | security | 0.4474 | 0.4471 | 0.4475 | 0.0002 | -0.0001 | security, and or, user |
| 12 | performance | 0.6503 | 0.5612 | 0.6339 | 0.0891 | 0.0163 | minutes, shall let, let |
| 12 | usability | 0.5389 | 0.5034 | 0.5285 | 0.0356 | 0.0104 | minutes, under, in under |
| 13 | operability | 0.4607 | 0.4422 | 0.4587 | 0.0184 | 0.0020 | server, servers, or |
| 14 | security | 0.4471 | 0.4542 | 0.4474 | -0.0071 | -0.0003 | the product, product, product shall |
| 15 | security | 0.5426 | 0.4681 | 0.5353 | 0.0745 | 0.0073 | authorized, only, access |

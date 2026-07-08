# NICE Explainability Deletion-test Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Model: contrastive quantum-inspired projection
- Evaluation: compare score drop after deleting top contribution terms with deleting random nonzero terms.

## Summary

| evaluated_label_assignments | top_k | random_trials | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_comprehensiveness | mean_random_comprehensiveness | mean_sufficiency | mean_random_sufficiency | comprehensiveness_ratio | sufficiency_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 158.0000 | 3.0000 | 50.0000 | 0.4831 | 0.4512 | 0.4768 | 0.0319 | 0.0062 | -0.0359 | 0.0373 | 5.1110 | -0.9626 |

## Example Rows

| sample_index | label | base_score | top_deleted_score | random_deleted_score | comprehensiveness | random_comprehensiveness | sufficiency | random_sufficiency | top_terms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | usability | 0.4804 | 0.4655 | 0.4781 | 0.0149 | 0.0023 | -0.0128 | 0.0229 | use, their, successfully |
| 1 | availability | 0.4174 | 0.4174 | 0.4175 | 0.0000 | -0.0000 | -0.0082 | -0.0006 | accessible by, accessible, system must |
| 1 | security | 0.4472 | 0.4471 | 0.4474 | 0.0001 | -0.0002 | -0.0227 | -0.0007 | disputes system, users, disputes |
| 2 | operability | 0.4397 | 0.4365 | 0.4396 | 0.0032 | 0.0001 | -0.0419 | 0.0003 | be, to be, shall be |
| 3 | look_and_feel | 0.5459 | 0.5039 | 0.5273 | 0.0420 | 0.0185 | 0.0612 | 0.0827 | ship, shall simulate, simulate the |
| 4 | operability | 0.4413 | 0.4369 | 0.4407 | 0.0044 | 0.0006 | -0.0099 | 0.0021 | environment, operate within, of the |
| 5 | usability | 0.4852 | 0.4598 | 0.4777 | 0.0254 | 0.0075 | -0.0117 | 0.0185 | use, shall use, navigation |
| 6 | performance | 0.5057 | 0.4570 | 0.5009 | 0.0488 | 0.0049 | -0.1373 | 0.0461 | seconds, time, response time |
| 7 | availability | 0.4701 | 0.4175 | 0.4594 | 0.0526 | 0.0107 | -0.0945 | 0.0232 | available, be available, technical |
| 7 | fault_tolerance | 0.3905 | 0.3905 | 0.3909 | 0.0000 | -0.0004 | -0.0072 | -0.0016 | available, available to, will be |
| 8 | look_and_feel | 0.4439 | 0.4425 | 0.4445 | 0.0013 | -0.0007 | -0.0036 | -0.0012 | and, products, allow |
| 8 | usability | 0.4797 | 0.4543 | 0.4717 | 0.0255 | 0.0081 | -0.0202 | 0.0112 | and, shall allow, allow |
| 9 | operability | 0.4365 | 0.4365 | 0.4365 | 0.0000 | -0.0000 | 0.0000 | -0.0001 | user, of the, of |
| 10 | availability | 0.4752 | 0.4214 | 0.4625 | 0.0537 | 0.0126 | -0.0312 | 0.0399 | time, shall achieve, achieve |
| 11 | security | 0.4474 | 0.4471 | 0.4474 | 0.0002 | -0.0001 | -0.0089 | -0.0004 | security, and or, user |
| 12 | performance | 0.6503 | 0.5612 | 0.6206 | 0.0891 | 0.0296 | 0.0478 | 0.1818 | minutes, shall let, let |
| 12 | usability | 0.5389 | 0.5034 | 0.5282 | 0.0356 | 0.0107 | 0.0249 | 0.0740 | minutes, under, in under |
| 13 | operability | 0.4607 | 0.4422 | 0.4567 | 0.0184 | 0.0040 | 0.0013 | 0.0173 | server, servers, or |
| 14 | security | 0.4471 | 0.4542 | 0.4473 | -0.0071 | -0.0002 | 0.0000 | -0.0008 | the product, product, product shall |
| 15 | security | 0.5426 | 0.4681 | 0.5359 | 0.0745 | 0.0067 | -0.1635 | 0.0756 | authorized, only, access |

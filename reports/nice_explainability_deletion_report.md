# NICE Explainability Deletion-test Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Model: contrastive quantum-inspired projection
- Evaluation: compare score drop after deleting top contribution terms with deleting random nonzero terms.

## Summary

| evaluated_label_assignments | top_k | random_trials | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_comprehensiveness | mean_random_comprehensiveness | mean_sufficiency | mean_random_sufficiency | comprehensiveness_ratio | sufficiency_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 158.0000 | 3.0000 | 50.0000 | 0.4786 | 0.4481 | 0.4727 | 0.0305 | 0.0059 | -0.0395 | 0.0331 | 5.1366 | -1.1914 |

## Example Rows

| sample_index | label | base_score | top_deleted_score | random_deleted_score | comprehensiveness | random_comprehensiveness | sufficiency | random_sufficiency | top_terms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | usability | 0.4796 | 0.4636 | 0.4773 | 0.0161 | 0.0023 | -0.1152 | 0.0193 | use, be able, able to |
| 1 | availability | 0.4180 | 0.4180 | 0.4180 | 0.0000 | 0.0000 | 0.0000 | -0.0000 | by, users, and |
| 1 | security | 0.4494 | 0.4489 | 0.4495 | 0.0006 | -0.0001 | -0.0222 | -0.0005 | disputes system, users, disputes |
| 2 | operability | 0.4422 | 0.4356 | 0.4419 | 0.0066 | 0.0003 | -0.0438 | 0.0032 | be, shall be, to be |
| 3 | look_and_feel | 0.5170 | 0.4749 | 0.5035 | 0.0421 | 0.0135 | 0.0321 | 0.0603 | ship, simulate the, simulate |
| 4 | operability | 0.4470 | 0.4356 | 0.4451 | 0.0113 | 0.0019 | -0.0405 | 0.0068 | environment, operate within, operate |
| 5 | usability | 0.4907 | 0.4603 | 0.4827 | 0.0304 | 0.0080 | -0.0252 | 0.0194 | use, shall use, navigation |
| 6 | performance | 0.5269 | 0.4671 | 0.5202 | 0.0598 | 0.0066 | -0.1299 | 0.0635 | seconds, time, response time |
| 7 | availability | 0.4671 | 0.4180 | 0.4573 | 0.0491 | 0.0098 | -0.1017 | 0.0215 | available, be available, technical |
| 7 | fault_tolerance | 0.3991 | 0.3991 | 0.3994 | 0.0000 | -0.0003 | -0.0072 | -0.0013 | available, available to, be |
| 8 | look_and_feel | 0.4431 | 0.4420 | 0.4442 | 0.0011 | -0.0010 | -0.0071 | -0.0017 | and, products, allow |
| 8 | usability | 0.4892 | 0.4553 | 0.4795 | 0.0339 | 0.0097 | -0.0371 | 0.0127 | and, shall allow, allow |
| 9 | operability | 0.4356 | 0.4356 | 0.4356 | 0.0000 | -0.0000 | 0.0000 | -0.0000 | user, of the, of |
| 10 | availability | 0.4776 | 0.4206 | 0.4637 | 0.0570 | 0.0138 | -0.0438 | 0.0427 | time, shall achieve, achieve |
| 11 | security | 0.4502 | 0.4489 | 0.4501 | 0.0014 | 0.0001 | -0.0116 | 0.0001 | security, and or, the system |
| 12 | performance | 0.6037 | 0.5311 | 0.5813 | 0.0727 | 0.0224 | 0.0650 | 0.1349 | minutes, 10, shall let |
| 12 | usability | 0.5203 | 0.4887 | 0.5069 | 0.0315 | 0.0134 | 0.0205 | 0.0537 | minutes, under, in under |
| 13 | operability | 0.4582 | 0.4409 | 0.4548 | 0.0174 | 0.0035 | -0.0002 | 0.0148 | server, servers, available for |
| 14 | security | 0.4489 | 0.4567 | 0.4492 | -0.0078 | -0.0003 | 0.0000 | -0.0010 | the product, product shall, product |
| 15 | security | 0.5446 | 0.4686 | 0.5331 | 0.0761 | 0.0115 | -0.1746 | 0.0798 | authorized, only, access |

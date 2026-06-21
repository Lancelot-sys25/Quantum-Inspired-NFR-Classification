# NICE Explainability Deletion-test Report

## Setup

- Dataset: `data\raw\PROMISE-relabeled-NICE.csv`
- Model: contrastive quantum-inspired projection
- Evaluation: compare score drop after deleting top contribution terms with deleting random nonzero terms.

## Summary

| evaluated_label_assignments | top_k | random_trials | mean_base_score | mean_top_deleted_score | mean_random_deleted_score | mean_top_score_drop | mean_random_score_drop | drop_ratio_top_vs_random |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 158.0000 | 3.0000 | 50.0000 | 0.6690 | 0.5598 | 0.6552 | 0.1092 | 0.0138 | 7.9310 |

## Example Rows

| sample_index | label | base_score | top_deleted_score | random_deleted_score | top_score_drop | random_score_drop | top_terms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | usability | 0.7258 | 0.6476 | 0.7142 | 0.0782 | 0.0116 | use, their, successfully |
| 1 | availability | 0.4013 | 0.3127 | 0.4071 | 0.0885 | -0.0058 | accessible by, accessible, system must |
| 1 | security | 0.4607 | 0.3617 | 0.4611 | 0.0990 | -0.0003 | disputes system, users, disputes |
| 2 | operability | 0.5354 | 0.4089 | 0.5333 | 0.1265 | 0.0021 | be, to be, shall be |
| 3 | look_and_feel | 0.8808 | 0.8159 | 0.8509 | 0.0650 | 0.0299 | ship, shall simulate, simulate the |
| 4 | operability | 0.5567 | 0.4723 | 0.5423 | 0.0844 | 0.0144 | environment, operate within, of the |
| 5 | usability | 0.7443 | 0.6019 | 0.7114 | 0.1424 | 0.0329 | use, shall use, navigation |
| 6 | performance | 0.8225 | 0.6576 | 0.8100 | 0.1649 | 0.0125 | seconds, time, response time |
| 7 | availability | 0.7804 | 0.4325 | 0.7410 | 0.3479 | 0.0394 | available, be available, technical |
| 7 | fault_tolerance | 0.3956 | 0.3071 | 0.3936 | 0.0886 | 0.0020 | available, available to, will be |
| 8 | look_and_feel | 0.5058 | 0.4212 | 0.5025 | 0.0846 | 0.0033 | and, products, allow |
| 8 | usability | 0.7231 | 0.5301 | 0.6776 | 0.1930 | 0.0455 | and, shall allow, allow |
| 9 | operability | 0.3088 | 0.3941 | 0.3187 | -0.0853 | -0.0098 | user, of the, of |
| 10 | availability | 0.7928 | 0.5278 | 0.7496 | 0.2650 | 0.0433 | time, shall achieve, achieve |
| 11 | security | 0.4737 | 0.4050 | 0.4696 | 0.0687 | 0.0041 | security, and or, user |
| 12 | performance | 0.9513 | 0.8978 | 0.9439 | 0.0535 | 0.0073 | minutes, shall let, let |
| 12 | usability | 0.8642 | 0.7986 | 0.8473 | 0.0657 | 0.0170 | minutes, under, in under |
| 13 | operability | 0.6958 | 0.5678 | 0.6834 | 0.1280 | 0.0123 | server, servers, or |
| 14 | security | 0.3902 | 0.5921 | 0.4102 | -0.2019 | -0.0200 | the product, product, product shall |
| 15 | security | 0.8735 | 0.6888 | 0.8607 | 0.1847 | 0.0128 | authorized, only, access |

# Model Benchmarking

This is a preliminary benchmark of some local models.
The [test suites](tests) try to highlight the usage and features of llme.
The ranking should not be considered fair or rigorous, since many uncontrolled variables (still) impact it.

Moreover, the experiments are done with more or less recent versions of llme, the test suites, the models, or the server.
This explains some discrepancies with the numbers.

The benchmark is also used to check the API compatibility with local LLM servers.

Most models come from the [huggingface](https://huggingface.co/).
GUFF models are served by [llama.cpp](https://github.com/ggml-org/llama.cpp) (and [llama-swap](https://github.com/mostlygeek/llama-swap)).
MLX models are served by [nexa](https://github.com/NexaAI/nexa-sdk).
The others models come from the [ollama](https://ollama.com/) repository and are served by the ollama server.

<!-- the contents bellow this line are generated -->

* 43 models
* 5 testsuites
* 39 tests

## Results by models

| Model                                                                 | PASS        | ALMOST     | FAIL        | ERROR      | TIMEOUT     |   Total |
|:----------------------------------------------------------------------|:------------|:-----------|:------------|:-----------|:------------|--------:|
| 🟡 [qwen3-coder:30b][qw1]                                             | 29 (74.36%) | 0          | 7 (17.95%)  | 0          | 3 (7.69%)   |      39 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]             | 18 (46.15%) | 2 (5.13%)  | 3 (7.69%)   | 4 (10.26%) | 12 (30.77%) |      39 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] | 17 (53.12%) | 5 (15.62%) | 8 (25.00%)  | 0          | 2 (6.25%)   |      32 |
| 🟠 [qwen3:latest][qw2]                                                | 16 (41.03%) | 1 (2.56%)  | 12 (30.77%) | 0          | 10 (25.64%) |      39 |
| 🟠 [llama3.2-vision:latest][ll1]                                      | 16 (41.03%) | 1 (2.56%)  | 21 (53.85%) | 0          | 1 (2.56%)   |      39 |
| 🟠 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw3]                         | 16 (41.03%) | 0          | 23 (58.97%) | 0          | 0           |      39 |
| 🟠 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                  | 15 (38.46%) | 2 (5.13%)  | 18 (46.15%) | 4 (10.26%) | 0           |      39 |
| 🟠 [qwen2.5vl:latest][qw4]                                            | 14 (35.90%) | 0          | 25 (64.10%) | 0          | 0           |      39 |
| 🔴 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]            | 13 (33.33%) | 4 (10.26%) | 11 (28.21%) | 4 (10.26%) | 7 (17.95%)  |      39 |
| 🔴 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                      | 13 (33.33%) | 3 (7.69%)  | 17 (43.59%) | 4 (10.26%) | 2 (5.13%)   |      39 |
| 🔴 [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4] | 13 (33.33%) | 1 (2.56%)  | 11 (28.21%) | 4 (10.26%) | 10 (25.64%) |      39 |
| 🔴 [gemma3:latest][ge2]                                               | 13 (33.33%) | 0          | 19 (48.72%) | 1 (2.56%)  | 6 (15.38%)  |      39 |
| 🔴 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                  | 12 (30.77%) | 3 (7.69%)  | 12 (30.77%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🟠 [magistral:latest][ma1]                                            | 12 (37.50%) | 3 (9.38%)  | 15 (46.88%) | 0          | 2 (6.25%)   |      32 |
| 🔴 [llava-phi3:latest][ll2]                                           | 12 (30.77%) | 2 (5.13%)  | 25 (64.10%) | 0          | 0           |      39 |
| 🔴 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw5]                         | 12 (30.77%) | 0          | 26 (66.67%) | 1 (2.56%)  | 0           |      39 |
| 🔴 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                     | 11 (28.21%) | 5 (12.82%) | 11 (28.21%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🔴 [granite3-dense:latest][gr2]                                       | 11 (28.21%) | 3 (7.69%)  | 24 (61.54%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [llama3:latest][ll3]                                               | 11 (28.21%) | 2 (5.13%)  | 24 (61.54%) | 0          | 2 (5.13%)   |      39 |
| 🔴 [llama3.2:latest][ll4]                                             | 11 (28.21%) | 1 (2.56%)  | 25 (64.10%) | 1 (2.56%)  | 1 (2.56%)   |      39 |
| 🔴 [qwen3:4b][qw2]                                                    | 11 (28.21%) | 0          | 12 (30.77%) | 0          | 16 (41.03%) |      39 |
| 🔴 [NexaAI/gpt-oss-20b-MLX-4bit][gp1]                                 | 10 (25.64%) | 4 (10.26%) | 23 (58.97%) | 0          | 2 (5.13%)   |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                           | 10 (25.64%) | 4 (10.26%) | 13 (33.33%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🔴 [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                    | 10 (26.32%) | 3 (7.89%)  | 17 (44.74%) | 4 (10.53%) | 4 (10.53%)  |      38 |
| 🔴 [llama2:7b][ll5]                                                   | 10 (25.64%) | 0          | 29 (74.36%) | 0          | 0           |      39 |
| 🔴 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                            | 10 (25.64%) | 0          | 25 (64.10%) | 4 (10.26%) | 0           |      39 |
| 🔴 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                      | 9 (23.08%)  | 4 (10.26%) | 8 (20.51%)  | 6 (15.38%) | 12 (30.77%) |      39 |
| 🔴 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                | 9 (34.62%)  | 4 (15.38%) | 7 (26.92%)  | 0          | 6 (23.08%)  |      26 |
| 🔴 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                 | 9 (23.08%)  | 2 (5.13%)  | 24 (61.54%) | 4 (10.26%) | 0           |      39 |
| 🔴 [mistral:latest][mi1]                                              | 9 (24.32%)  | 1 (2.70%)  | 25 (67.57%) | 1 (2.70%)  | 1 (2.70%)   |      37 |
| 🔴 [llava-llama3:latest][ll6]                                         | 9 (23.08%)  | 0          | 30 (76.92%) | 0          | 0           |      39 |
| 🔴 [llava:latest][ll7]                                                | 9 (23.08%)  | 0          | 30 (76.92%) | 0          | 0           |      39 |
| 🔴 [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                    | 8 (20.51%)  | 4 (10.26%) | 26 (66.67%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp2]                            | 8 (20.51%)  | 3 (7.69%)  | 24 (61.54%) | 4 (10.26%) | 0           |      39 |
| 🔴 [minicpm-v:latest][mi2]                                            | 8 (20.51%)  | 1 (2.56%)  | 29 (74.36%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [unsloth/gpt-oss-120b-GGUF][gp2]                                   | 8 (20.51%)  | 1 (2.56%)  | 26 (66.67%) | 4 (10.26%) | 0           |      39 |
| 🔴 [llama2:latest][ll5]                                               | 8 (20.51%)  | 0          | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [bakllava:latest][ba1]                                             | 7 (17.95%)  | 1 (2.56%)  | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp3]                             | 7 (18.92%)  | 1 (2.70%)  | 24 (64.86%) | 4 (10.81%) | 1 (2.70%)   |      37 |
| 🔴 [deepseek-r1:14b][de1]                                             | 7 (17.95%)  | 0          | 6 (15.38%)  | 0          | 26 (66.67%) |      39 |
| 🔥 [gpt-oss:latest][gp4]                                              | 4 (10.26%)  | 0          | 35 (89.74%) | 0          | 0           |      39 |
| 🔥 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                          | 2 (5.13%)   | 2 (5.13%)  | 14 (35.90%) | 5 (12.82%) | 16 (41.03%) |      39 |
| 🔥 [deepseek-r1:latest][de1]                                          | 1 (2.78%)   | 1 (2.78%)  | 4 (11.11%)  | 0          | 30 (83.33%) |      36 |

## Testsuites by models

| Models                                                             | [smoketest][sm1]   | [smokeimages][sm2]   | [basic_answers][ba2]   | [hello][he1]     | [patch_file][pa1]   |
|:-------------------------------------------------------------------|:-------------------|:---------------------|:-----------------------|:-----------------|:--------------------|
| [qwen3-coder:30b][qw1]                                             | 🟢 12/13 (92.31%)  | 🔴 1/5 (20.00%)      | 💎 5/5 (100.00%)       | 💎 4/4 (100.00%) | 🟠 7/12 (58.33%)    |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]             | 💎 13/13 (100.00%) | 🔴 1/5 (20.00%)      | 🟠 2/5 (40.00%)        | 🟠 2/4 (50.00%)  | 💀 0/12             |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] | 💎 8/8 (100.00%)   | 🟡 3/5 (60.00%)      | 💀 0/5                 | 💎 2/2 (100.00%) | 🔴 4/12 (33.33%)    |
| [qwen3:latest][qw2]                                                | 💎 13/13 (100.00%) | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔴 1/4 (25.00%)  | 🔥 1/12 (8.33%)     |
| [llama3.2-vision:latest][ll1]                                      | 🟡 11/13 (84.62%)  | 🟡 3/5 (60.00%)      | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/12             |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw3]                         | 🟡 11/13 (84.62%)  | 💀 0/5               | 🟡 3/5 (60.00%)        | 🟠 2/4 (50.00%)  | 💀 0/12             |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                  | 🟢 12/13 (92.31%)  | 💀 0/5               | 🟠 2/5 (40.00%)        | 🔴 1/4 (25.00%)  | 💀 0/12             |
| [qwen2.5vl:latest][qw4]                                            | 🟡 9/13 (69.23%)   | 🟡 4/5 (80.00%)      | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]            | 🟡 10/13 (76.92%)  | 💀 0/5               | 💀 0/5                 | 🟡 3/4 (75.00%)  | 💀 0/12             |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                      | 🟡 9/13 (69.23%)   | 💀 0/5               | 🟠 2/5 (40.00%)        | 🟠 2/4 (50.00%)  | 💀 0/12             |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4] | 🟡 10/13 (76.92%)  | 💀 0/5               | 💀 0/5                 | 🔴 1/4 (25.00%)  | 🔴 2/12 (16.67%)    |
| [gemma3:latest][ge2]                                               | 🟠 7/13 (53.85%)   | 🟡 3/5 (60.00%)      | 🟠 2/5 (40.00%)        | 🔴 1/4 (25.00%)  | 💀 0/12             |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                  | 🟡 11/13 (84.62%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [magistral:latest][ma1]                                            | 🟡 9/11 (81.82%)   | 🔴 1/5 (20.00%)      | 🔴 1/5 (20.00%)        | 🟠 1/2 (50.00%)  | 💀 0/9              |
| [llava-phi3:latest][ll2]                                           | 🟡 9/13 (69.23%)   | 🟡 3/5 (60.00%)      | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw5]                         | 🟡 9/13 (69.23%)   | 🔴 1/5 (20.00%)      | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/12             |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                     | 🟡 9/13 (69.23%)   | 💀 0/5               | 💀 0/5                 | 🟠 2/4 (50.00%)  | 💀 0/12             |
| [granite3-dense:latest][gr2]                                       | 🟡 10/13 (76.92%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [llama3:latest][ll3]                                               | 🟡 10/13 (76.92%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [llama3.2:latest][ll4]                                             | 🟡 10/13 (76.92%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [qwen3:4b][qw2]                                                    | 🟡 9/13 (69.23%)   | 💀 0/5               | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/12             |
| [NexaAI/gpt-oss-20b-MLX-4bit][gp1]                                 | 🟡 10/13 (76.92%)  | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                           | 🟠 7/13 (53.85%)   | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔴 1/4 (25.00%)  | 🔥 1/12 (8.33%)     |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                    | 🟡 9/13 (69.23%)   | 💀 0/5               | 💀 0/5                 | 🔴 1/3 (33.33%)  | 💀 0/12             |
| [llama2:7b][ll5]                                                   | 🟡 8/13 (61.54%)   | 🟠 2/5 (40.00%)      | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                            | 🟡 8/13 (61.54%)   | 💀 0/5               | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/12             |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                      | 🟡 9/13 (69.23%)   | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                | 🟢 6/7 (85.71%)    | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💎 2/2 (100.00%) | 💀 0/7              |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                 | 🟡 9/13 (69.23%)   | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [mistral:latest][mi1]                                              | 🟡 8/13 (61.54%)   | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💀 0/2           | 💀 0/12             |
| [llava-llama3:latest][ll6]                                         | 🟠 5/13 (38.46%)   | 🟡 3/5 (60.00%)      | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [llava:latest][ll7]                                                | 🟠 5/13 (38.46%)   | 🟡 4/5 (80.00%)      | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                    | 🟠 7/13 (53.85%)   | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp2]                            | 🟡 8/13 (61.54%)   | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [minicpm-v:latest][mi2]                                            | 🔴 4/13 (30.77%)   | 🟡 3/5 (60.00%)      | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [unsloth/gpt-oss-120b-GGUF][gp2]                                   | 🟡 8/13 (61.54%)   | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [llama2:latest][ll5]                                               | 🟠 6/13 (46.15%)   | 🔴 1/5 (20.00%)      | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [bakllava:latest][ba1]                                             | 🔴 3/13 (23.08%)   | 🟡 4/5 (80.00%)      | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp3]                             | 🟠 7/13 (53.85%)   | 💀 0/5               | 💀 0/5                 | 💀 0/2           | 💀 0/12             |
| [deepseek-r1:14b][de1]                                             | 🟠 6/13 (46.15%)   | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [gpt-oss:latest][gp4]                                              | 🔴 3/13 (23.08%)   | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/12             |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                          | 🔴 2/13 (15.38%)   | 💀 0/5               | 💀 0/5                 | 💀 0/4           | 💀 0/12             |
| [deepseek-r1:latest][de1]                                          | 💀 0/12            | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💀 0/2           | 💀 0/12             |

## Results by testsuites

| Model                   | PASS         | ALMOST      | FAIL         | ERROR       | TIMEOUT     |   Total |
|:------------------------|:-------------|:------------|:-------------|:------------|:------------|--------:|
| 🟡 [smoketest][sm1]     | 349 (64.04%) | 0           | 130 (23.85%) | 4 (0.73%)   | 62 (11.38%) |     545 |
| 🔴 [smokeimages][sm2]   | 40 (18.60%)  | 0           | 102 (47.44%) | 66 (30.70%) | 7 (3.26%)   |     215 |
| 🔴 [basic_answers][ba2] | 38 (17.67%)  | 74 (34.42%) | 82 (38.14%)  | 0           | 21 (9.77%)  |     215 |
| 🔴 [hello][he1]         | 26 (16.35%)  | 0           | 114 (71.70%) | 0           | 19 (11.95%) |     159 |
| 🔥 [patch_file][pa1]    | 15 (2.95%)   | 0           | 402 (79.13%) | 1 (0.20%)   | 90 (17.72%) |     508 |

## Results by tests

| Model                           | PASS        | ALMOST      | FAIL        | ERROR       | TIMEOUT     |   Total |
|:--------------------------------|:------------|:------------|:------------|:------------|:------------|--------:|
| 🟢 [smoketest][sm1] 03          | 38 (88.37%) | 0           | 2 (4.65%)   | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 04          | 36 (83.72%) | 0           | 4 (9.30%)   | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 32          | 36 (83.72%) | 0           | 3 (6.98%)   | 0           | 4 (9.30%)   |      43 |
| 🟡 [smoketest][sm1] 05          | 36 (83.72%) | 0           | 4 (9.30%)   | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 06          | 34 (80.95%) | 0           | 2 (4.76%)   | 0           | 6 (14.29%)  |      42 |
| 🟡 [smoketest][sm1] 33          | 32 (74.42%) | 0           | 7 (16.28%)  | 1 (2.33%)   | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 01          | 28 (65.12%) | 0           | 4 (9.30%)   | 1 (2.33%)   | 10 (23.26%) |      43 |
| 🟠 [smoketest][sm1] 11          | 22 (53.66%) | 0           | 18 (43.90%) | 0           | 1 (2.44%)   |      41 |
| 🟠 [smoketest][sm1] 02          | 22 (51.16%) | 0           | 5 (11.63%)  | 2 (4.65%)   | 14 (32.56%) |      43 |
| 🟠 [smoketest][sm1] 13          | 18 (45.00%) | 0           | 19 (47.50%) | 0           | 3 (7.50%)   |      40 |
| 🟠 [basic_answers][ba2] 0.paris | 17 (39.53%) | 23 (53.49%) | 3 (6.98%)   | 0           | 0           |      43 |
| 🟠 [smoketest][sm1] 12          | 17 (42.50%) | 0           | 20 (50.00%) | 0           | 3 (7.50%)   |      40 |
| 🟠 [basic_answers][ba2] 4.fact  | 16 (37.21%) | 10 (23.26%) | 14 (32.56%) | 0           | 3 (6.98%)   |      43 |
| 🟠 [smoketest][sm1] 10          | 16 (40.00%) | 0           | 23 (57.50%) | 0           | 1 (2.50%)   |      40 |
| 🔴 [smoketest][sm1] 31          | 14 (34.15%) | 0           | 19 (46.34%) | 0           | 8 (19.51%)  |      41 |
| 🔴 [smokeimages][sm2] 4         | 14 (32.56%) | 0           | 11 (25.58%) | 16 (37.21%) | 2 (4.65%)   |      43 |
| 🔴 [smokeimages][sm2] 0         | 9 (20.93%)  | 0           | 17 (39.53%) | 16 (37.21%) | 1 (2.33%)   |      43 |
| 🔴 [smokeimages][sm2] 2         | 9 (20.93%)  | 0           | 17 (39.53%) | 16 (37.21%) | 1 (2.33%)   |      43 |
| 🔴 [hello][he1] 02name          | 8 (18.60%)  | 0           | 30 (69.77%) | 0           | 5 (11.63%)  |      43 |
| 🔴 [hello][he1] 03git           | 8 (21.62%)  | 0           | 23 (62.16%) | 0           | 6 (16.22%)  |      37 |
| 🔴 [smokeimages][sm2] 1         | 7 (16.28%)  | 0           | 19 (44.19%) | 17 (39.53%) | 0           |      43 |
| 🔥 [hello][he1] 01world         | 6 (13.95%)  | 0           | 34 (79.07%) | 0           | 3 (6.98%)   |      43 |
| 🔥 [patch_file][pa1] 05python   | 4 (9.52%)   | 0           | 33 (78.57%) | 0           | 5 (11.90%)  |      42 |
| 🔥 [patch_file][pa1] 04ed       | 4 (9.52%)   | 0           | 31 (73.81%) | 0           | 7 (16.67%)  |      42 |
| 🔥 [hello][he1] 04gitignore     | 4 (11.11%)  | 0           | 27 (75.00%) | 0           | 5 (13.89%)  |      36 |
| 🔥 [basic_answers][ba2] 3.llme  | 2 (4.65%)   | 15 (34.88%) | 21 (48.84%) | 0           | 5 (11.63%)  |      43 |
| 🔥 [basic_answers][ba2] 1.llme  | 2 (4.65%)   | 12 (27.91%) | 22 (51.16%) | 0           | 7 (16.28%)  |      43 |
| 🔥 [patch_file][pa1] 03patch    | 2 (4.88%)   | 0           | 32 (78.05%) | 0           | 7 (17.07%)  |      41 |
| 🔥 [patch_file][pa1] 01cat      | 2 (4.88%)   | 0           | 32 (78.05%) | 0           | 7 (17.07%)  |      41 |
| 🔥 [basic_answers][ba2] 2.llme  | 1 (2.33%)   | 14 (32.56%) | 22 (51.16%) | 0           | 6 (13.95%)  |      43 |
| 🔥 [patch_file][pa1] 11cat      | 1 (2.33%)   | 0           | 36 (83.72%) | 0           | 6 (13.95%)  |      43 |
| 🔥 [patch_file][pa1] 00free     | 1 (2.38%)   | 0           | 35 (83.33%) | 0           | 6 (14.29%)  |      42 |
| 🔥 [patch_file][pa1] 02sed      | 1 (2.38%)   | 0           | 33 (78.57%) | 0           | 8 (19.05%)  |      42 |
| 🔥 [smokeimages][sm2] 3         | 1 (2.33%)   | 0           | 38 (88.37%) | 1 (2.33%)   | 3 (6.98%)   |      43 |
| 💀 [patch_file][pa1] 10free     | 0           | 0           | 35 (81.40%) | 0           | 8 (18.60%)  |      43 |
| 💀 [patch_file][pa1] 14ed       | 0           | 0           | 33 (76.74%) | 0           | 10 (23.26%) |      43 |
| 💀 [patch_file][pa1] 13patch    | 0           | 0           | 35 (81.40%) | 0           | 8 (18.60%)  |      43 |
| 💀 [patch_file][pa1] 12sed      | 0           | 0           | 36 (83.72%) | 0           | 7 (16.28%)  |      43 |
| 💀 [patch_file][pa1] 15python   | 0           | 0           | 31 (72.09%) | 1 (2.33%)   | 11 (25.58%) |      43 |


  [qw1]: https://ollama.com/library/qwen3-coder
  [Qw1]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [Mi1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [qw2]: https://ollama.com/library/qwen3
  [ll1]: https://ollama.com/library/llama3.2-vision
  [qw3]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [Qw2]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [qw4]: https://ollama.com/library/qwen2.5vl
  [Qw3]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [ge1]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [Qw4]: https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [ge2]: https://ollama.com/library/gemma3
  [Qw5]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [ma1]: https://ollama.com/library/magistral
  [ll2]: https://ollama.com/library/llava-phi3
  [qw5]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [gr1]: https://huggingface.co/unsloth/granite-4.0-h-small-GGUF
  [gr2]: https://ollama.com/library/granite3-dense
  [ll3]: https://ollama.com/library/llama3
  [ll4]: https://ollama.com/library/llama3.2
  [gp1]: https://huggingface.co/NexaAI/gpt-oss-20b-MLX-4bit
  [Qw6]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [Qw7]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [ll5]: https://ollama.com/library/llama2
  [LF1]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [gr3]: https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF
  [Ma1]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [gr4]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [mi1]: https://ollama.com/library/mistral
  [ll6]: https://ollama.com/library/llava-llama3
  [ll7]: https://ollama.com/library/llava
  [Qw8]: https://huggingface.co/NexaAI/Qwen3-4B-4bit-MLX
  [gp2]: https://huggingface.co/unsloth/gpt-oss-120b-GGUF
  [mi2]: https://ollama.com/library/minicpm-v
  [ba1]: https://ollama.com/library/bakllava
  [gp3]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [de1]: https://ollama.com/library/deepseek-r1
  [gp4]: https://ollama.com/library/gpt-oss
  [ge3]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [sm1]: tests/smoketest.sh
  [sm2]: tests/smokeimages.sh
  [ba2]: tests/basic_answers.sh
  [he1]: tests/hello.sh
  [pa1]: tests/patch_file.sh

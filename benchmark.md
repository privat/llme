# Model Benchmarking

This is a preliminary benchmark of some local models.
The [test suites](tests) try to highlight the usage and features of llme.
The ranking should not be considered fair or rigorous, since many uncontrolled variables (still) impact it.

Moreover, the experiments are done with more or less recent versions of llme, the test suites, the models, or the server.
This explains possible discrepancies with the numbers.

The benchmark is also used to check the API compatibility with local LLM servers.

Most models come from the [huggingface](https://huggingface.co/).
GUFF models are served by [llama.cpp](https://github.com/ggml-org/llama.cpp) (and [llama-swap](https://github.com/mostlygeek/llama-swap)).
MLX models are served by [nexa](https://github.com/NexaAI/nexa-sdk).
The others models come from the [ollama](https://ollama.com/) repository and are served by the ollama server.

These preliminary results show that there is a lot of variation in the performance of the models, and that if the model size or the temperature does something, but it's not clear what...
The larger is not always the better.

## Legend

* PASS: the task was successfully completed.
* ALMOST: some tasks have a fallback validation.
* FAIL: the task was successfully completed.
* ERROR: there was an error during the task.
  Most are server errors: images unsupported by the model, or context too large.
* TIMEOUT: the task was not completed before 3 minutes.
  Usually it means the model went into repeating itself and running the same commands again and again without progress or giving the hand to the user.
  Note that we do not check if the task was successful or not.

## Basic stats

<!-- the contents bellow this line are generated -->

* 46 models
* 75 model configurations
* 5 task suites
* 39 tasks

## Results by models

| name                                                                                | PASS        | ALMOST     | FAIL        | ERROR       | TIMEOUT     |   Total |
|:------------------------------------------------------------------------------------|:------------|:-----------|:------------|:------------|:------------|--------:|
| 🟡 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] mode=native                               | 29 (74.36%) | 1 (2.56%)  | 4 (10.26%)  | 4 (10.26%)  | 1 (2.56%)   |      39 |
| 🟡 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=1.0 mode=native                         | 27 (69.23%) | 1 (2.56%)  | 7 (17.95%)  | 4 (10.26%)  | 0           |      39 |
| 🟡 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=0.5 mode=native                         | 26 (66.67%) | 0          | 8 (20.51%)  | 4 (10.26%)  | 1 (2.56%)   |      39 |
| 🟠 [qwen3-coder:30b][qw1] t=0.0 mode=native                                         | 25 (64.10%) | 2 (5.13%)  | 10 (25.64%) | 0           | 2 (5.13%)   |      39 |
| 🟠 [qwen3-coder:30b][qw1] t=0.5 mode=native                                         | 25 (64.10%) | 1 (2.56%)  | 12 (30.77%) | 0           | 1 (2.56%)   |      39 |
| 🟠 [qwen3-coder:30b][qw1] mode=native                                               | 24 (61.54%) | 1 (2.56%)  | 14 (35.90%) | 0           | 0           |      39 |
| 🟠 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=0.0 mode=native                         | 24 (61.54%) | 0          | 8 (20.51%)  | 4 (10.26%)  | 3 (7.69%)   |      39 |
| 🟠 [qwen3-coder:30b][qw1] t=1.5 mode=native                                         | 22 (56.41%) | 2 (5.13%)  | 15 (38.46%) | 0           | 0           |      39 |
| 🟠 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1] mode=native                       | 22 (56.41%) | 1 (2.56%)  | 11 (28.21%) | 4 (10.26%)  | 1 (2.56%)   |      39 |
| 🟠 [qwen3-coder:30b][qw1] t=1.0 mode=native                                         | 22 (56.41%) | 0          | 17 (43.59%) | 0           | 0           |      39 |
| 🟠 [qwen3:latest][qw2] mode=native                                                  | 21 (53.85%) | 2 (5.13%)  | 15 (38.46%) | 0           | 1 (2.56%)   |      39 |
| 🟠 [gpt-oss:latest][gp2] mode=native                                                | 21 (53.85%) | 1 (2.56%)  | 15 (38.46%) | 0           | 2 (5.13%)   |      39 |
| 🟠 [qwen3:32b][qw2] mode=native                                                     | 20 (51.28%) | 3 (7.69%)  | 7 (17.95%)  | 0           | 9 (23.08%)  |      39 |
| 🟠 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1] mode=native                        | 20 (51.28%) | 2 (5.13%)  | 10 (25.64%) | 1 (2.56%)   | 6 (15.38%)  |      39 |
| 🟠 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw1] mode=native                             | 20 (51.28%) | 2 (5.13%)  | 11 (28.21%) | 6 (15.38%)  | 0           |      39 |
| 🟠 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw2] mode=native                    | 20 (51.28%) | 0          | 10 (25.64%) | 4 (10.26%)  | 5 (12.82%)  |      39 |
| 🟠 [qwen3:14b][qw2] mode=native                                                     | 19 (48.72%) | 2 (5.13%)  | 13 (33.33%) | 0           | 5 (12.82%)  |      39 |
| 🟠 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw3] mode=native                    | 19 (48.72%) | 2 (5.13%)  | 14 (35.90%) | 4 (10.26%)  | 0           |      39 |
| 🟠 [qwen3-coder:30b][qw1] t=2.0 mode=native                                         | 19 (48.72%) | 1 (2.56%)  | 19 (48.72%) | 0           | 0           |      39 |
| 🟠 [qwen3:4b][qw2] mode=native                                                      | 19 (48.72%) | 1 (2.56%)  | 19 (48.72%) | 0           | 0           |      39 |
| 🟠 [qwen3:30b][qw2] mode=native                                                     | 18 (46.15%) | 0          | 17 (43.59%) | 0           | 4 (10.26%)  |      39 |
| 🟠 [qwen3:1.7b][qw2] mode=native                                                    | 17 (43.59%) | 2 (5.13%)  | 18 (46.15%) | 0           | 2 (5.13%)   |      39 |
| 🟠 [qwen3:30b][qw2] mode=markdown                                                   | 16 (41.03%) | 1 (2.56%)  | 20 (51.28%) | 0           | 2 (5.13%)   |      39 |
| 🟠 [qwen3:14b][qw2] mode=markdown                                                   | 16 (41.03%) | 1 (2.56%)  | 19 (48.72%) | 0           | 3 (7.69%)   |      39 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw4] mode=native               | 15 (38.46%) | 4 (10.26%) | 11 (28.21%) | 4 (10.26%)  | 5 (12.82%)  |      39 |
| 🟠 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr2] mode=native                   | 15 (38.46%) | 3 (7.69%)  | 17 (43.59%) | 4 (10.26%)  | 0           |      39 |
| 🟠 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw5] mode=native              | 14 (35.90%) | 3 (7.69%)  | 15 (38.46%) | 6 (15.38%)  | 1 (2.56%)   |      39 |
| 🟠 [qwen3:32b][qw2] mode=markdown                                                   | 14 (35.90%) | 1 (2.56%)  | 18 (46.15%) | 0           | 6 (15.38%)  |      39 |
| 🟠 [qwen3:latest][qw2] mode=markdown                                                | 14 (35.90%) | 1 (2.56%)  | 23 (58.97%) | 0           | 1 (2.56%)   |      39 |
| 🔴 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1] mode=native                  | 13 (33.33%) | 4 (10.26%) | 18 (46.15%) | 1 (2.56%)   | 3 (7.69%)   |      39 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] mode=native   | 13 (33.33%) | 2 (5.13%)  | 10 (25.64%) | 1 (2.56%)   | 13 (33.33%) |      39 |
| 🔴 [qwen3-coder:30b][qw1] mode=markdown                                             | 13 (33.33%) | 0          | 26 (66.67%) | 0           | 0           |      39 |
| 🔴 [qwen2.5vl:latest][qw3] mode=markdown                                            | 13 (33.33%) | 0          | 26 (66.67%) | 0           | 0           |      39 |
| 🔴 [gpt-oss:latest][gp2] mode=markdown                                              | 13 (33.33%) | 0          | 26 (66.67%) | 0           | 0           |      39 |
| 🔴 [llama3.2:latest][ll1] mode=native                                               | 12 (30.77%) | 2 (5.13%)  | 25 (64.10%) | 0           | 0           |      39 |
| 🔴 [qwen3:4b][qw2] mode=markdown                                                    | 12 (30.77%) | 1 (2.56%)  | 26 (66.67%) | 0           | 0           |      39 |
| 🔴 [llama3:latest][ll2] mode=markdown                                               | 12 (30.77%) | 0          | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [minicpm-v:latest][mi1] mode=markdown                                            | 12 (30.77%) | 0          | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [deepseek-r1:14b][de1] mode=markdown                                             | 12 (30.77%) | 0          | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [llama3.2:latest][ll1] mode=markdown                                             | 11 (28.21%) | 1 (2.56%)  | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [llama3.2-vision:latest][ll3] mode=markdown                                      | 11 (28.21%) | 1 (2.56%)  | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1] mode=markdown                | 11 (28.21%) | 1 (2.56%)  | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1] mode=markdown                     | 11 (28.21%) | 1 (2.56%)  | 22 (56.41%) | 4 (10.26%)  | 1 (2.56%)   |      39 |
| 🔴 [qwen3:0.6b][qw2] mode=native                                                    | 10 (25.64%) | 4 (10.26%) | 25 (64.10%) | 0           | 0           |      39 |
| 🔴 [gemma3:27b][ge2] mode=markdown                                                  | 10 (25.64%) | 3 (7.69%)  | 26 (66.67%) | 0           | 0           |      39 |
| 🔴 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3] mode=native                        | 10 (25.64%) | 3 (7.69%)  | 16 (41.03%) | 4 (10.26%)  | 6 (15.38%)  |      39 |
| 🔴 [magistral:latest][ma1] mode=markdown                                            | 10 (25.64%) | 2 (5.13%)  | 26 (66.67%) | 0           | 1 (2.56%)   |      39 |
| 🔴 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=1.5 mode=native                         | 10 (25.64%) | 2 (5.13%)  | 22 (56.41%) | 5 (12.82%)  | 0           |      39 |
| 🔴 [llava-llama3:latest][ll4] mode=markdown                                         | 10 (25.64%) | 1 (2.56%)  | 28 (71.79%) | 0           | 0           |      39 |
| 🔴 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr2] mode=markdown                 | 10 (25.64%) | 1 (2.56%)  | 24 (61.54%) | 4 (10.26%)  | 0           |      39 |
| 🔴 [granite3-dense:latest][gr4] mode=native                                         | 10 (25.64%) | 0          | 29 (74.36%) | 0           | 0           |      39 |
| 🔴 [llava:latest][ll5] mode=markdown                                                | 10 (25.64%) | 0          | 29 (74.36%) | 0           | 0           |      39 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] mode=markdown | 9 (23.08%)  | 4 (10.26%) | 25 (64.10%) | 0           | 1 (2.56%)   |      39 |
| 🔴 [magistral:latest][ma1] mode=native                                              | 9 (23.08%)  | 3 (7.69%)  | 27 (69.23%) | 0           | 0           |      39 |
| 🔴 [llava-phi3:latest][ll6] mode=markdown                                           | 9 (23.08%)  | 1 (2.56%)  | 29 (74.36%) | 0           | 0           |      39 |
| 🔴 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1] mode=native                              | 9 (23.08%)  | 0          | 18 (46.15%) | 4 (10.26%)  | 8 (20.51%)  |      39 |
| 🔴 [llama2:latest][ll7] mode=markdown                                               | 8 (20.51%)  | 1 (2.56%)  | 30 (76.92%) | 0           | 0           |      39 |
| 🔴 [qwen3:1.7b][qw2] mode=markdown                                                  | 8 (20.51%)  | 1 (2.56%)  | 29 (74.36%) | 0           | 1 (2.56%)   |      39 |
| 🔴 [llama2:7b][ll7] mode=markdown                                                   | 8 (20.51%)  | 1 (2.56%)  | 30 (76.92%) | 0           | 0           |      39 |
| 🔴 [mistral:latest][mi2] mode=markdown                                              | 8 (20.51%)  | 1 (2.56%)  | 30 (76.92%) | 0           | 0           |      39 |
| 🔴 [granite3-dense:latest][gr4] mode=markdown                                       | 8 (20.51%)  | 1 (2.56%)  | 30 (76.92%) | 0           | 0           |      39 |
| 🔴 [qwen3:0.6b][qw2] mode=markdown                                                  | 8 (20.51%)  | 1 (2.56%)  | 30 (76.92%) | 0           | 0           |      39 |
| 🔴 [gemma3:latest][ge2] mode=markdown                                               | 8 (20.51%)  | 0          | 31 (79.49%) | 0           | 0           |      39 |
| 🔴 [gemma3:12b][ge2] mode=markdown                                                  | 8 (20.51%)  | 0          | 31 (79.49%) | 0           | 0           |      39 |
| 🔴 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3] mode=markdown                          | 7 (17.95%)  | 0          | 28 (71.79%) | 4 (10.26%)  | 0           |      39 |
| 🔴 [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw6] mode=markdown                    | 7 (17.95%)  | 0          | 12 (30.77%) | 4 (10.26%)  | 16 (41.03%) |      39 |
| 🔴 [bakllava:latest][ba1] mode=markdown                                             | 6 (15.38%)  | 1 (2.56%)  | 32 (82.05%) | 0           | 0           |      39 |
| 🔴 [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw7] mode=markdown | 6 (15.38%)  | 1 (2.56%)  | 22 (56.41%) | 4 (10.26%)  | 6 (15.38%)  |      39 |
| 🔴 [gemma3:1b][ge2] mode=markdown                                                   | 6 (15.38%)  | 1 (2.56%)  | 28 (71.79%) | 4 (10.26%)  | 0           |      39 |
| 🔴 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1] mode=markdown                            | 6 (15.38%)  | 0          | 28 (71.79%) | 4 (10.26%)  | 1 (2.56%)   |      39 |
| 🔥 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=2.0 mode=native                         | 5 (12.82%)  | 3 (7.69%)  | 25 (64.10%) | 6 (15.38%)  | 0           |      39 |
| 🔥 [mistral:latest][mi2] mode=native                                                | 5 (12.82%)  | 2 (5.13%)  | 32 (82.05%) | 0           | 0           |      39 |
| 🔥 [gemma3:270m][ge2] mode=markdown                                                 | 5 (12.82%)  | 1 (2.56%)  | 29 (74.36%) | 4 (10.26%)  | 0           |      39 |
| 🔥 [deepseek-r1:latest][de1] mode=markdown                                          | 4 (10.26%)  | 0          | 12 (30.77%) | 0           | 23 (58.97%) |      39 |
| 💀 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3] mode=native                            | 0           | 0          | 2 (5.13%)   | 34 (87.18%) | 3 (7.69%)   |      39 |

## Task suites by models

| Models                                                                           | [smoketest][sm1]   | [basic_answers][ba2]   | [hello][he1]     | [smokeimages][sm2]   | [patch_file][pa1]   |
|:---------------------------------------------------------------------------------|:-------------------|:-----------------------|:-----------------|:---------------------|:--------------------|
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] mode=native                               | 💎 13/13 (100.00%) | 🟡 4/5 (80.00%)        | 💎 4/4 (100.00%) | 💀 0/5               | 🟡 8/12 (66.67%)    |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=1.0 mode=native                         | 🟢 12/13 (92.31%)  | 🟡 4/5 (80.00%)        | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 🟠 6/12 (50.00%)    |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=0.5 mode=native                         | 🟢 12/13 (92.31%)  | 🟡 4/5 (80.00%)        | 💎 4/4 (100.00%) | 💀 0/5               | 🟠 6/12 (50.00%)    |
| [qwen3-coder:30b][qw1] t=0.0 mode=native                                         | 💎 13/13 (100.00%) | 🟠 3/5 (60.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🟠 6/12 (50.00%)    |
| [qwen3-coder:30b][qw1] t=0.5 mode=native                                         | 🟢 12/13 (92.31%)  | 🟡 4/5 (80.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🟠 6/12 (50.00%)    |
| [qwen3-coder:30b][qw1] mode=native                                               | 🟡 11/13 (84.62%)  | 🟠 3/5 (60.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🟠 7/12 (58.33%)    |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=0.0 mode=native                         | 🟡 11/13 (84.62%)  | 🟡 4/5 (80.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🟠 6/12 (50.00%)    |
| [qwen3-coder:30b][qw1] t=1.5 mode=native                                         | 🟡 10/13 (76.92%)  | 🟠 2/5 (40.00%)        | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 🟠 5/12 (41.67%)    |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1] mode=native                       | 🟢 12/13 (92.31%)  | 🟡 4/5 (80.00%)        | 💎 4/4 (100.00%) | 💀 0/5               | 🔴 2/12 (16.67%)    |
| [qwen3-coder:30b][qw1] t=1.0 mode=native                                         | 🟢 12/13 (92.31%)  | 🟠 2/5 (40.00%)        | 🟡 3/4 (75.00%)  | 🔴 1/5 (20.00%)      | 🔴 4/12 (33.33%)    |
| [qwen3:latest][qw2] mode=native                                                  | 🟢 12/13 (92.31%)  | 🟠 3/5 (60.00%)        | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 🔥 1/12 (8.33%)     |
| [gpt-oss:latest][gp2] mode=native                                                | 💎 13/13 (100.00%) | 🟠 3/5 (60.00%)        | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)      | 💀 0/12             |
| [qwen3:32b][qw2] mode=native                                                     | 🟢 12/13 (92.31%)  | 🟠 2/5 (40.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🔴 3/12 (25.00%)    |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1] mode=native                        | 🟢 12/13 (92.31%)  | 🟠 3/5 (60.00%)        | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw1] mode=native                             | 🟡 11/13 (84.62%)  | 🟠 3/5 (60.00%)        | 💎 4/4 (100.00%) | 💀 0/5               | 🔴 2/12 (16.67%)    |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw2] mode=native                    | 🟡 11/13 (84.62%)  | 💎 5/5 (100.00%)       | 🟠 2/4 (50.00%)  | 💀 0/5               | 🔴 2/12 (16.67%)    |
| [qwen3:14b][qw2] mode=native                                                     | 🟡 10/13 (76.92%)  | 🟠 3/5 (60.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 🔴 3/12 (25.00%)    |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw3] mode=native                    | 💎 13/13 (100.00%) | 🟠 3/5 (60.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/12             |
| [qwen3-coder:30b][qw1] t=2.0 mode=native                                         | 🟡 10/13 (76.92%)  | 🟠 2/5 (40.00%)        | 🟡 3/4 (75.00%)  | 🔴 1/5 (20.00%)      | 🔴 3/12 (25.00%)    |
| [qwen3:4b][qw2] mode=native                                                      | 💎 13/13 (100.00%) | 🟠 2/5 (40.00%)        | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)      | 🔥 1/12 (8.33%)     |
| [qwen3:30b][qw2] mode=native                                                     | 🟡 10/13 (76.92%)  | 🟠 2/5 (40.00%)        | 🟡 3/4 (75.00%)  | 🔴 1/5 (20.00%)      | 🔴 2/12 (16.67%)    |
| [qwen3:1.7b][qw2] mode=native                                                    | 🟢 12/13 (92.31%)  | 🟠 2/5 (40.00%)        | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/12             |
| [qwen3:30b][qw2] mode=markdown                                                   | 🟠 8/13 (61.54%)   | 🟠 2/5 (40.00%)        | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)      | 🔴 3/12 (25.00%)    |
| [qwen3:14b][qw2] mode=markdown                                                   | 🟡 11/13 (84.62%)  | 🟠 3/5 (60.00%)        | 💀 0/4           | 💀 0/5               | 🔴 2/12 (16.67%)    |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw4] mode=native               | 💎 13/13 (100.00%) | 🔴 1/5 (20.00%)        | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/12             |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr2] mode=native                   | 🟢 12/13 (92.31%)  | 💀 0/5                 | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/12             |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw5] mode=native              | 🟡 11/13 (84.62%)  | 🔴 1/5 (20.00%)        | 🟠 2/4 (50.00%)  | 💀 0/5               | 💀 0/12             |
| [qwen3:32b][qw2] mode=markdown                                                   | 🟡 10/13 (76.92%)  | 🟠 3/5 (60.00%)        | 💀 0/4           | 💀 0/5               | 🔥 1/12 (8.33%)     |
| [qwen3:latest][qw2] mode=markdown                                                | 🟡 10/13 (76.92%)  | 🟠 3/5 (60.00%)        | 💀 0/4           | 💀 0/5               | 🔥 1/12 (8.33%)     |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1] mode=native                  | 🟠 8/13 (61.54%)   | 🔴 1/5 (20.00%)        | 🟠 2/4 (50.00%)  | 🟠 2/5 (40.00%)      | 💀 0/12             |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] mode=native   | 🟡 10/13 (76.92%)  | 🔴 1/5 (20.00%)        | 🔴 1/4 (25.00%)  | 💀 0/5               | 🔥 1/12 (8.33%)     |
| [qwen3-coder:30b][qw1] mode=markdown                                             | 🟡 10/13 (76.92%)  | 🟠 2/5 (40.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [qwen2.5vl:latest][qw3] mode=markdown                                            | 🟠 8/13 (61.54%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🟡 4/5 (80.00%)      | 💀 0/12             |
| [gpt-oss:latest][gp2] mode=markdown                                              | 🟡 9/13 (69.23%)   | 🟠 2/5 (40.00%)        | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llama3.2:latest][ll1] mode=native                                               | 🟡 9/13 (69.23%)   | 🔴 1/5 (20.00%)        | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [qwen3:4b][qw2] mode=markdown                                                    | 🟠 7/13 (53.85%)   | 🟠 2/5 (40.00%)        | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)      | 🔥 1/12 (8.33%)     |
| [llama3:latest][ll2] mode=markdown                                               | 🟠 8/13 (61.54%)   | 🟠 2/5 (40.00%)        | 💀 0/4           | 🟠 2/5 (40.00%)      | 💀 0/12             |
| [minicpm-v:latest][mi1] mode=markdown                                            | 🟠 8/13 (61.54%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🟠 3/5 (60.00%)      | 💀 0/12             |
| [deepseek-r1:14b][de1] mode=markdown                                             | 🟠 8/13 (61.54%)   | 🟠 2/5 (40.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 🔥 1/12 (8.33%)     |
| [llama3.2:latest][ll1] mode=markdown                                             | 🟡 9/13 (69.23%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llama3.2-vision:latest][ll3] mode=markdown                                      | 🟠 7/13 (53.85%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🟠 3/5 (60.00%)      | 💀 0/12             |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1] mode=markdown                | 🟠 7/13 (53.85%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🟠 2/5 (40.00%)      | 🔥 1/12 (8.33%)     |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1] mode=markdown                     | 🟠 7/13 (53.85%)   | 🔴 1/5 (20.00%)        | 🟠 2/4 (50.00%)  | 💀 0/5               | 🔥 1/12 (8.33%)     |
| [qwen3:0.6b][qw2] mode=native                                                    | 🟠 8/13 (61.54%)   | 💀 0/5                 | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [gemma3:27b][ge2] mode=markdown                                                  | 🟠 7/13 (53.85%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🟠 2/5 (40.00%)      | 💀 0/12             |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3] mode=native                        | 🟡 9/13 (69.23%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [magistral:latest][ma1] mode=markdown                                            | 🟠 8/13 (61.54%)   | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=1.5 mode=native                         | 🟠 6/13 (46.15%)   | 🟠 2/5 (40.00%)        | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llava-llama3:latest][ll4] mode=markdown                                         | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🟠 3/5 (60.00%)      | 💀 0/12             |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr2] mode=markdown                 | 🟡 9/13 (69.23%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [granite3-dense:latest][gr4] mode=native                                         | 🟠 7/13 (53.85%)   | 🟠 2/5 (40.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llava:latest][ll5] mode=markdown                                                | 🟠 6/13 (46.15%)   | 💀 0/5                 | 💀 0/4           | 🟡 4/5 (80.00%)      | 💀 0/12             |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] mode=markdown | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🟠 2/5 (40.00%)      | 💀 0/12             |
| [magistral:latest][ma1] mode=native                                              | 🟠 7/13 (53.85%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llava-phi3:latest][ll6] mode=markdown                                           | 🟠 6/13 (46.15%)   | 💀 0/5                 | 💀 0/4           | 🟠 3/5 (60.00%)      | 💀 0/12             |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1] mode=native                              | 🟠 8/13 (61.54%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [llama2:latest][ll7] mode=markdown                                               | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [qwen3:1.7b][qw2] mode=markdown                                                  | 🟠 6/13 (46.15%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [llama2:7b][ll7] mode=markdown                                                   | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [mistral:latest][mi2] mode=markdown                                              | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [granite3-dense:latest][gr4] mode=markdown                                       | 🟠 6/13 (46.15%)   | 🟠 2/5 (40.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [qwen3:0.6b][qw2] mode=markdown                                                  | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [gemma3:latest][ge2] mode=markdown                                               | 🟠 6/13 (46.15%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [gemma3:12b][ge2] mode=markdown                                                  | 🔴 4/13 (30.77%)   | 💀 0/5                 | 💀 0/4           | 🟡 4/5 (80.00%)      | 💀 0/12             |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3] mode=markdown                          | 🟠 7/13 (53.85%)   | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw6] mode=markdown                    | 🟠 6/13 (46.15%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [bakllava:latest][ba1] mode=markdown                                             | 🔴 3/13 (23.08%)   | 💀 0/5                 | 💀 0/4           | 🟠 3/5 (60.00%)      | 💀 0/12             |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw7] mode=markdown | 🟠 5/13 (38.46%)   | 💀 0/5                 | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/12             |
| [gemma3:1b][ge2] mode=markdown                                                   | 🟠 6/13 (46.15%)   | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1] mode=markdown                            | 🟠 5/13 (38.46%)   | 🔴 1/5 (20.00%)        | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp1] t=2.0 mode=native                         | 🔴 4/13 (30.77%)   | 💀 0/5                 | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/12             |
| [mistral:latest][mi2] mode=native                                                | 🟠 5/13 (38.46%)   | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [gemma3:270m][ge2] mode=markdown                                                 | 🟠 5/13 (38.46%)   | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [deepseek-r1:latest][de1] mode=markdown                                          | 🔴 4/13 (30.77%)   | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3] mode=native                            | 💀 0/13            | 💀 0/5                 | 💀 0/4           | 💀 0/5               | 💀 0/12             |

## Results by task suites

| name                    | PASS         | ALMOST      | FAIL         | ERROR       | TIMEOUT    |   Total |
|:------------------------|:-------------|:------------|:-------------|:------------|:-----------|--------:|
| 🟡 [smoketest][sm1]     | 642 (65.85%) | 0           | 293 (30.05%) | 20 (2.05%)  | 20 (2.05%) |     975 |
| 🔴 [basic_answers][ba2] | 116 (30.93%) | 93 (24.80%) | 145 (38.67%) | 5 (1.33%)   | 16 (4.27%) |     375 |
| 🔴 [hello][he1]         | 91 (30.33%)  | 0           | 188 (62.67%) | 3 (1.00%)   | 18 (6.00%) |     300 |
| 🔴 [smokeimages][sm2]   | 65 (17.33%)  | 0           | 205 (54.67%) | 98 (26.13%) | 7 (1.87%)  |     375 |
| 🔥 [patch_file][pa1]    | 85 (9.44%)   | 0           | 722 (80.22%) | 10 (1.11%)  | 83 (9.22%) |     900 |

## Results by tasks

| name                            | PASS        | ALMOST      | FAIL        | ERROR       | TIMEOUT     |   Total |
|:--------------------------------|:------------|:------------|:------------|:------------|:------------|--------:|
| 🟢 [smoketest][sm1] 05          | 70 (93.33%) | 0           | 4 (5.33%)   | 0           | 1 (1.33%)   |      75 |
| 🟢 [smoketest][sm1] 03          | 68 (90.67%) | 0           | 4 (5.33%)   | 0           | 3 (4.00%)   |      75 |
| 🟢 [smoketest][sm1] 33          | 68 (90.67%) | 0           | 5 (6.67%)   | 1 (1.33%)   | 1 (1.33%)   |      75 |
| 🟡 [smoketest][sm1] 32          | 62 (82.67%) | 0           | 11 (14.67%) | 1 (1.33%)   | 1 (1.33%)   |      75 |
| 🟡 [smoketest][sm1] 04          | 62 (82.67%) | 0           | 12 (16.00%) | 1 (1.33%)   | 0           |      75 |
| 🟡 [smoketest][sm1] 01          | 62 (82.67%) | 0           | 8 (10.67%)  | 3 (4.00%)   | 2 (2.67%)   |      75 |
| 🟡 [smoketest][sm1] 06          | 60 (80.00%) | 0           | 10 (13.33%) | 2 (2.67%)   | 3 (4.00%)   |      75 |
| 🟠 [basic_answers][ba2] 0.paris | 44 (58.67%) | 21 (28.00%) | 6 (8.00%)   | 1 (1.33%)   | 3 (4.00%)   |      75 |
| 🟠 [smoketest][sm1] 02          | 44 (58.67%) | 0           | 23 (30.67%) | 6 (8.00%)   | 2 (2.67%)   |      75 |
| 🟠 [basic_answers][ba2] 4.fact  | 34 (45.33%) | 2 (2.67%)   | 35 (46.67%) | 1 (1.33%)   | 3 (4.00%)   |      75 |
| 🟠 [smoketest][sm1] 12          | 34 (45.33%) | 0           | 38 (50.67%) | 1 (1.33%)   | 2 (2.67%)   |      75 |
| 🟠 [smoketest][sm1] 10          | 32 (42.67%) | 0           | 41 (54.67%) | 1 (1.33%)   | 1 (1.33%)   |      75 |
| 🟠 [smokeimages][sm2] 4         | 32 (42.67%) | 0           | 17 (22.67%) | 24 (32.00%) | 2 (2.67%)   |      75 |
| 🟠 [smoketest][sm1] 13          | 29 (38.67%) | 0           | 44 (58.67%) | 1 (1.33%)   | 1 (1.33%)   |      75 |
| 🟠 [hello][he1] 03git           | 28 (37.33%) | 0           | 41 (54.67%) | 1 (1.33%)   | 5 (6.67%)   |      75 |
| 🟠 [smoketest][sm1] 11          | 27 (36.00%) | 0           | 46 (61.33%) | 1 (1.33%)   | 1 (1.33%)   |      75 |
| 🔴 [smoketest][sm1] 31          | 24 (32.00%) | 0           | 47 (62.67%) | 2 (2.67%)   | 2 (2.67%)   |      75 |
| 🔴 [hello][he1] 02name          | 22 (29.33%) | 0           | 48 (64.00%) | 0           | 5 (6.67%)   |      75 |
| 🔴 [hello][he1] 04gitignore     | 22 (29.33%) | 0           | 47 (62.67%) | 1 (1.33%)   | 5 (6.67%)   |      75 |
| 🔴 [hello][he1] 01world         | 19 (25.33%) | 0           | 52 (69.33%) | 1 (1.33%)   | 3 (4.00%)   |      75 |
| 🔴 [patch_file][pa1] 05python   | 17 (22.67%) | 0           | 55 (73.33%) | 1 (1.33%)   | 2 (2.67%)   |      75 |
| 🔴 [basic_answers][ba2] 1.llme  | 16 (21.33%) | 24 (32.00%) | 30 (40.00%) | 1 (1.33%)   | 4 (5.33%)   |      75 |
| 🔴 [patch_file][pa1] 04ed       | 14 (18.67%) | 0           | 55 (73.33%) | 1 (1.33%)   | 5 (6.67%)   |      75 |
| 🔴 [patch_file][pa1] 00free     | 13 (17.33%) | 0           | 59 (78.67%) | 1 (1.33%)   | 2 (2.67%)   |      75 |
| 🔴 [basic_answers][ba2] 2.llme  | 12 (16.00%) | 23 (30.67%) | 36 (48.00%) | 1 (1.33%)   | 3 (4.00%)   |      75 |
| 🔥 [smokeimages][sm2] 0         | 11 (14.67%) | 0           | 38 (50.67%) | 25 (33.33%) | 1 (1.33%)   |      75 |
| 🔥 [basic_answers][ba2] 3.llme  | 10 (13.33%) | 23 (30.67%) | 38 (50.67%) | 1 (1.33%)   | 3 (4.00%)   |      75 |
| 🔥 [patch_file][pa1] 03patch    | 9 (12.00%)  | 0           | 56 (74.67%) | 1 (1.33%)   | 9 (12.00%)  |      75 |
| 🔥 [smokeimages][sm2] 2         | 9 (12.00%)  | 0           | 42 (56.00%) | 24 (32.00%) | 0           |      75 |
| 🔥 [smokeimages][sm2] 1         | 9 (12.00%)  | 0           | 42 (56.00%) | 24 (32.00%) | 0           |      75 |
| 🔥 [patch_file][pa1] 11cat      | 8 (10.67%)  | 0           | 57 (76.00%) | 0           | 10 (13.33%) |      75 |
| 🔥 [patch_file][pa1] 13patch    | 5 (6.67%)   | 0           | 59 (78.67%) | 0           | 11 (14.67%) |      75 |
| 🔥 [patch_file][pa1] 01cat      | 5 (6.67%)   | 0           | 64 (85.33%) | 1 (1.33%)   | 5 (6.67%)   |      75 |
| 🔥 [patch_file][pa1] 10free     | 4 (5.33%)   | 0           | 61 (81.33%) | 1 (1.33%)   | 9 (12.00%)  |      75 |
| 🔥 [smokeimages][sm2] 3         | 4 (5.33%)   | 0           | 66 (88.00%) | 1 (1.33%)   | 4 (5.33%)   |      75 |
| 🔥 [patch_file][pa1] 02sed      | 4 (5.33%)   | 0           | 68 (90.67%) | 1 (1.33%)   | 2 (2.67%)   |      75 |
| 🔥 [patch_file][pa1] 15python   | 3 (4.00%)   | 0           | 65 (86.67%) | 1 (1.33%)   | 6 (8.00%)   |      75 |
| 🔥 [patch_file][pa1] 12sed      | 2 (2.67%)   | 0           | 64 (85.33%) | 1 (1.33%)   | 8 (10.67%)  |      75 |
| 🔥 [patch_file][pa1] 14ed       | 1 (1.33%)   | 0           | 59 (78.67%) | 1 (1.33%)   | 14 (18.67%) |      75 |


  [gp1]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [qw1]: https://ollama.com/library/qwen3-coder
  [gr1]: https://huggingface.co/unsloth/granite-4.0-h-small-GGUF
  [qw2]: https://ollama.com/library/qwen3
  [gp2]: https://ollama.com/library/gpt-oss
  [ge1]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [Qw1]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [Qw2]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [Qw3]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [Qw4]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [gr2]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [Qw5]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [Ma1]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [Mi1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [qw3]: https://ollama.com/library/qwen2.5vl
  [ll1]: https://ollama.com/library/llama3.2
  [ll2]: https://ollama.com/library/llama3
  [mi1]: https://ollama.com/library/minicpm-v
  [de1]: https://ollama.com/library/deepseek-r1
  [ll3]: https://ollama.com/library/llama3.2-vision
  [ge2]: https://ollama.com/library/gemma3
  [gr3]: https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF
  [ma1]: https://ollama.com/library/magistral
  [ll4]: https://ollama.com/library/llava-llama3
  [gr4]: https://ollama.com/library/granite3-dense
  [ll5]: https://ollama.com/library/llava
  [ll6]: https://ollama.com/library/llava-phi3
  [LF1]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [ll7]: https://ollama.com/library/llama2
  [mi2]: https://ollama.com/library/mistral
  [ge3]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [Qw6]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [ba1]: https://ollama.com/library/bakllava
  [Qw7]: https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [sm1]: tests/smoketest.sh
  [ba2]: tests/basic_answers.sh
  [he1]: tests/hello.sh
  [sm2]: tests/smokeimages.sh
  [pa1]: tests/patch_file.sh

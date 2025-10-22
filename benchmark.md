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

<!-- the contents bellow this line are generated -->

* 61 models and configurations
* 5 test suites
* 39 test cases

## Results by models

| Model                                                                       | PASS        | ALMOST     | FAIL        | ERROR      | TIMEOUT     |   Total |
|:----------------------------------------------------------------------------|:------------|:-----------|:------------|:-----------|:------------|--------:|
| 🟡 [qwen3-coder:30b][qw1]                                                   | 29 (74.36%) | 0          | 7 (17.95%)  | 0          | 3 (7.69%)   |      39 |
| 🟡 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1]       | 25 (64.10%) | 5 (12.82%) | 7 (17.95%)  | 0          | 2 (5.13%)   |      39 |
| 🟠 [qwen3:14b][qw2]                                                         | 20 (51.28%) | 2 (5.13%)  | 7 (17.95%)  | 0          | 10 (25.64%) |      39 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=0.0 | 19 (48.72%) | 4 (10.26%) | 11 (28.21%) | 0          | 5 (12.82%)  |      39 |
| 🟠 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                      | 19 (48.72%) | 4 (10.26%) | 10 (25.64%) | 0          | 6 (15.38%)  |      39 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=0.5 | 19 (48.72%) | 4 (10.26%) | 11 (28.21%) | 0          | 5 (12.82%)  |      39 |
| 🟠 [qwen3:30b][qw2]                                                         | 19 (48.72%) | 1 (2.56%)  | 7 (17.95%)  | 0          | 12 (30.77%) |      39 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=1.5 | 18 (46.15%) | 4 (10.26%) | 14 (35.90%) | 0          | 3 (7.69%)   |      39 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]                   | 18 (46.15%) | 2 (5.13%)  | 3 (7.69%)   | 4 (10.26%) | 12 (30.77%) |      39 |
| 🟠 [qwen3:latest][qw2]                                                      | 16 (41.03%) | 1 (2.56%)  | 12 (30.77%) | 0          | 10 (25.64%) |      39 |
| 🟠 [llama3.2-vision:latest][ll1]                                            | 16 (41.03%) | 1 (2.56%)  | 21 (53.85%) | 0          | 1 (2.56%)   |      39 |
| 🟠 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw3]                               | 16 (41.03%) | 0          | 23 (58.97%) | 0          | 0           |      39 |
| 🟠 [magistral:latest][ma1]                                                  | 15 (38.46%) | 3 (7.69%)  | 19 (48.72%) | 0          | 2 (5.13%)   |      39 |
| 🟠 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                        | 15 (38.46%) | 2 (5.13%)  | 18 (46.15%) | 4 (10.26%) | 0           |      39 |
| 🟠 [qwen3:32b][qw2]                                                         | 15 (38.46%) | 1 (2.56%)  | 6 (15.38%)  | 0          | 17 (43.59%) |      39 |
| 🟠 [qwen2.5vl:latest][qw4]                                                  | 14 (35.90%) | 0          | 25 (64.10%) | 0          | 0           |      39 |
| 🟠 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw5]                               | 14 (35.90%) | 0          | 24 (61.54%) | 1 (2.56%)  | 0           |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=2.0             | 13 (33.33%) | 4 (10.26%) | 15 (38.46%) | 0          | 7 (17.95%)  |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=1.0             | 13 (33.33%) | 4 (10.26%) | 11 (28.21%) | 0          | 11 (28.21%) |      39 |
| 🔴 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]                  | 13 (33.33%) | 4 (10.26%) | 11 (28.21%) | 4 (10.26%) | 7 (17.95%)  |      39 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=2.0 | 13 (33.33%) | 3 (7.69%)  | 18 (46.15%) | 0          | 5 (12.82%)  |      39 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=1.0 | 13 (33.33%) | 3 (7.69%)  | 12 (30.77%) | 0          | 11 (28.21%) |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=0.5             | 13 (33.33%) | 3 (7.69%)  | 14 (35.90%) | 1 (2.56%)  | 8 (20.51%)  |      39 |
| 🔴 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                            | 13 (33.33%) | 3 (7.69%)  | 17 (43.59%) | 4 (10.26%) | 2 (5.13%)   |      39 |
| 🔴 [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4]       | 13 (33.33%) | 1 (2.56%)  | 11 (28.21%) | 4 (10.26%) | 10 (25.64%) |      39 |
| 🔴 [gemma3:latest][ge2]                                                     | 13 (33.33%) | 0          | 19 (48.72%) | 1 (2.56%)  | 6 (15.38%)  |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=1.5             | 12 (30.77%) | 4 (10.26%) | 14 (35.90%) | 0          | 9 (23.08%)  |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=0.0             | 12 (30.77%) | 4 (10.26%) | 13 (33.33%) | 0          | 10 (25.64%) |      39 |
| 🔴 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                        | 12 (30.77%) | 3 (7.69%)  | 12 (30.77%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🔴 [llava-phi3:latest][ll2]                                                 | 12 (30.77%) | 2 (5.13%)  | 25 (64.10%) | 0          | 0           |      39 |
| 🔴 [qwen3:4b][qw2]                                                          | 12 (30.77%) | 0          | 14 (35.90%) | 0          | 13 (33.33%) |      39 |
| 🔴 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                           | 11 (28.21%) | 5 (12.82%) | 11 (28.21%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🔴 [granite3-dense:latest][gr2]                                             | 11 (28.21%) | 3 (7.69%)  | 24 (61.54%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [llama3:latest][ll3]                                                     | 11 (28.21%) | 2 (5.13%)  | 24 (61.54%) | 0          | 2 (5.13%)   |      39 |
| 🔴 [llama3.2:latest][ll4]                                                   | 11 (28.21%) | 1 (2.56%)  | 25 (64.10%) | 1 (2.56%)  | 1 (2.56%)   |      39 |
| 🔴 [NexaAI/gpt-oss-20b-MLX-4bit][gp1]                                       | 10 (25.64%) | 4 (10.26%) | 23 (58.97%) | 0          | 2 (5.13%)   |      39 |
| 🔴 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                                 | 10 (25.64%) | 4 (10.26%) | 13 (33.33%) | 4 (10.26%) | 8 (20.51%)  |      39 |
| 🔴 [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                          | 10 (25.64%) | 3 (7.69%)  | 15 (38.46%) | 4 (10.26%) | 7 (17.95%)  |      39 |
| 🔴 [gemma3:12b][ge2]                                                        | 10 (25.64%) | 1 (2.56%)  | 28 (71.79%) | 0          | 0           |      39 |
| 🔴 [llama2:7b][ll5]                                                         | 10 (25.64%) | 0          | 29 (74.36%) | 0          | 0           |      39 |
| 🔴 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                                  | 10 (25.64%) | 0          | 25 (64.10%) | 4 (10.26%) | 0           |      39 |
| 🔴 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                            | 9 (23.08%)  | 4 (10.26%) | 8 (20.51%)  | 6 (15.38%) | 12 (30.77%) |      39 |
| 🔴 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                       | 9 (23.08%)  | 2 (5.13%)  | 24 (61.54%) | 4 (10.26%) | 0           |      39 |
| 🔴 [mistral:latest][mi1]                                                    | 9 (23.08%)  | 1 (2.56%)  | 28 (71.79%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [llava-llama3:latest][ll6]                                               | 9 (23.08%)  | 0          | 30 (76.92%) | 0          | 0           |      39 |
| 🔴 [llava:latest][ll7]                                                      | 9 (23.08%)  | 0          | 30 (76.92%) | 0          | 0           |      39 |
| 🔴 [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                          | 8 (20.51%)  | 4 (10.26%) | 26 (66.67%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp2]                                  | 8 (20.51%)  | 3 (7.69%)  | 24 (61.54%) | 4 (10.26%) | 0           |      39 |
| 🔴 [minicpm-v:latest][mi2]                                                  | 8 (20.51%)  | 1 (2.56%)  | 29 (74.36%) | 0          | 1 (2.56%)   |      39 |
| 🔴 [unsloth/gpt-oss-120b-GGUF][gp2]                                         | 8 (20.51%)  | 1 (2.56%)  | 26 (66.67%) | 4 (10.26%) | 0           |      39 |
| 🔴 [llama2:latest][ll5]                                                     | 8 (20.51%)  | 0          | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [qwen3:0.6b][qw2]                                                        | 7 (17.95%)  | 1 (2.56%)  | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [bakllava:latest][ba1]                                                   | 7 (17.95%)  | 1 (2.56%)  | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [gemma3:1b][ge2]                                                         | 7 (17.95%)  | 1 (2.56%)  | 31 (79.49%) | 0          | 0           |      39 |
| 🔴 [qwen3:1.7b][qw2]                                                        | 7 (17.95%)  | 1 (2.56%)  | 26 (66.67%) | 1 (2.56%)  | 4 (10.26%)  |      39 |
| 🔴 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp3]                                   | 7 (17.95%)  | 1 (2.56%)  | 24 (61.54%) | 4 (10.26%) | 3 (7.69%)   |      39 |
| 🔴 [deepseek-r1:14b][de1]                                                   | 7 (17.95%)  | 0          | 6 (15.38%)  | 0          | 26 (66.67%) |      39 |
| 🔥 [gemma3:270m][ge2]                                                       | 5 (12.82%)  | 1 (2.56%)  | 33 (84.62%) | 0          | 0           |      39 |
| 🔥 [gpt-oss:latest][gp4]                                                    | 4 (10.26%)  | 0          | 35 (89.74%) | 0          | 0           |      39 |
| 🔥 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                                | 2 (5.13%)   | 2 (5.13%)  | 14 (35.90%) | 5 (12.82%) | 16 (41.03%) |      39 |
| 🔥 [deepseek-r1:latest][de1]                                                | 2 (5.13%)   | 1 (2.56%)  | 5 (12.82%)  | 0          | 31 (79.49%) |      39 |

## Testsuites by models

| Models                                                                   | [smoketest][sm1]   | [hello][he1]     | [smokeimages][sm2]   | [basic_answers][ba2]   | [patch_file][pa1]   |
|:-------------------------------------------------------------------------|:-------------------|:-----------------|:---------------------|:-----------------------|:--------------------|
| [qwen3-coder:30b][qw1]                                                   | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 💎 5/5 (100.00%)       | 🟠 7/12 (58.33%)    |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1]       | 💎 13/13 (100.00%) | 💎 4/4 (100.00%) | 🟡 3/5 (60.00%)      | 💀 0/5                 | 🟠 5/12 (41.67%)    |
| [qwen3:14b][qw2]                                                         | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 🔴 1/5 (20.00%)      | 🟠 2/5 (40.00%)        | 🔴 4/12 (33.33%)    |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=0.0 | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 🟡 4/5 (80.00%)      | 💀 0/5                 | 🔥 1/12 (8.33%)     |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                      | 🟡 11/13 (84.62%)  | 💎 4/4 (100.00%) | 🔴 1/5 (20.00%)      | 💀 0/5                 | 🔴 3/12 (25.00%)    |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=0.5 | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)      | 💀 0/5                 | 🔴 3/12 (25.00%)    |
| [qwen3:30b][qw2]                                                         | 🟡 10/13 (76.92%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 🟡 3/5 (60.00%)        | 🔴 4/12 (33.33%)    |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=1.5 | 🟡 11/13 (84.62%)  | 💎 4/4 (100.00%) | 🟠 2/5 (40.00%)      | 💀 0/5                 | 🔥 1/12 (8.33%)     |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]                   | 💎 13/13 (100.00%) | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)      | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [qwen3:latest][qw2]                                                      | 💎 13/13 (100.00%) | 🔴 1/4 (25.00%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔥 1/12 (8.33%)     |
| [llama3.2-vision:latest][ll1]                                            | 🟡 11/13 (84.62%)  | 💀 0/4           | 🟡 3/5 (60.00%)      | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw3]                               | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 🟡 3/5 (60.00%)        | 💀 0/12             |
| [magistral:latest][ma1]                                                  | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 🔴 1/5 (20.00%)      | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                        | 🟢 12/13 (92.31%)  | 🔴 1/4 (25.00%)  | 💀 0/5               | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [qwen3:32b][qw2]                                                         | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔥 1/12 (8.33%)     |
| [qwen2.5vl:latest][qw4]                                                  | 🟡 9/13 (69.23%)   | 💀 0/4           | 🟡 4/5 (80.00%)      | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw5]                               | 🟡 11/13 (84.62%)  | 💀 0/4           | 🔴 1/5 (20.00%)      | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=2.0             | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=1.0             | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]                  | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=2.0 | 🟠 5/13 (38.46%)   | 💎 4/4 (100.00%) | 🟡 3/5 (60.00%)      | 💀 0/5                 | 🔥 1/12 (8.33%)     |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] t=1.0 | 🟡 9/13 (69.23%)   | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/5                 | 🔥 1/12 (8.33%)     |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=0.5             | 🟢 12/13 (92.31%)  | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                            | 🟡 9/13 (69.23%)   | 🟠 2/4 (50.00%)  | 💀 0/5               | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4]       | 🟡 10/13 (76.92%)  | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/5                 | 🔴 2/12 (16.67%)    |
| [gemma3:latest][ge2]                                                     | 🟠 7/13 (53.85%)   | 🔴 1/4 (25.00%)  | 🟡 3/5 (60.00%)      | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=1.5             | 🟡 10/13 (76.92%)  | 🟠 2/4 (50.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1] t=0.0             | 🟡 9/13 (69.23%)   | 🟡 3/4 (75.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                        | 🟡 11/13 (84.62%)  | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [llava-phi3:latest][ll2]                                                 | 🟡 9/13 (69.23%)   | 💀 0/4           | 🟡 3/5 (60.00%)      | 💀 0/5                 | 💀 0/12             |
| [qwen3:4b][qw2]                                                          | 🟡 8/13 (61.54%)   | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔴 3/12 (25.00%)    |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                           | 🟡 9/13 (69.23%)   | 🟠 2/4 (50.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [granite3-dense:latest][gr2]                                             | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [llama3:latest][ll3]                                                     | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [llama3.2:latest][ll4]                                                   | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [NexaAI/gpt-oss-20b-MLX-4bit][gp1]                                       | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                                 | 🟠 7/13 (53.85%)   | 🔴 1/4 (25.00%)  | 💀 0/5               | 🔴 1/5 (20.00%)        | 🔥 1/12 (8.33%)     |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                          | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [gemma3:12b][ge2]                                                        | 🟠 7/13 (53.85%)   | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)      | 💀 0/5                 | 💀 0/12             |
| [llama2:7b][ll5]                                                         | 🟡 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)      | 💀 0/5                 | 💀 0/12             |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                                  | 🟡 8/13 (61.54%)   | 💀 0/4           | 💀 0/5               | 🟠 2/5 (40.00%)        | 💀 0/12             |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                            | 🟡 9/13 (69.23%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                       | 🟡 9/13 (69.23%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [mistral:latest][mi1]                                                    | 🟡 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💀 0/12             |
| [llava-llama3:latest][ll6]                                               | 🟠 5/13 (38.46%)   | 💀 0/4           | 🟡 3/5 (60.00%)      | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [llava:latest][ll7]                                                      | 🟠 5/13 (38.46%)   | 💀 0/4           | 🟡 4/5 (80.00%)      | 💀 0/5                 | 💀 0/12             |
| [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                          | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp2]                                  | 🟡 8/13 (61.54%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [minicpm-v:latest][mi2]                                                  | 🔴 4/13 (30.77%)   | 💀 0/4           | 🟡 3/5 (60.00%)      | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [unsloth/gpt-oss-120b-GGUF][gp2]                                         | 🟡 8/13 (61.54%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [llama2:latest][ll5]                                                     | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)      | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [qwen3:0.6b][qw2]                                                        | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💀 0/12             |
| [bakllava:latest][ba1]                                                   | 🔴 3/13 (23.08%)   | 💀 0/4           | 🟡 4/5 (80.00%)      | 💀 0/5                 | 💀 0/12             |
| [gemma3:1b][ge2]                                                         | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [qwen3:1.7b][qw2]                                                        | 🟠 6/13 (46.15%)   | 🔴 1/4 (25.00%)  | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp3]                                   | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [deepseek-r1:14b][de1]                                                   | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [gemma3:270m][ge2]                                                       | 🟠 5/13 (38.46%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [gpt-oss:latest][gp4]                                                    | 🔴 3/13 (23.08%)   | 💀 0/4           | 💀 0/5               | 🔴 1/5 (20.00%)        | 💀 0/12             |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                                | 🔴 2/13 (15.38%)   | 💀 0/4           | 💀 0/5               | 💀 0/5                 | 💀 0/12             |
| [deepseek-r1:latest][de1]                                                | 🔥 1/13 (7.69%)    | 💀 0/4           | 🔴 1/5 (20.00%)      | 💀 0/5                 | 💀 0/12             |

## Results by test suites

| Test suites             | PASS         | ALMOST       | FAIL         | ERROR       | TIMEOUT      |   Total |
|:------------------------|:-------------|:-------------|:-------------|:------------|:-------------|--------:|
| 🟡 [smoketest][sm1]     | 524 (66.08%) | 0            | 173 (21.82%) | 4 (0.50%)   | 92 (11.60%)  |     793 |
| 🔴 [hello][he1]         | 68 (27.87%)  | 0            | 136 (55.74%) | 0           | 40 (16.39%)  |     244 |
| 🔴 [smokeimages][sm2]   | 55 (18.03%)  | 0            | 163 (53.44%) | 67 (21.97%) | 20 (6.56%)   |     305 |
| 🔥 [basic_answers][ba2] | 43 (14.10%)  | 120 (39.34%) | 112 (36.72%) | 0           | 30 (9.84%)   |     305 |
| 🔥 [patch_file][pa1]    | 38 (5.19%)   | 0            | 556 (75.96%) | 1 (0.14%)   | 137 (18.72%) |     732 |

## Results by test cases

| Test case                       | PASS        | ALMOST      | FAIL        | ERROR       | TIMEOUT     |   Total |
|:--------------------------------|:------------|:------------|:------------|:------------|:------------|--------:|
| 🟢 [smoketest][sm1] 03          | 56 (91.80%) | 0           | 2 (3.28%)   | 0           | 3 (4.92%)   |      61 |
| 🟢 [smoketest][sm1] 04          | 52 (85.25%) | 0           | 6 (9.84%)   | 0           | 3 (4.92%)   |      61 |
| 🟡 [smoketest][sm1] 05          | 50 (81.97%) | 0           | 3 (4.92%)   | 0           | 8 (13.11%)  |      61 |
| 🟡 [smoketest][sm1] 32          | 48 (78.69%) | 0           | 5 (8.20%)   | 0           | 8 (13.11%)  |      61 |
| 🟡 [smoketest][sm1] 33          | 48 (78.69%) | 0           | 8 (13.11%)  | 1 (1.64%)   | 4 (6.56%)   |      61 |
| 🟡 [smoketest][sm1] 06          | 46 (75.41%) | 0           | 5 (8.20%)   | 0           | 10 (16.39%) |      61 |
| 🟡 [smoketest][sm1] 01          | 39 (63.93%) | 0           | 7 (11.48%)  | 1 (1.64%)   | 14 (22.95%) |      61 |
| 🟡 [smoketest][sm1] 11          | 38 (62.30%) | 0           | 22 (36.07%) | 0           | 1 (1.64%)   |      61 |
| 🟠 [smoketest][sm1] 13          | 34 (55.74%) | 0           | 24 (39.34%) | 0           | 3 (4.92%)   |      61 |
| 🟠 [smoketest][sm1] 12          | 33 (54.10%) | 0           | 25 (40.98%) | 0           | 3 (4.92%)   |      61 |
| 🟠 [smoketest][sm1] 10          | 29 (47.54%) | 0           | 31 (50.82%) | 0           | 1 (1.64%)   |      61 |
| 🟠 [smoketest][sm1] 31          | 27 (44.26%) | 0           | 24 (39.34%) | 0           | 10 (16.39%) |      61 |
| 🟠 [hello][he1] 03git           | 24 (39.34%) | 0           | 30 (49.18%) | 0           | 7 (11.48%)  |      61 |
| 🟠 [smoketest][sm1] 02          | 24 (39.34%) | 0           | 11 (18.03%) | 2 (3.28%)   | 24 (39.34%) |      61 |
| 🔴 [smokeimages][sm2] 4         | 20 (32.79%) | 0           | 19 (31.15%) | 16 (26.23%) | 6 (9.84%)   |      61 |
| 🔴 [basic_answers][ba2] 0.paris | 19 (31.15%) | 34 (55.74%) | 4 (6.56%)   | 0           | 4 (6.56%)   |      61 |
| 🔴 [basic_answers][ba2] 4.fact  | 18 (29.51%) | 16 (26.23%) | 24 (39.34%) | 0           | 3 (4.92%)   |      61 |
| 🔴 [hello][he1] 01world         | 16 (26.23%) | 0           | 40 (65.57%) | 0           | 5 (8.20%)   |      61 |
| 🔴 [hello][he1] 02name          | 15 (24.59%) | 0           | 32 (52.46%) | 0           | 14 (22.95%) |      61 |
| 🔴 [smokeimages][sm2] 2         | 14 (22.95%) | 0           | 29 (47.54%) | 16 (26.23%) | 2 (3.28%)   |      61 |
| 🔴 [hello][he1] 04gitignore     | 13 (21.31%) | 0           | 34 (55.74%) | 0           | 14 (22.95%) |      61 |
| 🔴 [smokeimages][sm2] 0         | 11 (18.03%) | 0           | 32 (52.46%) | 16 (26.23%) | 2 (3.28%)   |      61 |
| 🔥 [patch_file][pa1] 05python   | 9 (14.75%)  | 0           | 47 (77.05%) | 0           | 5 (8.20%)   |      61 |
| 🔥 [patch_file][pa1] 04ed       | 9 (14.75%)  | 0           | 38 (62.30%) | 0           | 14 (22.95%) |      61 |
| 🔥 [smokeimages][sm2] 1         | 9 (14.75%)  | 0           | 33 (54.10%) | 17 (27.87%) | 2 (3.28%)   |      61 |
| 🔥 [patch_file][pa1] 03patch    | 6 (9.84%)   | 0           | 47 (77.05%) | 0           | 8 (13.11%)  |      61 |
| 🔥 [patch_file][pa1] 01cat      | 5 (8.20%)   | 0           | 47 (77.05%) | 0           | 9 (14.75%)  |      61 |
| 🔥 [patch_file][pa1] 02sed      | 4 (6.56%)   | 0           | 48 (78.69%) | 0           | 9 (14.75%)  |      61 |
| 🔥 [patch_file][pa1] 00free     | 4 (6.56%)   | 0           | 51 (83.61%) | 0           | 6 (9.84%)   |      61 |
| 🔥 [basic_answers][ba2] 2.llme  | 2 (3.28%)   | 25 (40.98%) | 27 (44.26%) | 0           | 7 (11.48%)  |      61 |
| 🔥 [basic_answers][ba2] 3.llme  | 2 (3.28%)   | 25 (40.98%) | 27 (44.26%) | 0           | 7 (11.48%)  |      61 |
| 🔥 [basic_answers][ba2] 1.llme  | 2 (3.28%)   | 20 (32.79%) | 30 (49.18%) | 0           | 9 (14.75%)  |      61 |
| 🔥 [patch_file][pa1] 11cat      | 1 (1.64%)   | 0           | 47 (77.05%) | 0           | 13 (21.31%) |      61 |
| 🔥 [smokeimages][sm2] 3         | 1 (1.64%)   | 0           | 50 (81.97%) | 2 (3.28%)   | 8 (13.11%)  |      61 |
| 💀 [patch_file][pa1] 10free     | 0           | 0           | 45 (73.77%) | 0           | 16 (26.23%) |      61 |
| 💀 [patch_file][pa1] 15python   | 0           | 0           | 45 (73.77%) | 0           | 16 (26.23%) |      61 |
| 💀 [patch_file][pa1] 13patch    | 0           | 0           | 46 (75.41%) | 0           | 15 (24.59%) |      61 |
| 💀 [patch_file][pa1] 12sed      | 0           | 0           | 49 (80.33%) | 0           | 12 (19.67%) |      61 |
| 💀 [patch_file][pa1] 14ed       | 0           | 0           | 46 (75.41%) | 1 (1.64%)   | 14 (22.95%) |      61 |


  [qw1]: https://ollama.com/library/qwen3-coder
  [Mi1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [qw2]: https://ollama.com/library/qwen3
  [Ma1]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [Qw1]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [ll1]: https://ollama.com/library/llama3.2-vision
  [qw3]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [ma1]: https://ollama.com/library/magistral
  [Qw2]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [qw4]: https://ollama.com/library/qwen2.5vl
  [qw5]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [Qw3]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [ge1]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [Qw4]: https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [ge2]: https://ollama.com/library/gemma3
  [Qw5]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [ll2]: https://ollama.com/library/llava-phi3
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
  [he1]: tests/hello.sh
  [sm2]: tests/smokeimages.sh
  [ba2]: tests/basic_answers.sh
  [pa1]: tests/patch_file.sh

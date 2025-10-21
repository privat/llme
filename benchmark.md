# Model Results

This is a preliminary benchmark of some local models.
The [testsuites](tests) tries to highlight the usage and features of llme.
The ranking should not be considered fair or rigorous since many uncontrolled variables (still) impact it.

The benchmark is also used to check the API compatibility with local LLM servers.

Most models come from the huggingface.
GUFF models are served by llama.cpp (and llama-swap).
MLX models are served by nexa.
The others models come from the ollama repository and are served by the ollama server.

<!-- the contents bellow this line are generated -->

* 43 models
* 6 testsuites
* 40 tests

## Results by models

| Model                                                                 | PASS        | ALMOST     | FAIL        | ERROR      | TIMEOUT     |   Total |
|:----------------------------------------------------------------------|:------------|:-----------|:------------|:-----------|:------------|--------:|
| 🟡 [qwen3-coder:30b][qw1]                                             | 30 (75.00%) | 0          | 7 (17.50%)  | 0          | 3 (7.50%)   |      40 |
| 🟡 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] | 23 (60.53%) | 5 (13.16%) | 8 (21.05%)  | 0          | 2 (5.26%)   |      38 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]             | 19 (47.50%) | 2 (5.00%)  | 3 (7.50%)   | 4 (10.00%) | 12 (30.00%) |      40 |
| 🟠 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                | 18 (48.65%) | 4 (10.81%) | 9 (24.32%)  | 0          | 6 (16.22%)  |      37 |
| 🟠 [llama3.2-vision:latest][ll1]                                      | 17 (42.50%) | 1 (2.50%)  | 21 (52.50%) | 0          | 1 (2.50%)   |      40 |
| 🟠 [qwen3:latest][qw2]                                                | 17 (42.50%) | 1 (2.50%)  | 12 (30.00%) | 0          | 10 (25.00%) |      40 |
| 🟠 [magistral:latest][ma1]                                            | 16 (41.03%) | 3 (7.69%)  | 17 (43.59%) | 0          | 3 (7.69%)   |      39 |
| 🟠 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                  | 16 (40.00%) | 2 (5.00%)  | 18 (45.00%) | 4 (10.00%) | 0           |      40 |
| 🟠 [qwen2.5vl:latest][qw3]                                            | 15 (37.50%) | 0          | 25 (62.50%) | 0          | 0           |      40 |
| 🟠 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]            | 14 (35.00%) | 4 (10.00%) | 11 (27.50%) | 4 (10.00%) | 7 (17.50%)  |      40 |
| 🟠 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                      | 14 (35.00%) | 3 (7.50%)  | 17 (42.50%) | 4 (10.00%) | 2 (5.00%)   |      40 |
| 🟠 [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4] | 14 (35.00%) | 1 (2.50%)  | 11 (27.50%) | 4 (10.00%) | 10 (25.00%) |      40 |
| 🟠 [gemma3:latest][ge2]                                               | 14 (35.00%) | 0          | 19 (47.50%) | 1 (2.50%)  | 6 (15.00%)  |      40 |
| 🟠 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                  | 13 (32.50%) | 3 (7.50%)  | 12 (30.00%) | 4 (10.00%) | 8 (20.00%)  |      40 |
| 🟠 [llava-phi3:latest][ll2]                                           | 13 (32.50%) | 2 (5.00%)  | 25 (62.50%) | 0          | 0           |      40 |
| 🟠 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                     | 12 (30.00%) | 5 (12.50%) | 11 (27.50%) | 4 (10.00%) | 8 (20.00%)  |      40 |
| 🟠 [granite3-dense:latest][gr2]                                       | 12 (30.00%) | 3 (7.50%)  | 24 (60.00%) | 0          | 1 (2.50%)   |      40 |
| 🟠 [llama3:latest][ll3]                                               | 12 (30.00%) | 2 (5.00%)  | 24 (60.00%) | 0          | 2 (5.00%)   |      40 |
| 🟠 [llama3.2:latest][ll4]                                             | 12 (30.00%) | 1 (2.50%)  | 25 (62.50%) | 1 (2.50%)  | 1 (2.50%)   |      40 |
| 🟠 [qwen3:4b][qw2]                                                    | 12 (30.00%) | 0          | 12 (30.00%) | 0          | 16 (40.00%) |      40 |
| 🟠 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                           | 11 (27.50%) | 4 (10.00%) | 13 (32.50%) | 4 (10.00%) | 8 (20.00%)  |      40 |
| 🟠 [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                    | 11 (28.21%) | 3 (7.69%)  | 17 (43.59%) | 4 (10.26%) | 4 (10.26%)  |      39 |
| 🟠 [llama2:7b][ll5]                                                   | 11 (27.50%) | 0          | 29 (72.50%) | 0          | 0           |      40 |
| 🟠 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                            | 11 (27.50%) | 0          | 25 (62.50%) | 4 (10.00%) | 0           |      40 |
| 🟠 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                      | 10 (25.00%) | 4 (10.00%) | 8 (20.00%)  | 6 (15.00%) | 12 (30.00%) |      40 |
| 🟠 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                 | 10 (25.00%) | 2 (5.00%)  | 24 (60.00%) | 4 (10.00%) | 0           |      40 |
| 🟠 [mistral:latest][mi1]                                              | 10 (26.32%) | 1 (2.63%)  | 25 (65.79%) | 1 (2.63%)  | 1 (2.63%)   |      38 |
| 🟠 [llava-llama3:latest][ll6]                                         | 10 (25.00%) | 0          | 30 (75.00%) | 0          | 0           |      40 |
| 🟠 [llava:latest][ll7]                                                | 10 (25.00%) | 0          | 30 (75.00%) | 0          | 0           |      40 |
| 🟠 [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp1]                            | 9 (22.50%)  | 3 (7.50%)  | 24 (60.00%) | 4 (10.00%) | 0           |      40 |
| 🟠 [minicpm-v:latest][mi2]                                            | 9 (22.50%)  | 1 (2.50%)  | 29 (72.50%) | 0          | 1 (2.50%)   |      40 |
| 🟠 [unsloth/gpt-oss-120b-GGUF][gp1]                                   | 9 (22.50%)  | 1 (2.50%)  | 26 (65.00%) | 4 (10.00%) | 0           |      40 |
| 🟠 [llama2:latest][ll5]                                               | 9 (22.50%)  | 0          | 31 (77.50%) | 0          | 0           |      40 |
| 🟠 [bakllava:latest][ba1]                                             | 8 (20.00%)  | 1 (2.50%)  | 31 (77.50%) | 0          | 0           |      40 |
| 🟠 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp2]                             | 8 (21.05%)  | 1 (2.63%)  | 24 (63.16%) | 4 (10.53%) | 1 (2.63%)   |      38 |
| 🟠 [deepseek-r1:14b][de1]                                             | 8 (20.00%)  | 0          | 6 (15.00%)  | 0          | 26 (65.00%) |      40 |
| 🟠 [gpt-oss:latest][gp3]                                              | 5 (12.50%)  | 0          | 35 (87.50%) | 0          | 0           |      40 |
| 🟠 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                          | 3 (7.50%)   | 2 (5.00%)  | 14 (35.00%) | 5 (12.50%) | 16 (40.00%) |      40 |
| 🟠 [deepseek-r1:latest][de1]                                          | 2 (5.26%)   | 1 (2.63%)  | 4 (10.53%)  | 0          | 31 (81.58%) |      38 |
| 🟠 [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                    | 1 (2.63%)   | 0          | 21 (55.26%) | 0          | 16 (42.11%) |      38 |
| 🟠 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw4]                         | 1 (2.63%)   | 0          | 36 (94.74%) | 1 (2.63%)  | 0           |      38 |
| 🟠 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw5]                         | 1 (2.63%)   | 0          | 36 (94.74%) | 1 (2.63%)  | 0           |      38 |
| 🟠 [NexaAI/gpt-oss-20b-MLX-4bit][gp4]                                 | 1 (2.63%)   | 0          | 32 (84.21%) | 5 (13.16%) | 0           |      38 |

## Testsuites by models

| Models                                                             | [smoketest][sm1]   | [test_utils][te1]   | [smokeimages][sm2]   | [basic_answers][ba2]   | [hello][he1]   | [patch_file][pa1]   |
|:-------------------------------------------------------------------|:-------------------|:--------------------|:---------------------|:-----------------------|:---------------|:--------------------|
| [qwen3-coder:30b][qw1]                                             | 🟡 12 (92.31%)     | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🟢 5 (100.00%)         | 🟢 4 (100.00%) | 🟡 7 (58.33%)       |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][Mi1] | 🟢 13 (100.00%)    | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🔴 0 (0.00%)           | 🟢 2 (100.00%) | 🟠 4 (33.33%)       |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][Qw1]             | 🟢 13 (100.00%)    | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🟠 2 (40.00%)          | 🟡 2 (50.00%)  | 🔴 0 (0.00%)        |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][Ma1]                | 🟡 11 (91.67%)     | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🔴 0 (0.00%)           | 🟢 2 (100.00%) | 🟠 3 (25.00%)       |
| [llama3.2-vision:latest][ll1]                                      | 🟡 11 (84.62%)     | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🟠 2 (40.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [qwen3:latest][qw2]                                                | 🟢 13 (100.00%)    | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🟠 1 (25.00%)  | 🟠 1 (8.33%)        |
| [magistral:latest][ma1]                                            | 🟡 12 (85.71%)     | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🟠 1 (20.00%)          | 🟡 1 (50.00%)  | 🔴 0 (0.00%)        |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][Qw2]                  | 🟡 12 (92.31%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 2 (40.00%)          | 🟠 1 (25.00%)  | 🔴 0 (0.00%)        |
| [qwen2.5vl:latest][qw3]                                            | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🟡 4 (80.00%)        | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw3]            | 🟡 10 (76.92%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🟡 3 (75.00%)  | 🔴 0 (0.00%)        |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][ge1]                      | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 2 (40.00%)          | 🟡 2 (50.00%)  | 🔴 0 (0.00%)        |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][Qw4] | 🟡 10 (76.92%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🟠 1 (25.00%)  | 🟠 2 (16.67%)       |
| [gemma3:latest][ge2]                                               | 🟡 7 (53.85%)      | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🟠 2 (40.00%)          | 🟠 1 (25.00%)  | 🔴 0 (0.00%)        |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][Qw5]                  | 🟡 11 (84.62%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llava-phi3:latest][ll2]                                           | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gr1]                     | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🟡 2 (50.00%)  | 🔴 0 (0.00%)        |
| [granite3-dense:latest][gr2]                                       | 🟡 10 (76.92%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llama3:latest][ll3]                                               | 🟡 10 (76.92%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llama3.2:latest][ll4]                                             | 🟡 10 (76.92%)     | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [qwen3:4b][qw2]                                                    | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 2 (40.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][Qw6]                           | 🟡 7 (53.85%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🟠 1 (25.00%)  | 🟠 1 (8.33%)        |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][Qw7]                    | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🟠 1 (33.33%)  | 🔴 0 (0.00%)        |
| [llama2:7b][ll5]                                                   | 🟡 8 (61.54%)      | 🟢 1 (100.00%)      | 🟠 2 (40.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][LF1]                            | 🟡 8 (61.54%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 2 (40.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gr3]                      | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gr4]                 | 🟡 9 (69.23%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [mistral:latest][mi1]                                              | 🟡 8 (61.54%)      | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llava-llama3:latest][ll6]                                         | 🟠 5 (38.46%)      | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llava:latest][ll7]                                                | 🟠 5 (38.46%)      | 🟢 1 (100.00%)      | 🟡 4 (80.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][gp1]                            | 🟡 8 (61.54%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [minicpm-v:latest][mi2]                                            | 🟠 4 (30.77%)      | 🟢 1 (100.00%)      | 🟡 3 (60.00%)        | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/gpt-oss-120b-GGUF][gp1]                                   | 🟡 8 (61.54%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [llama2:latest][ll5]                                               | 🟠 6 (46.15%)      | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [bakllava:latest][ba1]                                             | 🟠 3 (23.08%)      | 🟢 1 (100.00%)      | 🟡 4 (80.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][gp2]                             | 🟡 7 (53.85%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [deepseek-r1:14b][de1]                                             | 🟠 6 (46.15%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [gpt-oss:latest][gp3]                                              | 🟠 3 (23.08%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🟠 1 (20.00%)          | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][ge3]                          | 🟠 2 (15.38%)      | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [deepseek-r1:latest][de1]                                          | 🔴 0 (0.00%)       | 🟢 1 (100.00%)      | 🟠 1 (20.00%)        | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [NexaAI/Qwen3-4B-4bit-MLX][Qw8]                                    | 🔴 0 (0.00%)       | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qw4]                         | 🔴 0 (0.00%)       | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qw5]                         | 🔴 0 (0.00%)       | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |
| [NexaAI/gpt-oss-20b-MLX-4bit][gp4]                                 | 🔴 0 (0.00%)       | 🟢 1 (100.00%)      | 🔴 0 (0.00%)         | 🔴 0 (0.00%)           | 🔴 0 (0.00%)   | 🔴 0 (0.00%)        |

## Results by testsuites

| Model                   | PASS         | ALMOST      | FAIL         | ERROR       | TIMEOUT     |   Total |
|:------------------------|:-------------|:------------|:-------------|:------------|:------------|--------:|
| 🟡 [smoketest][sm1]     | 325 (58.14%) | 0           | 160 (28.62%) | 6 (1.07%)   | 68 (12.16%) |     559 |
| 🟢 [test_utils][te1]    | 43 (100.00%) | 0           | 0            | 0           | 0           |      43 |
| 🟠 [smokeimages][sm2]   | 39 (18.14%)  | 0           | 94 (43.72%)  | 70 (32.56%) | 12 (5.58%)  |     215 |
| 🟠 [basic_answers][ba2] | 32 (14.88%)  | 66 (30.70%) | 93 (43.26%)  | 0           | 24 (11.16%) |     215 |
| 🟠 [hello][he1]         | 24 (15.89%)  | 0           | 108 (71.52%) | 0           | 19 (12.58%) |     151 |
| 🟠 [patch_file][pa1]    | 18 (3.49%)   | 0           | 406 (78.68%) | 1 (0.19%)   | 91 (17.64%) |     516 |

## Results by tests

| Model                           | PASS         | ALMOST      | FAIL        | ERROR       | TIMEOUT     |   Total |
|:--------------------------------|:-------------|:------------|:------------|:------------|:------------|--------:|
| 🟢 [test_utils][te1] 00         | 43 (100.00%) | 0           | 0           | 0           | 0           |      43 |
| 🟡 [smoketest][sm1] 03          | 34 (79.07%)  | 0           | 6 (13.95%)  | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 05          | 33 (76.74%)  | 0           | 7 (16.28%)  | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 04          | 33 (76.74%)  | 0           | 7 (16.28%)  | 0           | 3 (6.98%)   |      43 |
| 🟡 [smoketest][sm1] 32          | 32 (74.42%)  | 0           | 6 (13.95%)  | 0           | 5 (11.63%)  |      43 |
| 🟡 [smoketest][sm1] 06          | 32 (74.42%)  | 0           | 5 (11.63%)  | 0           | 6 (13.95%)  |      43 |
| 🟡 [smoketest][sm1] 33          | 28 (65.12%)  | 0           | 10 (23.26%) | 1 (2.33%)   | 4 (9.30%)   |      43 |
| 🟡 [smoketest][sm1] 01          | 25 (58.14%)  | 0           | 6 (13.95%)  | 1 (2.33%)   | 11 (25.58%) |      43 |
| 🟡 [smoketest][sm1] 02          | 22 (51.16%)  | 0           | 6 (13.95%)  | 3 (6.98%)   | 12 (27.91%) |      43 |
| 🟠 [smoketest][sm1] 11          | 21 (48.84%)  | 0           | 20 (46.51%) | 0           | 2 (4.65%)   |      43 |
| 🟠 [smoketest][sm1] 13          | 18 (41.86%)  | 0           | 21 (48.84%) | 0           | 4 (9.30%)   |      43 |
| 🟠 [smoketest][sm1] 12          | 17 (39.53%)  | 0           | 22 (51.16%) | 0           | 4 (9.30%)   |      43 |
| 🟠 [smoketest][sm1] 10          | 16 (37.21%)  | 0           | 24 (55.81%) | 0           | 3 (6.98%)   |      43 |
| 🟠 [basic_answers][ba2] 0.paris | 15 (34.88%)  | 21 (48.84%) | 6 (13.95%)  | 0           | 1 (2.33%)   |      43 |
| 🟠 [basic_answers][ba2] 4.fact  | 14 (32.56%)  | 9 (20.93%)  | 17 (39.53%) | 0           | 3 (6.98%)   |      43 |
| 🟠 [smoketest][sm1] 31          | 14 (32.56%)  | 0           | 20 (46.51%) | 1 (2.33%)   | 8 (18.60%)  |      43 |
| 🟠 [smokeimages][sm2] 4         | 13 (30.23%)  | 0           | 10 (23.26%) | 17 (39.53%) | 3 (6.98%)   |      43 |
| 🟠 [smokeimages][sm2] 2         | 9 (20.93%)   | 0           | 15 (34.88%) | 17 (39.53%) | 2 (4.65%)   |      43 |
| 🟠 [smokeimages][sm2] 0         | 9 (20.93%)   | 0           | 15 (34.88%) | 17 (39.53%) | 2 (4.65%)   |      43 |
| 🟠 [hello][he1] 02name          | 7 (16.28%)   | 0           | 31 (72.09%) | 0           | 5 (11.63%)  |      43 |
| 🟠 [hello][he1] 03git           | 7 (21.21%)   | 0           | 20 (60.61%) | 0           | 6 (18.18%)  |      33 |
| 🟠 [smokeimages][sm2] 1         | 7 (16.28%)   | 0           | 17 (39.53%) | 18 (41.86%) | 1 (2.33%)   |      43 |
| 🟠 [hello][he1] 01world         | 6 (13.95%)   | 0           | 34 (79.07%) | 0           | 3 (6.98%)   |      43 |
| 🟠 [patch_file][pa1] 05python   | 5 (11.63%)   | 0           | 33 (76.74%) | 0           | 5 (11.63%)  |      43 |
| 🟠 [patch_file][pa1] 04ed       | 4 (9.30%)    | 0           | 32 (74.42%) | 0           | 7 (16.28%)  |      43 |
| 🟠 [hello][he1] 04gitignore     | 4 (12.50%)   | 0           | 23 (71.88%) | 0           | 5 (15.62%)  |      32 |
| 🟠 [patch_file][pa1] 03patch    | 3 (6.98%)    | 0           | 33 (76.74%) | 0           | 7 (16.28%)  |      43 |
| 🟠 [patch_file][pa1] 01cat      | 2 (4.65%)    | 0           | 34 (79.07%) | 0           | 7 (16.28%)  |      43 |
| 🟠 [patch_file][pa1] 00free     | 2 (4.65%)    | 0           | 35 (81.40%) | 0           | 6 (13.95%)  |      43 |
| 🟠 [basic_answers][ba2] 3.llme  | 1 (2.33%)    | 13 (30.23%) | 24 (55.81%) | 0           | 5 (11.63%)  |      43 |
| 🟠 [basic_answers][ba2] 2.llme  | 1 (2.33%)    | 12 (27.91%) | 23 (53.49%) | 0           | 7 (16.28%)  |      43 |
| 🟠 [basic_answers][ba2] 1.llme  | 1 (2.33%)    | 11 (25.58%) | 23 (53.49%) | 0           | 8 (18.60%)  |      43 |
| 🟠 [patch_file][pa1] 11cat      | 1 (2.33%)    | 0           | 36 (83.72%) | 0           | 6 (13.95%)  |      43 |
| 🟠 [patch_file][pa1] 02sed      | 1 (2.33%)    | 0           | 33 (76.74%) | 0           | 9 (20.93%)  |      43 |
| 🟠 [smokeimages][sm2] 3         | 1 (2.33%)    | 0           | 37 (86.05%) | 1 (2.33%)   | 4 (9.30%)   |      43 |
| 🔴 [patch_file][pa1] 14ed       | 0            | 0           | 33 (76.74%) | 0           | 10 (23.26%) |      43 |
| 🔴 [patch_file][pa1] 13patch    | 0            | 0           | 35 (81.40%) | 0           | 8 (18.60%)  |      43 |
| 🔴 [patch_file][pa1] 12sed      | 0            | 0           | 36 (83.72%) | 0           | 7 (16.28%)  |      43 |
| 🔴 [patch_file][pa1] 10free     | 0            | 0           | 35 (81.40%) | 0           | 8 (18.60%)  |      43 |
| 🔴 [patch_file][pa1] 15python   | 0            | 0           | 31 (72.09%) | 1 (2.33%)   | 11 (25.58%) |      43 |


  [qw1]: https://ollama.com/library/qwen3-coder
  [Mi1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [Qw1]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [Ma1]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [ll1]: https://ollama.com/library/llama3.2-vision
  [qw2]: https://ollama.com/library/qwen3
  [ma1]: https://ollama.com/library/magistral
  [Qw2]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [qw3]: https://ollama.com/library/qwen2.5vl
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
  [Qw6]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [Qw7]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [ll5]: https://ollama.com/library/llama2
  [LF1]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [gr3]: https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF
  [gr4]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [mi1]: https://ollama.com/library/mistral
  [ll6]: https://ollama.com/library/llava-llama3
  [ll7]: https://ollama.com/library/llava
  [gp1]: https://huggingface.co/unsloth/gpt-oss-120b-GGUF
  [mi2]: https://ollama.com/library/minicpm-v
  [ba1]: https://ollama.com/library/bakllava
  [gp2]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [de1]: https://ollama.com/library/deepseek-r1
  [gp3]: https://ollama.com/library/gpt-oss
  [ge3]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [Qw8]: https://huggingface.co/NexaAI/Qwen3-4B-4bit-MLX
  [qw4]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [qw5]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [gp4]: https://huggingface.co/NexaAI/gpt-oss-20b-MLX-4bit
  [sm1]: tests/smoketest.sh
  [te1]: tests/test_utils.sh
  [sm2]: tests/smokeimages.sh
  [ba2]: tests/basic_answers.sh
  [he1]: tests/hello.sh
  [pa1]: tests/patch_file.sh

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

* 68 models
* 124 model configurations
* 7 task suites
* 53 tasks
* 6512 results

## Results by models

| name                                                                                      | PASS        | ALMOST     | FAIL        | ERROR       | TIMEOUT     |   Total |
|:------------------------------------------------------------------------------------------|:------------|:-----------|:------------|:------------|:------------|--------:|
| 🟡 [unsloth/gpt-oss-120b-GGUF:Q4_K_M][go120] mode=native                                  | 37 (69.81%) | 0          | 10 (18.87%) | 4 (7.55%)   | 2 (3.77%)   |      53 |
| 🟡 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=1.0 mode=native                              | 35 (66.04%) | 1 (1.89%)  | 12 (22.64%) | 4 (7.55%)   | 1 (1.89%)   |      53 |
| 🟡 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=0.5 mode=native                              | 35 (66.04%) | 0          | 10 (18.87%) | 5 (9.43%)   | 3 (5.66%)   |      53 |
| 🟠 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] mode=native                                    | 34 (64.15%) | 2 (3.77%)  | 11 (20.75%) | 4 (7.55%)   | 2 (3.77%)   |      53 |
| 🟠 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=0.0 mode=native                              | 34 (64.15%) | 0          | 11 (20.75%) | 4 (7.55%)   | 4 (7.55%)   |      53 |
| 🟠 [qwen3-coder:30b][qc] t=0.0 mode=native                                                | 29 (54.72%) | 2 (3.77%)  | 20 (37.74%) | 0           | 2 (3.77%)   |      53 |
| 🟠 [qwen3-coder:30b][qc] t=0.5 mode=native                                                | 29 (54.72%) | 1 (1.89%)  | 21 (39.62%) | 0           | 2 (3.77%)   |      53 |
| 🟠 [qwen3-coder:30b][qc] mode=native                                                      | 29 (54.72%) | 1 (1.89%)  | 23 (43.40%) | 0           | 0           |      53 |
| 🟠 [qwen3-coder:30b][qc] t=1.5 mode=native                                                | 28 (52.83%) | 2 (3.77%)  | 22 (41.51%) | 0           | 1 (1.89%)   |      53 |
| 🟠 [gpt-oss:latest][go] mode=native                                                       | 28 (52.83%) | 1 (1.89%)  | 20 (37.74%) | 0           | 4 (7.55%)   |      53 |
| 🟠 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][qt4] mode=native                          | 26 (49.06%) | 0          | 18 (33.96%) | 4 (7.55%)   | 5 (9.43%)   |      53 |
| 🟠 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][qa30] mode=native                                  | 25 (47.17%) | 2 (3.77%)  | 18 (33.96%) | 6 (11.32%)  | 2 (3.77%)   |      53 |
| 🟠 [qwen3-coder:30b][qc] t=1.0 mode=native                                                | 25 (47.17%) | 0          | 28 (52.83%) | 0           | 0           |      53 |
| 🟠 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gh4] mode=native                             | 24 (45.28%) | 1 (1.89%)  | 21 (39.62%) | 4 (7.55%)   | 3 (5.66%)   |      53 |
| 🟠 [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][qt4] mode=markdown                        | 24 (45.28%) | 0          | 23 (43.40%) | 4 (7.55%)   | 2 (3.77%)   |      53 |
| 🟠 [qwen3:32b][q] mode=native                                                             | 23 (43.40%) | 3 (5.66%)  | 8 (15.09%)  | 0           | 19 (35.85%) |      53 |
| 🟠 [qwen3-coder:30b][qc] t=2.0 mode=native                                                | 23 (43.40%) | 1 (1.89%)  | 29 (54.72%) | 0           | 0           |      53 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] mode=native                   | 22 (41.51%) | 4 (7.55%)  | 15 (28.30%) | 5 (9.43%)   | 7 (13.21%)  |      53 |
| 🟠 [qwen3:latest][q] mode=native                                                          | 22 (41.51%) | 2 (3.77%)  | 26 (49.06%) | 0           | 3 (5.66%)   |      53 |
| 🟠 [gpt-oss:120b][go] mode=native                                                         | 22 (41.51%) | 1 (1.89%)  | 21 (39.62%) | 0           | 9 (16.98%)  |      53 |
| 🟠 [qwen3-vl:32b][qv] mode=native                                                         | 22 (41.51%) | 1 (1.89%)  | 8 (15.09%)  | 1 (1.89%)   | 21 (39.62%) |      53 |
| 🟠 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qi8] mode=markdown                               | 16 (41.03%) | 0          | 23 (58.97%) | 0           | 0           |      39 |
| 🟠 [qwen3:14b][q] mode=native                                                             | 21 (39.62%) | 2 (3.77%)  | 24 (45.28%) | 0           | 6 (11.32%)  |      53 |
| 🟠 [qwen3:30b][q] mode=native                                                             | 21 (39.62%) | 0          | 22 (41.51%) | 0           | 10 (18.87%) |      53 |
| 🟠 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qt8] mode=markdown                               | 15 (38.46%) | 0          | 23 (58.97%) | 1 (2.56%)   | 0           |      39 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] mode=markdown                 | 20 (37.74%) | 3 (5.66%)  | 23 (43.40%) | 4 (7.55%)   | 3 (5.66%)   |      53 |
| 🟠 [qwen3-vl:8b][qv] mode=native                                                          | 20 (37.74%) | 2 (3.77%)  | 19 (35.85%) | 0           | 12 (22.64%) |      53 |
| 🟠 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][gi3] mode=native                              | 20 (37.74%) | 2 (3.77%)  | 20 (37.74%) | 1 (1.89%)   | 10 (18.87%) |      53 |
| 🟠 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][qi4] mode=native                          | 20 (37.74%) | 2 (3.77%)  | 26 (49.06%) | 4 (7.55%)   | 1 (1.89%)   |      53 |
| 🟠 [qwen3:4b][q] mode=native                                                              | 20 (37.74%) | 1 (1.89%)  | 31 (58.49%) | 0           | 1 (1.89%)   |      53 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=1.0 mode=markdown           | 19 (35.85%) | 4 (7.55%)  | 18 (33.96%) | 0           | 12 (22.64%) |      53 |
| 🟠 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=0.0 mode=markdown           | 19 (35.85%) | 4 (7.55%)  | 15 (28.30%) | 0           | 15 (28.30%) |      53 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=0.0 mode=markdown | 19 (35.85%) | 4 (7.55%)  | 22 (41.51%) | 0           | 8 (15.09%)  |      53 |
| 🟠 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=0.5 mode=markdown | 19 (35.85%) | 4 (7.55%)  | 22 (41.51%) | 0           | 8 (15.09%)  |      53 |
| 🟠 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30] mode=native                   | 19 (35.85%) | 3 (5.66%)  | 24 (45.28%) | 6 (11.32%)  | 1 (1.89%)   |      53 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=1.5 mode=markdown | 18 (33.96%) | 4 (7.55%)  | 28 (52.83%) | 0           | 3 (5.66%)   |      53 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=2.0 mode=markdown           | 18 (33.96%) | 4 (7.55%)  | 23 (43.40%) | 1 (1.89%)   | 7 (13.21%)  |      53 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=0.5 mode=markdown           | 18 (33.96%) | 3 (5.66%)  | 19 (35.85%) | 4 (7.55%)   | 9 (16.98%)  |      53 |
| 🔴 [NexaAI/qwen3vl-4B-Instruct-4bit-mlx:4BIT][qi4b] mode=markdown                         | 18 (33.96%) | 3 (5.66%)  | 14 (26.42%) | 18 (33.96%) | 0           |      53 |
| 🔴 [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=1.5 mode=markdown           | 17 (32.08%) | 4 (7.55%)  | 23 (43.40%) | 0           | 9 (16.98%)  |      53 |
| 🔴 [qwen3-vl:30b][qv] mode=native                                                         | 17 (32.08%) | 2 (3.77%)  | 24 (45.28%) | 0           | 10 (18.87%) |      53 |
| 🔴 [qwen3:1.7b][q] mode=native                                                            | 17 (32.08%) | 2 (3.77%)  | 31 (58.49%) | 0           | 3 (5.66%)   |      53 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] mode=native         | 17 (32.08%) | 2 (3.77%)  | 16 (30.19%) | 1 (1.89%)   | 17 (32.08%) |      53 |
| 🔴 [qwen3:30b][q] mode=markdown                                                           | 17 (32.08%) | 1 (1.89%)  | 27 (50.94%) | 0           | 8 (15.09%)  |      53 |
| 🔴 [qwen3:14b][q] mode=markdown                                                           | 17 (32.08%) | 1 (1.89%)  | 30 (56.60%) | 0           | 5 (9.43%)   |      53 |
| 🔴 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][ms2509] mode=native                     | 16 (30.19%) | 4 (7.55%)  | 28 (52.83%) | 1 (1.89%)   | 4 (7.55%)   |      53 |
| 🔴 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gh4b] mode=native                        | 16 (30.19%) | 3 (5.66%)  | 30 (56.60%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [qwen3:32b][q] mode=markdown                                                           | 16 (30.19%) | 1 (1.89%)  | 23 (43.40%) | 0           | 13 (24.53%) |      53 |
| 🔴 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx:4BIT][qi8] mode=markdown                          | 16 (30.19%) | 1 (1.89%)  | 9 (16.98%)  | 24 (45.28%) | 3 (5.66%)   |      53 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=1.0 mode=markdown | 15 (28.30%) | 3 (5.66%)  | 23 (43.40%) | 0           | 12 (22.64%) |      53 |
| 🔴 [granite4:3b][g] mode=native                                                           | 15 (28.30%) | 3 (5.66%)  | 31 (58.49%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [qwen3-vl:4b][qv] mode=native                                                          | 15 (28.30%) | 2 (3.77%)  | 21 (39.62%) | 0           | 15 (28.30%) |      53 |
| 🔴 [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30] mode=markdown                 | 15 (28.30%) | 1 (1.89%)  | 33 (62.26%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][qi4] mode=markdown                        | 14 (26.42%) | 2 (3.77%)  | 33 (62.26%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [qwen3:latest][q] mode=markdown                                                        | 14 (26.42%) | 1 (1.89%)  | 36 (67.92%) | 0           | 2 (3.77%)   |      53 |
| 🔴 [NexaAI/gpt-oss-20b-MLX-4bit][go20b] mode=markdown                                     | 10 (25.64%) | 4 (10.26%) | 23 (58.97%) | 0           | 2 (5.13%)   |      39 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=2.0 mode=markdown | 13 (24.53%) | 3 (5.66%)  | 31 (58.49%) | 0           | 6 (11.32%)  |      53 |
| 🔴 [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][qa30] mode=markdown                                | 13 (24.53%) | 2 (3.77%)  | 24 (45.28%) | 4 (7.55%)   | 10 (18.87%) |      53 |
| 🔴 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=1.5 mode=native                              | 13 (24.53%) | 2 (3.77%)  | 33 (62.26%) | 5 (9.43%)   | 0           |      53 |
| 🔴 [qwen3:4b][q] mode=markdown                                                            | 13 (24.53%) | 1 (1.89%)  | 38 (71.70%) | 0           | 1 (1.89%)   |      53 |
| 🔴 [qwen3-coder:30b][qc] mode=markdown                                                    | 13 (24.53%) | 0          | 40 (75.47%) | 0           | 0           |      53 |
| 🔴 [qwen2.5vl:latest][q5] mode=markdown                                                   | 13 (24.53%) | 0          | 40 (75.47%) | 0           | 0           |      53 |
| 🔴 [gpt-oss:latest][go] mode=markdown                                                     | 13 (24.53%) | 0          | 39 (73.58%) | 1 (1.89%)   | 0           |      53 |
| 🔴 [llama3.2:latest][l2] mode=native                                                      | 12 (22.64%) | 2 (3.77%)  | 39 (73.58%) | 0           | 0           |      53 |
| 🔴 [llama3:latest][l] mode=markdown                                                       | 12 (22.64%) | 0          | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [minicpm-v:latest][mv] mode=markdown                                                   | 12 (22.64%) | 0          | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [deepseek-r1:14b][dr] mode=markdown                                                    | 12 (22.64%) | 0          | 40 (75.47%) | 0           | 1 (1.89%)   |      53 |
| 🔴 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx:4BIT][qt8] mode=native                            | 11 (20.75%) | 3 (5.66%)  | 38 (71.70%) | 1 (1.89%)   | 0           |      53 |
| 🔴 [llama3.2:latest][l2] mode=markdown                                                    | 11 (20.75%) | 1 (1.89%)  | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][ms2509] mode=markdown                   | 11 (20.75%) | 1 (1.89%)  | 40 (75.47%) | 0           | 1 (1.89%)   |      53 |
| 🔴 [llama3.2-vision:latest][lv2] mode=markdown                                            | 11 (20.75%) | 1 (1.89%)  | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gh4] mode=markdown                           | 11 (20.75%) | 1 (1.89%)  | 36 (67.92%) | 4 (7.55%)   | 1 (1.89%)   |      53 |
| 🔴 [NexaAI/qwen3vl-8B-Instruct-4bit-mlx:4BIT][qi8] mode=native                            | 11 (20.75%) | 0          | 42 (79.25%) | 0           | 0           |      53 |
| 🔴 [NexaAI/Qwen3-4B-4bit-MLX][qm4] mode=markdown                                          | 8 (20.51%)  | 4 (10.26%) | 26 (66.67%) | 0           | 1 (2.56%)   |      39 |
| 🔴 [qwen3:0.6b][q] mode=native                                                            | 10 (18.87%) | 4 (7.55%)  | 39 (73.58%) | 0           | 0           |      53 |
| 🔴 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gh4c] mode=markdown                           | 10 (18.87%) | 4 (7.55%)  | 17 (32.08%) | 4 (7.55%)   | 18 (33.96%) |      53 |
| 🔴 [gemma3:27b][gb] mode=markdown                                                         | 10 (18.87%) | 3 (5.66%)  | 40 (75.47%) | 0           | 0           |      53 |
| 🔴 [NexaAI/qwen3vl-4B-Thinking-4bit-mlx:4BIT][qt4b] mode=native                           | 10 (18.87%) | 3 (5.66%)  | 38 (71.70%) | 2 (3.77%)   | 0           |      53 |
| 🔴 [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gh4c] mode=native                             | 10 (18.87%) | 3 (5.66%)  | 30 (56.60%) | 4 (7.55%)   | 6 (11.32%)  |      53 |
| 🔴 [llama3.1:70b][l1] mode=markdown                                                       | 10 (18.87%) | 2 (3.77%)  | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [magistral:latest][m] mode=markdown                                                    | 10 (18.87%) | 2 (3.77%)  | 39 (73.58%) | 0           | 2 (3.77%)   |      53 |
| 🔴 [llava-llama3:latest][ll] mode=markdown                                                | 10 (18.87%) | 1 (1.89%)  | 42 (79.25%) | 0           | 0           |      53 |
| 🔴 [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gh4b] mode=markdown                      | 10 (18.87%) | 1 (1.89%)  | 38 (71.70%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [llava:latest][lb] mode=markdown                                                       | 10 (18.87%) | 0          | 43 (81.13%) | 0           | 0           |      53 |
| 🔴 [granite3-dense:latest][gd] mode=native                                                | 10 (18.87%) | 0          | 43 (81.13%) | 0           | 0           |      53 |
| 🔴 [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] mode=markdown       | 9 (16.98%)  | 4 (7.55%)  | 39 (73.58%) | 0           | 1 (1.89%)   |      53 |
| 🔴 [NexaAI/qwen3vl-4B-Thinking-4bit-mlx:4BIT][qt4b] mode=markdown                         | 9 (16.98%)  | 4 (7.55%)  | 28 (52.83%) | 12 (22.64%) | 0           |      53 |
| 🔴 [mistral-small3.2:24b][ms2] mode=native                                                | 9 (16.98%)  | 3 (5.66%)  | 27 (50.94%) | 0           | 14 (26.42%) |      53 |
| 🔴 [magistral:latest][m] mode=native                                                      | 9 (16.98%)  | 3 (5.66%)  | 41 (77.36%) | 0           | 0           |      53 |
| 🔴 [llava-phi3:latest][lp] mode=markdown                                                  | 9 (16.98%)  | 1 (1.89%)  | 43 (81.13%) | 0           | 0           |      53 |
| 🔴 [granite4:350m][g] mode=native                                                         | 9 (16.98%)  | 0          | 41 (77.36%) | 3 (5.66%)   | 0           |      53 |
| 🔴 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][la8] mode=native                                    | 9 (16.98%)  | 0          | 32 (60.38%) | 4 (7.55%)   | 8 (15.09%)  |      53 |
| 🔴 [unsloth/gpt-oss-120b-GGUF:Q4_K_M][go120] mode=markdown                                | 9 (16.98%)  | 0          | 40 (75.47%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] mode=markdown                                  | 9 (16.98%)  | 0          | 40 (75.47%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [NexaAI/Qwen3-4B-4bit-MLX:4BIT][qm4] mode=native                                       | 8 (15.09%)  | 4 (7.55%)  | 37 (69.81%) | 4 (7.55%)   | 0           |      53 |
| 🔴 [NexaAI/qwen3vl-8B-Thinking-4bit-mlx:4BIT][qt8] mode=markdown                          | 8 (15.09%)  | 4 (7.55%)  | 33 (62.26%) | 8 (15.09%)  | 0           |      53 |
| 🔴 [llama2:7b][lc] mode=markdown                                                          | 8 (15.09%)  | 1 (1.89%)  | 44 (83.02%) | 0           | 0           |      53 |
| 🔴 [qwen3:1.7b][q] mode=markdown                                                          | 8 (15.09%)  | 1 (1.89%)  | 43 (81.13%) | 0           | 1 (1.89%)   |      53 |
| 🔴 [granite3-dense:latest][gd] mode=markdown                                              | 8 (15.09%)  | 1 (1.89%)  | 44 (83.02%) | 0           | 0           |      53 |
| 🔴 [mistral:latest][mb] mode=markdown                                                     | 8 (15.09%)  | 1 (1.89%)  | 44 (83.02%) | 0           | 0           |      53 |
| 🔴 [qwen3:0.6b][q] mode=markdown                                                          | 8 (15.09%)  | 1 (1.89%)  | 44 (83.02%) | 0           | 0           |      53 |
| 🔴 [llama2:latest][lc] mode=markdown                                                      | 8 (15.09%)  | 1 (1.89%)  | 44 (83.02%) | 0           | 0           |      53 |
| 🔴 [NexaAI/qwen3vl-4B-Instruct-4bit-mlx:4BIT][qi4b] mode=native                           | 8 (15.09%)  | 1 (1.89%)  | 43 (81.13%) | 1 (1.89%)   | 0           |      53 |
| 🔴 [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30b] mode=markdown     | 8 (15.09%)  | 1 (1.89%)  | 34 (64.15%) | 4 (7.55%)   | 6 (11.32%)  |      53 |
| 🔴 [gemma3:latest][gb] mode=markdown                                                      | 8 (15.09%)  | 0          | 45 (84.91%) | 0           | 0           |      53 |
| 🔴 [gemma3:12b][gb] mode=markdown                                                         | 8 (15.09%)  | 0          | 45 (84.91%) | 0           | 0           |      53 |
| 🔴 [gpt-oss:120b][go] mode=markdown                                                       | 8 (15.09%)  | 0          | 32 (60.38%) | 12 (22.64%) | 1 (1.89%)   |      53 |
| 🔥 [llama3.1:70b][l1] mode=native                                                         | 7 (14.29%)  | 0          | 39 (79.59%) | 0           | 3 (6.12%)   |      49 |
| 🔥 [granite4:1b][g] mode=native                                                           | 7 (13.21%)  | 3 (5.66%)  | 34 (64.15%) | 9 (16.98%)  | 0           |      53 |
| 🔥 [qwen3-vl:2b][qv] mode=native                                                          | 7 (13.21%)  | 1 (1.89%)  | 26 (49.06%) | 0           | 19 (35.85%) |      53 |
| 🔥 [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][qc5] mode=markdown                          | 7 (13.21%)  | 0          | 18 (33.96%) | 4 (7.55%)   | 24 (45.28%) |      53 |
| 🔥 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][gi3b] mode=markdown                               | 7 (13.21%)  | 0          | 42 (79.25%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [NexaAI/gpt-oss-20b-MLX-4bit:4BIT][go20b] mode=markdown                                | 6 (11.32%)  | 2 (3.77%)  | 41 (77.36%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [NexaAI/gpt-oss-20b-MLX-4bit:4BIT][go20b] mode=native                                  | 6 (11.32%)  | 2 (3.77%)  | 41 (77.36%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [bakllava:latest][b] mode=markdown                                                     | 6 (11.32%)  | 1 (1.89%)  | 46 (86.79%) | 0           | 0           |      53 |
| 🔥 [gemma3:1b][gb] mode=markdown                                                          | 6 (11.32%)  | 1 (1.89%)  | 42 (79.25%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][la8] mode=markdown                                  | 6 (11.32%)  | 0          | 42 (79.25%) | 4 (7.55%)   | 1 (1.89%)   |      53 |
| 🔥 [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][gi3] mode=markdown                            | 6 (11.32%)  | 0          | 43 (81.13%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [NexaAI/Qwen3-4B-4bit-MLX:4BIT][qm4] mode=markdown                                     | 5 (9.43%)   | 4 (7.55%)  | 14 (26.42%) | 30 (56.60%) | 0           |      53 |
| 🔥 [mistral:latest][mb] mode=native                                                       | 5 (9.43%)   | 2 (3.77%)  | 46 (86.79%) | 0           | 0           |      53 |
| 🔥 [gemma3:270m][gb] mode=markdown                                                        | 5 (9.43%)   | 1 (1.89%)  | 43 (81.13%) | 4 (7.55%)   | 0           |      53 |
| 🔥 [deepseek-r1:latest][dr] mode=markdown                                                 | 4 (7.55%)   | 0          | 15 (28.30%) | 0           | 34 (64.15%) |      53 |
| 🔥 [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=2.0 mode=native                              | 2 (3.77%)   | 3 (5.66%)  | 41 (77.36%) | 5 (9.43%)   | 2 (3.77%)   |      53 |
| 💀 [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][gi3b] mode=native                                 | 0           | 0          | 12 (22.64%) | 36 (67.92%) | 5 (9.43%)   |      53 |

## Task suites by models

| Models                                                                                 | [smoketest][ss]    | [hello][hs]      | [basic_answers][bs]   | [smokeimages][ssb]   | [debug_fib][ds]   | [crapto][cs]    | [patch_file][ps]   |
|:---------------------------------------------------------------------------------------|:-------------------|:-----------------|:----------------------|:---------------------|:------------------|:----------------|:-------------------|
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][go120] mode=native                                  | 💎 13/13 (100.00%) | 💎 4/4 (100.00%) | 🟡 4/5 (80.00%)       | 💀 0/5               | 💎 6/6 (100.00%)  | 🟠 3/8 (37.50%) | 🟠 7/12 (58.33%)   |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=1.0 mode=native                              | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🟡 4/5 (80.00%)       | 🔴 1/5 (20.00%)      | 🟡 4/6 (66.67%)   | 🟠 4/8 (50.00%) | 🟠 6/12 (50.00%)   |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=0.5 mode=native                              | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🟡 4/5 (80.00%)       | 💀 0/5               | 🟡 5/6 (83.33%)   | 🟠 4/8 (50.00%) | 🟠 6/12 (50.00%)   |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] mode=native                                    | 💎 13/13 (100.00%) | 💎 4/4 (100.00%) | 🟠 2/5 (40.00%)       | 💀 0/5               | 🟡 4/6 (66.67%)   | 🟠 3/8 (37.50%) | 🟡 8/12 (66.67%)   |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=0.0 mode=native                              | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 🟡 4/5 (80.00%)       | 💀 0/5               | 💎 6/6 (100.00%)  | 🟠 4/8 (50.00%) | 🟠 6/12 (50.00%)   |
| [qwen3-coder:30b][qc] t=0.0 mode=native                                                | 💎 13/13 (100.00%) | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 🟠 4/8 (50.00%) | 🟠 6/12 (50.00%)   |
| [qwen3-coder:30b][qc] t=0.5 mode=native                                                | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 🟡 4/5 (80.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🟠 3/8 (37.50%) | 🟠 6/12 (50.00%)   |
| [qwen3-coder:30b][qc] mode=native                                                      | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🟠 4/8 (50.00%) | 🟠 7/12 (58.33%)   |
| [qwen3-coder:30b][qc] t=1.5 mode=native                                                | 🟡 10/13 (76.92%)  | 💎 4/4 (100.00%) | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 🟠 3/6 (50.00%)   | 🟠 3/8 (37.50%) | 🟠 5/12 (41.67%)   |
| [gpt-oss:latest][go] mode=native                                                       | 💎 13/13 (100.00%) | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 🟠 2/5 (40.00%)      | 🟠 3/6 (50.00%)   | 🟠 4/8 (50.00%) | 💀 0/12            |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][qt4] mode=native                          | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💎 5/5 (100.00%)      | 💀 0/5               | 🟠 3/6 (50.00%)   | 🟠 3/8 (37.50%) | 🔴 2/12 (16.67%)   |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][qa30] mode=native                                  | 🟡 11/13 (84.62%)  | 💎 4/4 (100.00%) | 🟠 3/5 (60.00%)       | 💀 0/5               | 🔴 2/6 (33.33%)   | 🟠 3/8 (37.50%) | 🔴 2/12 (16.67%)   |
| [qwen3-coder:30b][qc] t=1.0 mode=native                                                | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🟠 3/8 (37.50%) | 🔴 4/12 (33.33%)   |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gh4] mode=native                             | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🟡 4/5 (80.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🔥 1/8 (12.50%) | 🔴 2/12 (16.67%)   |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][qt4] mode=markdown                        | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 💎 5/5 (100.00%)      | 💀 0/5               | 💀 0/6            | 🔥 1/8 (12.50%) | 🔴 3/12 (25.00%)   |
| [qwen3:32b][q] mode=native                                                             | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🔴 2/8 (25.00%) | 🔴 3/12 (25.00%)   |
| [qwen3-coder:30b][qc] t=2.0 mode=native                                                | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 🔴 1/6 (16.67%)   | 🟠 3/8 (37.50%) | 🔴 3/12 (25.00%)   |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] mode=native                   | 💎 13/13 (100.00%) | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 🟠 3/6 (50.00%)   | 🟠 4/8 (50.00%) | 💀 0/12            |
| [qwen3:latest][q] mode=native                                                          | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🟠 3/5 (60.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [gpt-oss:120b][go] mode=native                                                         | 🟢 12/13 (92.31%)  | 🟠 2/4 (50.00%)  | 🟠 3/5 (60.00%)       | 🟠 3/5 (60.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [qwen3-vl:32b][qv] mode=native                                                         | 🟠 7/13 (53.85%)   | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 🟡 4/5 (80.00%)      | 💀 0/6            | 🔴 2/8 (25.00%) | 🔴 4/12 (33.33%)   |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][qi8] mode=markdown                               | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               |                   |                 | 💀 0/12            |
| [qwen3:14b][q] mode=native                                                             | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🔥 1/8 (12.50%) | 🔴 3/12 (25.00%)   |
| [qwen3:30b][q] mode=native                                                             | 🟡 10/13 (76.92%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 🔴 1/6 (16.67%)   | 🔴 2/8 (25.00%) | 🔴 2/12 (16.67%)   |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][qt8] mode=markdown                               | 🟢 12/13 (92.31%)  | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      |                   |                 | 💀 0/12            |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] mode=markdown                 | 🟢 12/13 (92.31%)  | 🟠 2/4 (50.00%)  | 🟠 2/5 (40.00%)       | 💀 0/5               | 💀 0/6            | 🔴 2/8 (25.00%) | 🔴 2/12 (16.67%)   |
| [qwen3-vl:8b][qv] mode=native                                                          | 🟠 6/13 (46.15%)   | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 🟠 2/5 (40.00%)      | 🔴 1/6 (16.67%)   | 🔥 1/8 (12.50%) | 🔴 4/12 (33.33%)   |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][gi3] mode=native                              | 🟢 12/13 (92.31%)  | 💎 4/4 (100.00%) | 🟠 3/5 (60.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][qi4] mode=native                          | 💎 13/13 (100.00%) | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 🔥 1/8 (12.50%) | 💀 0/12            |
| [qwen3:4b][q] mode=native                                                              | 💎 13/13 (100.00%) | 🟠 2/4 (50.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=1.0 mode=markdown           | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5                | 💀 0/5               | 🟠 3/6 (50.00%)   | 🟠 3/8 (37.50%) | 💀 0/12            |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=0.0 mode=markdown           | 🟠 8/13 (61.54%)   | 🟡 3/4 (75.00%)  | 💀 0/5                | 💀 0/5               | 🟡 5/6 (83.33%)   | 🟠 3/8 (37.50%) | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=0.0 mode=markdown | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 💀 0/5                | 🟡 4/5 (80.00%)      | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=0.5 mode=markdown | 🟡 11/13 (84.62%)  | 🟡 3/4 (75.00%)  | 💀 0/5                | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 🔴 3/12 (25.00%)   |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30] mode=native                   | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 🔴 2/6 (33.33%)   | 🟠 3/8 (37.50%) | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=1.5 mode=markdown | 🟡 11/13 (84.62%)  | 💎 4/4 (100.00%) | 💀 0/5                | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=2.0 mode=markdown           | 🟡 11/13 (84.62%)  | 🟠 2/4 (50.00%)  | 💀 0/5                | 💀 0/5               | 🔴 2/6 (33.33%)   | 🟠 3/8 (37.50%) | 💀 0/12            |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=0.5 mode=markdown           | 🟢 12/13 (92.31%)  | 🔴 1/4 (25.00%)  | 💀 0/5                | 💀 0/5               | 🟡 4/6 (66.67%)   | 🔥 1/8 (12.50%) | 💀 0/12            |
| [NexaAI/qwen3vl-4B-Instruct-4bit-mlx:4BIT][qi4b] mode=markdown                         | 💎 13/13 (100.00%) | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 🔴 2/8 (25.00%) | 💀 0/12            |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][qa30b] t=1.5 mode=markdown           | 🟡 10/13 (76.92%)  | 🟠 2/4 (50.00%)  | 💀 0/5                | 💀 0/5               | 🔴 2/6 (33.33%)   | 🟠 3/8 (37.50%) | 💀 0/12            |
| [qwen3-vl:30b][qv] mode=native                                                         | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 🟠 3/5 (60.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 🔴 3/12 (25.00%)   |
| [qwen3:1.7b][q] mode=native                                                            | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] mode=native         | 🟡 10/13 (76.92%)  | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 🟠 3/6 (50.00%)   | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [qwen3:30b][q] mode=markdown                                                           | 🟠 8/13 (61.54%)   | 🟠 2/4 (50.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔴 3/12 (25.00%)   |
| [qwen3:14b][q] mode=markdown                                                           | 🟡 11/13 (84.62%)  | 💀 0/4           | 🟠 3/5 (60.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 💀 0/8          | 🔴 2/12 (16.67%)   |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][ms2509] mode=native                     | 🟠 8/13 (61.54%)   | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)       | 🟠 2/5 (40.00%)      | 🔴 1/6 (16.67%)   | 🔴 2/8 (25.00%) | 💀 0/12            |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gh4b] mode=native                        | 🟢 12/13 (92.31%)  | 🟡 3/4 (75.00%)  | 💀 0/5                | 💀 0/5               | 🔴 1/6 (16.67%)   | 💀 0/8          | 💀 0/12            |
| [qwen3:32b][q] mode=markdown                                                           | 🟡 10/13 (76.92%)  | 💀 0/4           | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 🔴 2/8 (25.00%) | 🔥 1/12 (8.33%)    |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx:4BIT][qi8] mode=markdown                          | 🟠 8/13 (61.54%)   | 🟡 3/4 (75.00%)  | 🟠 3/5 (60.00%)       | 🔴 1/5 (20.00%)      | 🔴 1/6 (16.67%)   | 💀 0/8          | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=1.0 mode=markdown | 🟡 9/13 (69.23%)   | 🟡 3/4 (75.00%)  | 💀 0/5                | 💀 0/5               | 🔴 1/6 (16.67%)   | 💀 0/8          | 🔴 2/12 (16.67%)   |
| [granite4:3b][g] mode=native                                                           | 🟡 10/13 (76.92%)  | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)       | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3-vl:4b][qv] mode=native                                                          | 🟠 7/13 (53.85%)   | 🟡 3/4 (75.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30] mode=markdown                 | 🟡 10/13 (76.92%)  | 🟠 2/4 (50.00%)  | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][qi4] mode=markdown                        | 🟡 11/13 (84.62%)  | 💀 0/4           | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3:latest][q] mode=markdown                                                        | 🟡 10/13 (76.92%)  | 💀 0/4           | 🟠 3/5 (60.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [NexaAI/gpt-oss-20b-MLX-4bit][go20b] mode=markdown                                     | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5                | 💀 0/5               |                   |                 | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] t=2.0 mode=markdown | 🟠 5/13 (38.46%)   | 💎 4/4 (100.00%) | 💀 0/5                | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][qa30] mode=markdown                                | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)       | 💀 0/5               | 🔴 1/6 (16.67%)   | 💀 0/8          | 💀 0/12            |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=1.5 mode=native                              | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3:4b][q] mode=markdown                                                            | 🟠 7/13 (53.85%)   | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 🔥 1/8 (12.50%) | 🔥 1/12 (8.33%)    |
| [qwen3-coder:30b][qc] mode=markdown                                                    | 🟡 10/13 (76.92%)  | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen2.5vl:latest][q5] mode=markdown                                                   | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🟡 4/5 (80.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gpt-oss:latest][go] mode=markdown                                                     | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama3.2:latest][l2] mode=native                                                      | 🟡 9/13 (69.23%)   | 🔴 1/4 (25.00%)  | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama3:latest][l] mode=markdown                                                       | 🟠 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [minicpm-v:latest][mv] mode=markdown                                                   | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [deepseek-r1:14b][dr] mode=markdown                                                    | 🟠 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx:4BIT][qt8] mode=native                            | 🟠 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama3.2:latest][l2] mode=markdown                                                    | 🟡 9/13 (69.23%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][ms2509] mode=markdown                   | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [llama3.2-vision:latest][lv2] mode=markdown                                            | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][gh4] mode=markdown                           | 🟠 7/13 (53.85%)   | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx:4BIT][qi8] mode=native                            | 🟠 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/Qwen3-4B-4bit-MLX][qm4] mode=markdown                                          | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               |                   |                 | 💀 0/12            |
| [qwen3:0.6b][q] mode=native                                                            | 🟠 8/13 (61.54%)   | 🔴 1/4 (25.00%)  | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gh4c] mode=markdown                           | 🟡 10/13 (76.92%)  | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gemma3:27b][gb] mode=markdown                                                         | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/qwen3vl-4B-Thinking-4bit-mlx:4BIT][qt4b] mode=native                           | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][gh4c] mode=native                             | 🟡 9/13 (69.23%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama3.1:70b][l1] mode=markdown                                                       | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [magistral:latest][m] mode=markdown                                                    | 🟠 8/13 (61.54%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llava-llama3:latest][ll] mode=markdown                                                | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][gh4b] mode=markdown                      | 🟡 9/13 (69.23%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llava:latest][lb] mode=markdown                                                       | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5                | 🟡 4/5 (80.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [granite3-dense:latest][gd] mode=native                                                | 🟠 7/13 (53.85%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][ms3] mode=markdown       | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🟠 2/5 (40.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/qwen3vl-4B-Thinking-4bit-mlx:4BIT][qt4b] mode=markdown                         | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [mistral-small3.2:24b][ms2] mode=native                                                | 🟠 6/13 (46.15%)   | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [magistral:latest][m] mode=native                                                      | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llava-phi3:latest][lp] mode=markdown                                                  | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5                | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [granite4:350m][g] mode=native                                                         | 🟡 9/13 (69.23%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][la8] mode=native                                    | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][go120] mode=markdown                                | 🟠 7/13 (53.85%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] mode=markdown                                  | 🟠 8/13 (61.54%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/Qwen3-4B-4bit-MLX:4BIT][qm4] mode=native                                       | 🟠 8/13 (61.54%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx:4BIT][qt8] mode=markdown                          | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama2:7b][lc] mode=markdown                                                          | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3:1.7b][q] mode=markdown                                                          | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [granite3-dense:latest][gd] mode=markdown                                              | 🟠 6/13 (46.15%)   | 💀 0/4           | 🟠 2/5 (40.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [mistral:latest][mb] mode=markdown                                                     | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3:0.6b][q] mode=markdown                                                          | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama2:latest][lc] mode=markdown                                                      | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/qwen3vl-4B-Instruct-4bit-mlx:4BIT][qi4b] mode=native                           | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][qc30b] mode=markdown     | 🟠 5/13 (38.46%)   | 🔴 1/4 (25.00%)  | 💀 0/5                | 💀 0/5               | 💀 0/6            | 🔴 2/8 (25.00%) | 💀 0/12            |
| [gemma3:latest][gb] mode=markdown                                                      | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gemma3:12b][gb] mode=markdown                                                         | 🔴 4/13 (30.77%)   | 💀 0/4           | 💀 0/5                | 🟡 4/5 (80.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gpt-oss:120b][go] mode=markdown                                                       | 🟠 7/13 (53.85%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [llama3.1:70b][l1] mode=native                                                         | 🟠 5/13 (38.46%)   | 💀 0/4           | 💎 1/1 (100.00%)      | 💀 0/5               | 💀 0/6            | 💀 0/8          | 🔥 1/12 (8.33%)    |
| [granite4:1b][g] mode=native                                                           | 🔴 4/13 (30.77%)   | 🟠 2/4 (50.00%)  | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [qwen3-vl:2b][qv] mode=native                                                          | 🟠 5/13 (38.46%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][qc5] mode=markdown                          | 🟠 6/13 (46.15%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][gi3b] mode=markdown                               | 🟠 7/13 (53.85%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/gpt-oss-20b-MLX-4bit:4BIT][go20b] mode=markdown                                | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/gpt-oss-20b-MLX-4bit:4BIT][go20b] mode=native                                  | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [bakllava:latest][b] mode=markdown                                                     | 🔴 3/13 (23.08%)   | 💀 0/4           | 💀 0/5                | 🟠 3/5 (60.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gemma3:1b][gb] mode=markdown                                                          | 🟠 6/13 (46.15%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][la8] mode=markdown                                  | 🟠 5/13 (38.46%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][gi3] mode=markdown                            | 🟠 5/13 (38.46%)   | 💀 0/4           | 🔴 1/5 (20.00%)       | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [NexaAI/Qwen3-4B-4bit-MLX:4BIT][qm4] mode=markdown                                     | 🟠 5/13 (38.46%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [mistral:latest][mb] mode=native                                                       | 🟠 5/13 (38.46%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [gemma3:270m][gb] mode=markdown                                                        | 🟠 5/13 (38.46%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [deepseek-r1:latest][dr] mode=markdown                                                 | 🔴 4/13 (30.77%)   | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][go20] t=2.0 mode=native                              | 🔥 1/13 (7.69%)    | 💀 0/4           | 💀 0/5                | 🔴 1/5 (20.00%)      | 💀 0/6            | 💀 0/8          | 💀 0/12            |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][gi3b] mode=native                                 | 💀 0/13            | 💀 0/4           | 💀 0/5                | 💀 0/5               | 💀 0/6            | 💀 0/8          | 💀 0/12            |

## Results by task suites

| name                   | PASS          | ALMOST       | FAIL          | ERROR        | TIMEOUT      |   Total |
|:-----------------------|:--------------|:-------------|:--------------|:-------------|:-------------|--------:|
| 🟡 [smoketest][ss]     | 1063 (65.94%) | 0            | 438 (27.17%)  | 44 (2.73%)   | 67 (4.16%)   |    1612 |
| 🔴 [hello][hs]         | 153 (30.85%)  | 0            | 296 (59.68%)  | 12 (2.42%)   | 35 (7.06%)   |     496 |
| 🔴 [basic_answers][bs] | 176 (28.57%)  | 202 (32.79%) | 206 (33.44%)  | 6 (0.97%)    | 26 (4.22%)   |     616 |
| 🔴 [smokeimages][ssb]  | 98 (15.81%)   | 0            | 335 (54.03%)  | 163 (26.29%) | 24 (3.87%)   |     620 |
| 🔥 [debug_fib][ds]     | 75 (10.42%)   | 0            | 559 (77.64%)  | 29 (4.03%)   | 57 (7.92%)   |     720 |
| 🔥 [crapto][cs]        | 96 (10.00%)   | 0            | 723 (75.31%)  | 35 (3.65%)   | 106 (11.04%) |     960 |
| 🔥 [patch_file][ps]    | 119 (8.00%)   | 0            | 1183 (79.50%) | 34 (2.28%)   | 152 (10.22%) |    1488 |

## Results by tasks

| name                                    | PASS         | ALMOST      | FAIL         | ERROR       | TIMEOUT     |   Total |
|:----------------------------------------|:-------------|:------------|:-------------|:------------|:------------|--------:|
| 🟢 [smoketest][ss] 03                   | 112 (90.32%) | 0           | 5 (4.03%)    | 5 (4.03%)   | 2 (1.61%)   |     124 |
| 🟢 [smoketest][ss] 33                   | 108 (87.10%) | 0           | 11 (8.87%)   | 1 (0.81%)   | 4 (3.23%)   |     124 |
| 🟢 [smoketest][ss] 05                   | 108 (87.10%) | 0           | 7 (5.65%)    | 1 (0.81%)   | 8 (6.45%)   |     124 |
| 🟡 [smoketest][ss] 32                   | 103 (83.06%) | 0           | 16 (12.90%)  | 0           | 5 (4.03%)   |     124 |
| 🟡 [smoketest][ss] 04                   | 101 (81.45%) | 0           | 20 (16.13%)  | 3 (2.42%)   | 0           |     124 |
| 🟡 [smoketest][ss] 06                   | 101 (81.45%) | 0           | 14 (11.29%)  | 3 (2.42%)   | 6 (4.84%)   |     124 |
| 🟡 [smoketest][ss] 01                   | 96 (77.42%)  | 0           | 15 (12.10%)  | 3 (2.42%)   | 10 (8.06%)  |     124 |
| 🟠 [smoketest][ss] 02                   | 71 (57.26%)  | 0           | 29 (23.39%)  | 10 (8.06%)  | 14 (11.29%) |     124 |
| 🟠 [basic_answers][bs] 0.paris          | 65 (52.85%)  | 42 (34.15%) | 8 (6.50%)    | 1 (0.81%)   | 7 (5.69%)   |     123 |
| 🟠 [smoketest][ss] 12                   | 62 (50.00%)  | 0           | 56 (45.16%)  | 4 (3.23%)   | 2 (1.61%)   |     124 |
| 🟠 [basic_answers][bs] 4.fact           | 57 (45.97%)  | 11 (8.87%)  | 51 (41.13%)  | 1 (0.81%)   | 4 (3.23%)   |     124 |
| 🟠 [smoketest][ss] 13                   | 53 (42.74%)  | 0           | 66 (53.23%)  | 3 (2.42%)   | 2 (1.61%)   |     124 |
| 🟠 [smoketest][ss] 10                   | 52 (41.94%)  | 0           | 65 (52.42%)  | 3 (2.42%)   | 4 (3.23%)   |     124 |
| 🟠 [smoketest][ss] 11                   | 52 (41.94%)  | 0           | 67 (54.03%)  | 4 (3.23%)   | 1 (0.81%)   |     124 |
| 🟠 [hello][hs] 03git                    | 48 (38.71%)  | 0           | 67 (54.03%)  | 2 (1.61%)   | 7 (5.65%)   |     124 |
| 🟠 [smokeimages][ssb] 4                 | 46 (37.10%)  | 0           | 28 (22.58%)  | 41 (33.06%) | 9 (7.26%)   |     124 |
| 🟠 [smoketest][ss] 31                   | 44 (35.48%)  | 0           | 67 (54.03%)  | 4 (3.23%)   | 9 (7.26%)   |     124 |
| 🔴 [hello][hs] 02name                   | 38 (30.65%)  | 0           | 73 (58.87%)  | 2 (1.61%)   | 11 (8.87%)  |     124 |
| 🔴 [hello][hs] 01world                  | 38 (30.65%)  | 0           | 79 (63.71%)  | 4 (3.23%)   | 3 (2.42%)   |     124 |
| 🔴 [crapto][cs] 10-base64               | 34 (28.33%)  | 0           | 78 (65.00%)  | 5 (4.17%)   | 3 (2.50%)   |     120 |
| 🔴 [hello][hs] 04gitignore              | 29 (23.39%)  | 0           | 77 (62.10%)  | 4 (3.23%)   | 14 (11.29%) |     124 |
| 🔴 [crapto][cs] 40-xor                  | 26 (21.67%)  | 0           | 79 (65.83%)  | 3 (2.50%)   | 12 (10.00%) |     120 |
| 🔴 [patch_file][ps] 05python            | 24 (19.35%)  | 0           | 95 (76.61%)  | 2 (1.61%)   | 3 (2.42%)   |     124 |
| 🔴 [crapto][cs] 41-xor-nohint           | 23 (19.17%)  | 0           | 84 (70.00%)  | 4 (3.33%)   | 9 (7.50%)   |     120 |
| 🔴 [patch_file][ps] 04ed                | 23 (18.55%)  | 0           | 85 (68.55%)  | 2 (1.61%)   | 14 (11.29%) |     124 |
| 🔴 [basic_answers][bs] 1.llme           | 21 (17.07%)  | 45 (36.59%) | 50 (40.65%)  | 1 (0.81%)   | 6 (4.88%)   |     123 |
| 🔴 [debug_fib][ds] 01                   | 18 (15.00%)  | 0           | 92 (76.67%)  | 2 (1.67%)   | 8 (6.67%)   |     120 |
| 🔥 [patch_file][ps] 00free              | 18 (14.52%)  | 0           | 98 (79.03%)  | 2 (1.61%)   | 6 (4.84%)   |     124 |
| 🔥 [basic_answers][bs] 3.llme           | 17 (13.82%)  | 51 (41.46%) | 49 (39.84%)  | 2 (1.63%)   | 4 (3.25%)   |     123 |
| 🔥 [debug_fib][ds] 04                   | 16 (13.33%)  | 0           | 96 (80.00%)  | 4 (3.33%)   | 4 (3.33%)   |     120 |
| 🔥 [basic_answers][bs] 2.llme           | 16 (13.01%)  | 53 (43.09%) | 48 (39.02%)  | 1 (0.81%)   | 5 (4.07%)   |     123 |
| 🔥 [smokeimages][ssb] 0                 | 16 (12.90%)  | 0           | 66 (53.23%)  | 40 (32.26%) | 2 (1.61%)   |     124 |
| 🔥 [smokeimages][ssb] 2                 | 16 (12.90%)  | 0           | 67 (54.03%)  | 40 (32.26%) | 1 (0.81%)   |     124 |
| 🔥 [debug_fib][ds] 02b                  | 15 (12.50%)  | 0           | 90 (75.00%)  | 4 (3.33%)   | 11 (9.17%)  |     120 |
| 🔥 [smokeimages][ssb] 1                 | 15 (12.10%)  | 0           | 68 (54.84%)  | 40 (32.26%) | 1 (0.81%)   |     124 |
| 🔥 [debug_fib][ds] 02                   | 14 (11.67%)  | 0           | 75 (62.50%)  | 11 (9.17%)  | 20 (16.67%) |     120 |
| 🔥 [patch_file][ps] 03patch             | 14 (11.29%)  | 0           | 92 (74.19%)  | 5 (4.03%)   | 13 (10.48%) |     124 |
| 🔥 [crapto][cs] 20-b64-hex              | 12 (10.00%)  | 0           | 95 (79.17%)  | 5 (4.17%)   | 8 (6.67%)   |     120 |
| 🔥 [patch_file][ps] 11cat               | 10 (8.06%)   | 0           | 94 (75.81%)  | 3 (2.42%)   | 17 (13.71%) |     124 |
| 🔥 [debug_fib][ds] 03                   | 9 (7.50%)    | 0           | 97 (80.83%)  | 5 (4.17%)   | 9 (7.50%)   |     120 |
| 🔥 [patch_file][ps] 13patch             | 7 (5.65%)    | 0           | 91 (73.39%)  | 2 (1.61%)   | 24 (19.35%) |     124 |
| 🔥 [patch_file][ps] 02sed               | 6 (4.84%)    | 0           | 112 (90.32%) | 2 (1.61%)   | 4 (3.23%)   |     124 |
| 🔥 [patch_file][ps] 01cat               | 6 (4.84%)    | 0           | 107 (86.29%) | 3 (2.42%)   | 8 (6.45%)   |     124 |
| 🔥 [smokeimages][ssb] 3                 | 5 (4.03%)    | 0           | 106 (85.48%) | 2 (1.61%)   | 11 (8.87%)  |     124 |
| 🔥 [patch_file][ps] 10free              | 5 (4.03%)    | 0           | 97 (78.23%)  | 4 (3.23%)   | 18 (14.52%) |     124 |
| 🔥 [patch_file][ps] 15python            | 4 (3.23%)    | 0           | 110 (88.71%) | 1 (0.81%)   | 9 (7.26%)   |     124 |
| 🔥 [debug_fib][ds] 05                   | 3 (2.50%)    | 0           | 109 (90.83%) | 3 (2.50%)   | 5 (4.17%)   |     120 |
| 🔥 [crapto][cs] 42-xor-nokey            | 1 (0.83%)    | 0           | 88 (73.33%)  | 4 (3.33%)   | 27 (22.50%) |     120 |
| 🔥 [patch_file][ps] 14ed                | 1 (0.81%)    | 0           | 96 (77.42%)  | 4 (3.23%)   | 23 (18.55%) |     124 |
| 🔥 [patch_file][ps] 12sed               | 1 (0.81%)    | 0           | 106 (85.48%) | 4 (3.23%)   | 13 (10.48%) |     124 |
| 💀 [crapto][cs] 31-rot13-b64-hex-nohint | 0            | 0           | 104 (86.67%) | 3 (2.50%)   | 13 (10.83%) |     120 |
| 💀 [crapto][cs] 43-xor-nokey-nohint     | 0            | 0           | 95 (79.17%)  | 5 (4.17%)   | 20 (16.67%) |     120 |
| 💀 [crapto][cs] 30-rot13-b64-hex        | 0            | 0           | 100 (83.33%) | 6 (5.00%)   | 14 (11.67%) |     120 |


  [go120]: https://huggingface.co/unsloth/gpt-oss-120b-GGUF
  [go20]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [qc]: https://ollama.com/library/qwen3-coder
  [go]: https://ollama.com/library/gpt-oss
  [qt4]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [qa30]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [gh4]: https://huggingface.co/unsloth/granite-4.0-h-small-GGUF
  [q]: https://ollama.com/library/qwen3
  [qa30b]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [qv]: https://ollama.com/library/qwen3-vl
  [qi8]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [qt8]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [gi3]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [qi4]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [ms3]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [qc30]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [qi4b]: https://huggingface.co/NexaAI/qwen3vl-4B-Instruct-4bit-mlx
  [ms2509]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [gh4b]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [g]: https://ollama.com/library/granite4
  [go20b]: https://huggingface.co/NexaAI/gpt-oss-20b-MLX-4bit
  [q5]: https://ollama.com/library/qwen2.5vl
  [l2]: https://ollama.com/library/llama3.2
  [l]: https://ollama.com/library/llama3
  [mv]: https://ollama.com/library/minicpm-v
  [dr]: https://ollama.com/library/deepseek-r1
  [lv2]: https://ollama.com/library/llama3.2-vision
  [qm4]: https://huggingface.co/NexaAI/Qwen3-4B-4bit-MLX
  [gh4c]: https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF
  [gb]: https://ollama.com/library/gemma3
  [qt4b]: https://huggingface.co/NexaAI/qwen3vl-4B-Thinking-4bit-mlx
  [l1]: https://ollama.com/library/llama3.1
  [m]: https://ollama.com/library/magistral
  [ll]: https://ollama.com/library/llava-llama3
  [lb]: https://ollama.com/library/llava
  [gd]: https://ollama.com/library/granite3-dense
  [ms2]: https://ollama.com/library/mistral-small3.2
  [lp]: https://ollama.com/library/llava-phi3
  [la8]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [lc]: https://ollama.com/library/llama2
  [mb]: https://ollama.com/library/mistral
  [qc30b]: https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [qc5]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [gi3b]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [b]: https://ollama.com/library/bakllava
  [ss]: tests/smoketest.sh
  [hs]: tests/hello.sh
  [bs]: tests/basic_answers.sh
  [ssb]: tests/smokeimages.sh
  [ds]: tests/debug_fib.sh
  [cs]: tests/crapto.sh
  [ps]: tests/patch_file.sh

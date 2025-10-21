
<!--cut-->
# Model Results

This is a preliminary benchmark on some local models. The ranking should not be considered fair or rigorous since many uncontrolled variables impact it.

The benchmark is also used to check some local LLM servers. The slashless are run on ollama, the guff models are run on a llama.cpp server + llama-seap, and the mlx models are run on a nexa server.
* 39 models
* 6 testsuites
* 40 tests

## Results by models

| Model                                                            |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:-----------------------------------------------------------------|-------:|---------:|-------:|--------:|----------:|
| [qwen3-coder:30b][0]                                             |     30 |        0 |      7 |       0 |         3 |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][1] |     23 |        5 |      8 |       0 |         2 |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][2]             |     19 |        2 |      3 |       4 |        12 |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][3]                |     18 |        4 |      9 |       0 |         6 |
| [qwen2.5vl:latest][4]                                            |     18 |        0 |     24 |       0 |         0 |
| [llama3.2-vision:latest][5]                                      |     17 |        1 |     21 |       0 |         1 |
| [qwen3:latest][6]                                                |     17 |        1 |     12 |       0 |        10 |
| [magistral][7]                                                   |     16 |        3 |     17 |       0 |         3 |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][8]                  |     16 |        2 |     18 |       4 |         0 |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][9]            |     14 |        4 |     11 |       4 |         7 |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][10]                     |     14 |        3 |     17 |       4 |         2 |
| [gemma3:latest][11]                                              |     14 |        0 |     19 |       1 |         6 |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][12]                 |     13 |        3 |     12 |       4 |         8 |
| [llava-phi3:latest][13]                                          |     13 |        2 |     25 |       0 |         0 |
| [granite3-dense:latest][14]                                      |     12 |        3 |     24 |       0 |         1 |
| [llama3:latest][15]                                              |     12 |        2 |     24 |       0 |         2 |
| [llama3.2:latest][16]                                            |     12 |        1 |     25 |       1 |         1 |
| [qwen3:4b][6]                                                    |     12 |        0 |     12 |       0 |        16 |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][17]                          |     11 |        4 |     13 |       4 |         8 |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][18]                   |     11 |        3 |     17 |       4 |         4 |
| [llama2:7b][19]                                                  |     11 |        0 |     29 |       0 |         0 |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][20]                           |     11 |        0 |     25 |       4 |         0 |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][21]                |     10 |        2 |     24 |       4 |         0 |
| [mistral][22]                                                    |     10 |        1 |     25 |       1 |         1 |
| [llava-llama3:latest][23]                                        |     10 |        0 |     30 |       0 |         0 |
| [llava:latest][24]                                               |     10 |        0 |     30 |       0 |         0 |
| [minicpm-v:latest][25]                                           |      9 |        1 |     29 |       0 |         1 |
| [unsloth/gpt-oss-120b-GGUF][26]                                  |      9 |        1 |     26 |       4 |         0 |
| [llama2:latest][19]                                              |      9 |        0 |     31 |       0 |         0 |
| [bakllava:latest][27]                                            |      8 |        1 |     31 |       0 |         0 |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][28]                            |      8 |        1 |     24 |       4 |         1 |
| [deepseek-r1:14b][29]                                            |      8 |        0 |      6 |       0 |        26 |
| [ggml-org/gemma-3-1b-it-GGUF][30]                                |      6 |        0 |     21 |       5 |         8 |
| [gpt-oss:latest][31]                                             |      5 |        0 |     35 |       0 |         0 |
| [deepseek-r1:latest][29]                                         |      2 |        1 |      4 |       0 |        31 |
| [NexaAI/Qwen3-4B-4bit-MLX][32]                                   |      1 |        0 |     21 |       0 |        16 |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][33]                        |      1 |        0 |     36 |       1 |         0 |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][34]                        |      1 |        0 |     36 |       1 |         0 |
| [NexaAI/gpt-oss-20b-MLX-4bit][35]                                |      1 |        0 |     32 |       5 |         0 |

## Passed tests by models

| Models                                                           |   [smoketest][36] |   [test_utils][37] |   [smokeimages][38] |   [basic_answers][39] |   [hello][40] |   [patch_file][41] |
|:-----------------------------------------------------------------|------------------:|-------------------:|--------------------:|----------------------:|--------------:|-------------------:|
| [qwen3-coder:30b][0]                                             |                12 |                  1 |                   1 |                     5 |             4 |                  7 |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][1] |                13 |                  1 |                   3 |                     0 |             2 |                  4 |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][2]             |                13 |                  1 |                   1 |                     2 |             2 |                  0 |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][3]                |                11 |                  1 |                   1 |                     0 |             2 |                  3 |
| [qwen2.5vl:latest][4]                                            |                 9 |                  3 |                   4 |                     1 |             1 |                  0 |
| [llama3.2-vision:latest][5]                                      |                11 |                  1 |                   3 |                     2 |             0 |                  0 |
| [qwen3:latest][6]                                                |                13 |                  1 |                   0 |                     1 |             1 |                  1 |
| [magistral][7]                                                   |                12 |                  1 |                   1 |                     1 |             1 |                  0 |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][8]                  |                12 |                  1 |                   0 |                     2 |             1 |                  0 |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][9]            |                10 |                  1 |                   0 |                     0 |             3 |                  0 |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][10]                     |                 9 |                  1 |                   0 |                     2 |             2 |                  0 |
| [gemma3:latest][11]                                              |                 7 |                  1 |                   3 |                     2 |             1 |                  0 |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][12]                 |                11 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llava-phi3:latest][13]                                          |                 9 |                  1 |                   3 |                     0 |             0 |                  0 |
| [granite3-dense:latest][14]                                      |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llama3:latest][15]                                              |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llama3.2:latest][16]                                            |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [qwen3:4b][6]                                                    |                 9 |                  1 |                   0 |                     2 |             0 |                  0 |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][17]                          |                 7 |                  1 |                   0 |                     1 |             1 |                  1 |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][18]                   |                 9 |                  1 |                   0 |                     0 |             1 |                  0 |
| [llama2:7b][19]                                                  |                 8 |                  1 |                   2 |                     0 |             0 |                  0 |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][20]                           |                 8 |                  1 |                   0 |                     2 |             0 |                  0 |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][21]                |                 9 |                  1 |                   0 |                     0 |             0 |                  0 |
| [mistral][22]                                                    |                 8 |                  1 |                   1 |                     0 |             0 |                  0 |
| [llava-llama3:latest][23]                                        |                 5 |                  1 |                   3 |                     1 |             0 |                  0 |
| [llava:latest][24]                                               |                 5 |                  1 |                   4 |                     0 |             0 |                  0 |
| [minicpm-v:latest][25]                                           |                 4 |                  1 |                   3 |                     1 |             0 |                  0 |
| [unsloth/gpt-oss-120b-GGUF][26]                                  |                 8 |                  1 |                   0 |                     0 |             0 |                  0 |
| [llama2:latest][19]                                              |                 6 |                  1 |                   1 |                     1 |             0 |                  0 |
| [bakllava:latest][27]                                            |                 3 |                  1 |                   4 |                     0 |             0 |                  0 |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][28]                            |                 7 |                  1 |                   0 |                     0 |             0 |                  0 |
| [deepseek-r1:14b][29]                                            |                 6 |                  1 |                   0 |                     1 |             0 |                  0 |
| [ggml-org/gemma-3-1b-it-GGUF][30]                                |                 4 |                  1 |                   0 |                     1 |             0 |                  0 |
| [gpt-oss:latest][31]                                             |                 3 |                  1 |                   0 |                     1 |             0 |                  0 |
| [deepseek-r1:latest][29]                                         |                 0 |                  1 |                   1 |                     0 |             0 |                  0 |
| [NexaAI/Qwen3-4B-4bit-MLX][32]                                   |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][33]                        |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][34]                        |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/gpt-oss-20b-MLX-4bit][35]                                |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |

## Results by testsuites

| Model               |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:--------------------|-------:|---------:|-------:|--------:|----------:|
| [smoketest][36]     |    291 |        0 |    157 |       4 |        55 |
| [test_utils][37]    |     41 |        0 |      0 |       0 |         0 |
| [smokeimages][38]   |     39 |        0 |     91 |      54 |        11 |
| [basic_answers][39] |     33 |       51 |     90 |       0 |        21 |
| [hello][40]         |     22 |        0 |     97 |       0 |        16 |
| [patch_file][41]    |     16 |        0 |    378 |       1 |        73 |

## Results by tests

| Model                       |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:----------------------------|-------:|---------:|-------:|--------:|----------:|
| [test_utils][37] 00         |     41 |        0 |      0 |       0 |         0 |
| [smoketest][36] 32          |     30 |        0 |      6 |       0 |         3 |
| [smoketest][36] 06          |     30 |        0 |      5 |       0 |         4 |
| [smoketest][36] 05          |     30 |        0 |      7 |       0 |         2 |
| [smoketest][36] 03          |     30 |        0 |      6 |       0 |         3 |
| [smoketest][36] 04          |     29 |        0 |      7 |       0 |         3 |
| [smoketest][36] 33          |     26 |        0 |     10 |       1 |         2 |
| [smoketest][36] 01          |     23 |        0 |      6 |       0 |        10 |
| [smoketest][36] 02          |     19 |        0 |      7 |       2 |        11 |
| [smoketest][36] 11          |     17 |        0 |     20 |       0 |         2 |
| [smoketest][36] 13          |     16 |        0 |     20 |       0 |         3 |
| [basic_answers][39] 0.paris |     15 |       16 |      7 |       0 |         1 |
| [basic_answers][39] 4.fact  |     15 |        6 |     15 |       0 |         3 |
| [smoketest][36] 12          |     15 |        0 |     21 |       0 |         3 |
| [smoketest][36] 10          |     15 |        0 |     22 |       0 |         2 |
| [smokeimages][38] 4         |     13 |        0 |     10 |      13 |         3 |
| [smoketest][36] 31          |     11 |        0 |     20 |       1 |         7 |
| [smokeimages][38] 2         |      9 |        0 |     15 |      13 |         2 |
| [smokeimages][38] 0         |      9 |        0 |     15 |      13 |         2 |
| [hello][40] 02name          |      7 |        0 |     27 |       0 |         5 |
| [smokeimages][38] 1         |      7 |        0 |     17 |      14 |         1 |
| [hello][40] 01world         |      6 |        0 |     30 |       0 |         3 |
| [hello][40] 03git           |      6 |        0 |     19 |       0 |         4 |
| [patch_file][41] 05python   |      4 |        0 |     30 |       0 |         5 |
| [patch_file][41] 04ed       |      3 |        0 |     30 |       0 |         6 |
| [patch_file][41] 03patch    |      3 |        0 |     31 |       0 |         5 |
| [hello][40] 04gitignore     |      3 |        0 |     21 |       0 |         4 |
| [patch_file][41] 01cat      |      2 |        0 |     32 |       0 |         5 |
| [patch_file][41] 00free     |      2 |        0 |     33 |       0 |         4 |
| [basic_answers][39] 3.llme  |      1 |       11 |     23 |       0 |         4 |
| [basic_answers][39] 2.llme  |      1 |       10 |     22 |       0 |         6 |
| [basic_answers][39] 1.llme  |      1 |        8 |     23 |       0 |         7 |
| [patch_file][41] 11cat      |      1 |        0 |     33 |       0 |         5 |
| [patch_file][41] 02sed      |      1 |        0 |     30 |       0 |         8 |
| [smokeimages][38] 3         |      1 |        0 |     34 |       1 |         3 |
| [patch_file][41] 14ed       |      0 |        0 |     30 |       0 |         9 |
| [patch_file][41] 13patch    |      0 |        0 |     33 |       0 |         6 |
| [patch_file][41] 12sed      |      0 |        0 |     33 |       0 |         6 |
| [patch_file][41] 10free     |      0 |        0 |     34 |       0 |         5 |
| [patch_file][41] 15python   |      0 |        0 |     29 |       1 |         9 |

  [0]: https://ollama.com/library/qwen3-coder
  [1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [2]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [3]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [4]: https://ollama.com/library/qwen2.5vl
  [5]: https://ollama.com/library/llama3.2-vision
  [6]: https://ollama.com/library/qwen3
  [7]: https://ollama.com/library/magistral
  [8]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [9]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [10]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [11]: https://ollama.com/library/gemma3
  [12]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [13]: https://ollama.com/library/llava-phi3
  [14]: https://ollama.com/library/granite3-dense
  [15]: https://ollama.com/library/llama3
  [16]: https://ollama.com/library/llama3.2
  [17]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [18]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [19]: https://ollama.com/library/llama2
  [20]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [21]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [22]: https://ollama.com/library/mistral
  [23]: https://ollama.com/library/llava-llama3
  [24]: https://ollama.com/library/llava
  [25]: https://ollama.com/library/minicpm-v
  [26]: https://huggingface.co/unsloth/gpt-oss-120b-GGUF
  [27]: https://ollama.com/library/bakllava
  [28]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [29]: https://ollama.com/library/deepseek-r1
  [30]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [31]: https://ollama.com/library/gpt-oss
  [32]: https://huggingface.co/NexaAI/Qwen3-4B-4bit-MLX
  [33]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [34]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [35]: https://huggingface.co/NexaAI/gpt-oss-20b-MLX-4bit
  [36]: tests/smoketest.sh
  [37]: tests/test_utils.sh
  [38]: tests/smokeimages.sh
  [39]: tests/basic_answers.sh
  [40]: tests/hello.sh
  [41]: tests/patch_file.sh

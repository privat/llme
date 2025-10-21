
<!--cut-->
# Model Results

This is a preliminary benchmark on some local models. The ranking should not be considered fair or rigorous since many uncontrolled variables impact it.

The benchmark is also used to check some local LLM servers. The slashless are run on ollama, the guff models are run on a llama.cpp server + llama-seap, and the mlx models are run on a nexa server.
* 43 models
* 6 testsuites
* 40 tests

## Results by models

| Model                                                             |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:------------------------------------------------------------------|-------:|---------:|-------:|--------:|----------:|
| [qwen3-coder:30b][0]                                              |     30 |        0 |      7 |       0 |         3 |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][1]  |     23 |        5 |      8 |       0 |         2 |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][2]              |     19 |        2 |      3 |       4 |        12 |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][3]                 |     18 |        4 |      9 |       0 |         6 |
| [llama3.2-vision:latest][4]                                       |     17 |        1 |     21 |       0 |         1 |
| [qwen3:latest][5]                                                 |     17 |        1 |     12 |       0 |        10 |
| [magistral:latest][6]                                             |     16 |        3 |     17 |       0 |         3 |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][7]                   |     16 |        2 |     18 |       4 |         0 |
| [qwen2.5vl:latest][8]                                             |     15 |        0 |     25 |       0 |         0 |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][9]             |     14 |        4 |     11 |       4 |         7 |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][10]                      |     14 |        3 |     17 |       4 |         2 |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][11] |     14 |        1 |     11 |       4 |        10 |
| [gemma3:latest][12]                                               |     14 |        0 |     19 |       1 |         6 |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][13]                  |     13 |        3 |     12 |       4 |         8 |
| [llava-phi3:latest][14]                                           |     13 |        2 |     25 |       0 |         0 |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][15]                     |     12 |        5 |     11 |       4 |         8 |
| [granite3-dense:latest][16]                                       |     12 |        3 |     24 |       0 |         1 |
| [llama3:latest][17]                                               |     12 |        2 |     24 |       0 |         2 |
| [llama3.2:latest][18]                                             |     12 |        1 |     25 |       1 |         1 |
| [qwen3:4b][5]                                                     |     12 |        0 |     12 |       0 |        16 |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][19]                           |     11 |        4 |     13 |       4 |         8 |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][20]                    |     11 |        3 |     17 |       4 |         4 |
| [llama2:7b][21]                                                   |     11 |        0 |     29 |       0 |         0 |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][22]                            |     11 |        0 |     25 |       4 |         0 |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][23]                      |     10 |        4 |      8 |       6 |        12 |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][24]                 |     10 |        2 |     24 |       4 |         0 |
| [mistral:latest][25]                                              |     10 |        1 |     25 |       1 |         1 |
| [llava-llama3:latest][26]                                         |     10 |        0 |     30 |       0 |         0 |
| [llava:latest][27]                                                |     10 |        0 |     30 |       0 |         0 |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][28]                            |      9 |        3 |     24 |       4 |         0 |
| [minicpm-v:latest][29]                                            |      9 |        1 |     29 |       0 |         1 |
| [unsloth/gpt-oss-120b-GGUF][28]                                   |      9 |        1 |     26 |       4 |         0 |
| [llama2:latest][21]                                               |      9 |        0 |     31 |       0 |         0 |
| [bakllava:latest][30]                                             |      8 |        1 |     31 |       0 |         0 |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][31]                             |      8 |        1 |     24 |       4 |         1 |
| [deepseek-r1:14b][32]                                             |      8 |        0 |      6 |       0 |        26 |
| [gpt-oss:latest][33]                                              |      5 |        0 |     35 |       0 |         0 |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][34]                          |      3 |        2 |     14 |       5 |        16 |
| [deepseek-r1:latest][32]                                          |      2 |        1 |      4 |       0 |        31 |
| [NexaAI/Qwen3-4B-4bit-MLX][35]                                    |      1 |        0 |     21 |       0 |        16 |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][36]                         |      1 |        0 |     36 |       1 |         0 |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][37]                         |      1 |        0 |     36 |       1 |         0 |
| [NexaAI/gpt-oss-20b-MLX-4bit][38]                                 |      1 |        0 |     32 |       5 |         0 |

## Passed tests by models

| Models                                                            |   [smoketest][39] |   [test_utils][40] |   [smokeimages][41] |   [basic_answers][42] |   [hello][43] |   [patch_file][44] |
|:------------------------------------------------------------------|------------------:|-------------------:|--------------------:|----------------------:|--------------:|-------------------:|
| [qwen3-coder:30b][0]                                              |                12 |                  1 |                   1 |                     5 |             4 |                  7 |
| [unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL][1]  |                13 |                  1 |                   3 |                     0 |             2 |                  4 |
| [unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M][2]              |                13 |                  1 |                   1 |                     2 |             2 |                  0 |
| [unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL][3]                 |                11 |                  1 |                   1 |                     0 |             2 |                  3 |
| [llama3.2-vision:latest][4]                                       |                11 |                  1 |                   3 |                     2 |             0 |                  0 |
| [qwen3:latest][5]                                                 |                13 |                  1 |                   0 |                     1 |             1 |                  1 |
| [magistral:latest][6]                                             |                12 |                  1 |                   1 |                     1 |             1 |                  0 |
| [unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M][7]                   |                12 |                  1 |                   0 |                     2 |             1 |                  0 |
| [qwen2.5vl:latest][8]                                             |                 9 |                  1 |                   4 |                     1 |             0 |                  0 |
| [unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][9]             |                10 |                  1 |                   0 |                     0 |             3 |                  0 |
| [unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M][10]                      |                 9 |                  1 |                   0 |                     2 |             2 |                  0 |
| [lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M][11] |                10 |                  1 |                   0 |                     0 |             1 |                  2 |
| [gemma3:latest][12]                                               |                 7 |                  1 |                   3 |                     2 |             1 |                  0 |
| [unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M][13]                  |                11 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llava-phi3:latest][14]                                           |                 9 |                  1 |                   3 |                     0 |             0 |                  0 |
| [unsloth/granite-4.0-h-small-GGUF:Q4_K_M][15]                     |                 9 |                  1 |                   0 |                     0 |             2 |                  0 |
| [granite3-dense:latest][16]                                       |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llama3:latest][17]                                               |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [llama3.2:latest][18]                                             |                10 |                  1 |                   0 |                     1 |             0 |                  0 |
| [qwen3:4b][5]                                                     |                 9 |                  1 |                   0 |                     2 |             0 |                  0 |
| [unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M][19]                           |                 7 |                  1 |                   0 |                     1 |             1 |                  1 |
| [ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0][20]                    |                 9 |                  1 |                   0 |                     0 |             1 |                  0 |
| [llama2:7b][21]                                                   |                 8 |                  1 |                   2 |                     0 |             0 |                  0 |
| [LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M][22]                            |                 8 |                  1 |                   0 |                     2 |             0 |                  0 |
| [unsloth/granite-4.0-h-tiny-GGUF:Q4_K_M][23]                      |                 9 |                  1 |                   0 |                     0 |             0 |                  0 |
| [ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M][24]                 |                 9 |                  1 |                   0 |                     0 |             0 |                  0 |
| [mistral:latest][25]                                              |                 8 |                  1 |                   1 |                     0 |             0 |                  0 |
| [llava-llama3:latest][26]                                         |                 5 |                  1 |                   3 |                     1 |             0 |                  0 |
| [llava:latest][27]                                                |                 5 |                  1 |                   4 |                     0 |             0 |                  0 |
| [unsloth/gpt-oss-120b-GGUF:Q4_K_M][28]                            |                 8 |                  1 |                   0 |                     0 |             0 |                  0 |
| [minicpm-v:latest][29]                                            |                 4 |                  1 |                   3 |                     1 |             0 |                  0 |
| [unsloth/gpt-oss-120b-GGUF][28]                                   |                 8 |                  1 |                   0 |                     0 |             0 |                  0 |
| [llama2:latest][21]                                               |                 6 |                  1 |                   1 |                     1 |             0 |                  0 |
| [bakllava:latest][30]                                             |                 3 |                  1 |                   4 |                     0 |             0 |                  0 |
| [unsloth/gpt-oss-20b-GGUF:Q4_K_M][31]                             |                 7 |                  1 |                   0 |                     0 |             0 |                  0 |
| [deepseek-r1:14b][32]                                             |                 6 |                  1 |                   0 |                     1 |             0 |                  0 |
| [gpt-oss:latest][33]                                              |                 3 |                  1 |                   0 |                     1 |             0 |                  0 |
| [ggml-org/gemma-3-1b-it-GGUF:Q4_K_M][34]                          |                 2 |                  1 |                   0 |                     0 |             0 |                  0 |
| [deepseek-r1:latest][32]                                          |                 0 |                  1 |                   1 |                     0 |             0 |                  0 |
| [NexaAI/Qwen3-4B-4bit-MLX][35]                                    |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/qwen3vl-8B-Thinking-4bit-mlx][36]                         |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/qwen3vl-8B-Instruct-4bit-mlx][37]                         |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |
| [NexaAI/gpt-oss-20b-MLX-4bit][38]                                 |                 0 |                  1 |                   0 |                     0 |             0 |                  0 |

## Results by testsuites

| Model               |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:--------------------|-------:|---------:|-------:|--------:|----------:|
| [smoketest][39]     |    325 |        0 |    160 |       6 |        68 |
| [test_utils][40]    |     43 |        0 |      0 |       0 |         0 |
| [smokeimages][41]   |     39 |        0 |     94 |      70 |        12 |
| [basic_answers][42] |     32 |       66 |     93 |       0 |        24 |
| [hello][43]         |     24 |        0 |    108 |       0 |        19 |
| [patch_file][44]    |     18 |        0 |    406 |       1 |        91 |

## Results by tests

| Model                       |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:----------------------------|-------:|---------:|-------:|--------:|----------:|
| [test_utils][40] 00         |     43 |        0 |      0 |       0 |         0 |
| [smoketest][39] 03          |     34 |        0 |      6 |       0 |         3 |
| [smoketest][39] 05          |     33 |        0 |      7 |       0 |         3 |
| [smoketest][39] 04          |     33 |        0 |      7 |       0 |         3 |
| [smoketest][39] 32          |     32 |        0 |      6 |       0 |         5 |
| [smoketest][39] 06          |     32 |        0 |      5 |       0 |         6 |
| [smoketest][39] 33          |     28 |        0 |     10 |       1 |         4 |
| [smoketest][39] 01          |     25 |        0 |      6 |       1 |        11 |
| [smoketest][39] 02          |     22 |        0 |      6 |       3 |        12 |
| [smoketest][39] 11          |     21 |        0 |     20 |       0 |         2 |
| [smoketest][39] 13          |     18 |        0 |     21 |       0 |         4 |
| [smoketest][39] 12          |     17 |        0 |     22 |       0 |         4 |
| [smoketest][39] 10          |     16 |        0 |     24 |       0 |         3 |
| [basic_answers][42] 0.paris |     15 |       21 |      6 |       0 |         1 |
| [basic_answers][42] 4.fact  |     14 |        9 |     17 |       0 |         3 |
| [smoketest][39] 31          |     14 |        0 |     20 |       1 |         8 |
| [smokeimages][41] 4         |     13 |        0 |     10 |      17 |         3 |
| [smokeimages][41] 2         |      9 |        0 |     15 |      17 |         2 |
| [smokeimages][41] 0         |      9 |        0 |     15 |      17 |         2 |
| [hello][43] 02name          |      7 |        0 |     31 |       0 |         5 |
| [hello][43] 03git           |      7 |        0 |     20 |       0 |         6 |
| [smokeimages][41] 1         |      7 |        0 |     17 |      18 |         1 |
| [hello][43] 01world         |      6 |        0 |     34 |       0 |         3 |
| [patch_file][44] 05python   |      5 |        0 |     33 |       0 |         5 |
| [patch_file][44] 04ed       |      4 |        0 |     32 |       0 |         7 |
| [hello][43] 04gitignore     |      4 |        0 |     23 |       0 |         5 |
| [patch_file][44] 03patch    |      3 |        0 |     33 |       0 |         7 |
| [patch_file][44] 01cat      |      2 |        0 |     34 |       0 |         7 |
| [patch_file][44] 00free     |      2 |        0 |     35 |       0 |         6 |
| [basic_answers][42] 3.llme  |      1 |       13 |     24 |       0 |         5 |
| [basic_answers][42] 2.llme  |      1 |       12 |     23 |       0 |         7 |
| [basic_answers][42] 1.llme  |      1 |       11 |     23 |       0 |         8 |
| [patch_file][44] 11cat      |      1 |        0 |     36 |       0 |         6 |
| [patch_file][44] 02sed      |      1 |        0 |     33 |       0 |         9 |
| [smokeimages][41] 3         |      1 |        0 |     37 |       1 |         4 |
| [patch_file][44] 14ed       |      0 |        0 |     33 |       0 |        10 |
| [patch_file][44] 13patch    |      0 |        0 |     35 |       0 |         8 |
| [patch_file][44] 12sed      |      0 |        0 |     36 |       0 |         7 |
| [patch_file][44] 10free     |      0 |        0 |     35 |       0 |         8 |
| [patch_file][44] 15python   |      0 |        0 |     31 |       1 |        11 |

  [0]: https://ollama.com/library/qwen3-coder
  [1]: https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF
  [2]: https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF
  [3]: https://huggingface.co/unsloth/Magistral-Small-2509-GGUF
  [4]: https://ollama.com/library/llama3.2-vision
  [5]: https://ollama.com/library/qwen3
  [6]: https://ollama.com/library/magistral
  [7]: https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
  [8]: https://ollama.com/library/qwen2.5vl
  [9]: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [10]: https://huggingface.co/unsloth/gemma-3-12b-it-qat-GGUF
  [11]: https://huggingface.co/lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-GGUF
  [12]: https://ollama.com/library/gemma3
  [13]: https://huggingface.co/unsloth/Qwen3-4B-Thinking-2507-GGUF
  [14]: https://ollama.com/library/llava-phi3
  [15]: https://huggingface.co/unsloth/granite-4.0-h-small-GGUF
  [16]: https://ollama.com/library/granite3-dense
  [17]: https://ollama.com/library/llama3
  [18]: https://ollama.com/library/llama3.2
  [19]: https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF
  [20]: https://huggingface.co/ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF
  [21]: https://ollama.com/library/llama2
  [22]: https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF
  [23]: https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF
  [24]: https://huggingface.co/ibm-granite/granite-4.0-h-micro-GGUF
  [25]: https://ollama.com/library/mistral
  [26]: https://ollama.com/library/llava-llama3
  [27]: https://ollama.com/library/llava
  [28]: https://huggingface.co/unsloth/gpt-oss-120b-GGUF
  [29]: https://ollama.com/library/minicpm-v
  [30]: https://ollama.com/library/bakllava
  [31]: https://huggingface.co/unsloth/gpt-oss-20b-GGUF
  [32]: https://ollama.com/library/deepseek-r1
  [33]: https://ollama.com/library/gpt-oss
  [34]: https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF
  [35]: https://huggingface.co/NexaAI/Qwen3-4B-4bit-MLX
  [36]: https://huggingface.co/NexaAI/qwen3vl-8B-Thinking-4bit-mlx
  [37]: https://huggingface.co/NexaAI/qwen3vl-8B-Instruct-4bit-mlx
  [38]: https://huggingface.co/NexaAI/gpt-oss-20b-MLX-4bit
  [39]: tests/smoketest.sh
  [40]: tests/test_utils.sh
  [41]: tests/smokeimages.sh
  [42]: tests/basic_answers.sh
  [43]: tests/hello.sh
  [44]: tests/patch_file.sh

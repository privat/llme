# Model Results

* 36 models
* 6 testsuites
* 40 tests

## Results by models

| Model                                                       |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:------------------------------------------------------------|-------:|---------:|-------:|--------:|----------:|
| qwen3-coder:30b                                             |     26 |        2 |      9 |       0 |         3 |
| unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M             |     19 |        2 |      3 |       4 |        12 |
| qwen2.5vl:latest                                            |     18 |        0 |     24 |       0 |         0 |
| llama3.2-vision:latest                                      |     17 |        1 |     21 |       0 |         1 |
| qwen3:latest                                                |     17 |        1 |     12 |       0 |        10 |
| unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M                  |     16 |        2 |     18 |       4 |         0 |
| unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M            |     15 |        3 |     12 |       4 |         6 |
| unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M                      |     14 |        3 |     17 |       4 |         2 |
| gemma3:latest                                               |     14 |        0 |     19 |       1 |         6 |
| magistral:latest                                            |     13 |        3 |     21 |       0 |         3 |
| unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M                  |     13 |        3 |     12 |       4 |         8 |
| llava-phi3:latest                                           |     13 |        2 |     25 |       0 |         0 |
| granite3-dense:latest                                       |     12 |        3 |     24 |       0 |         1 |
| llama3:latest                                               |     12 |        2 |     24 |       0 |         2 |
| llama3.2:latest                                             |     12 |        1 |     25 |       1 |         1 |
| qwen3:4b                                                    |     12 |        0 |     12 |       0 |        16 |
| unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M                           |     11 |        4 |     13 |       4 |         8 |
| ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0                    |     11 |        3 |     18 |       4 |         4 |
| llama2:7b                                                   |     11 |        0 |     29 |       0 |         0 |
| LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M                            |     11 |        0 |     25 |       4 |         0 |
| ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M                 |     10 |        2 |     24 |       4 |         0 |
| llava-llama3:latest                                         |     10 |        0 |     30 |       0 |         0 |
| llava:latest                                                |     10 |        0 |     30 |       0 |         0 |
| mistral:latest                                              |      9 |        3 |     27 |       0 |         1 |
| minicpm-v:latest                                            |      9 |        1 |     29 |       0 |         1 |
| unsloth/gpt-oss-120b-GGUF                                   |      9 |        1 |     26 |       4 |         0 |
| llama2:latest                                               |      9 |        0 |     31 |       0 |         0 |
| bakllava:latest                                             |      8 |        1 |     31 |       0 |         0 |
| deepseek-r1:14b                                             |      8 |        0 |      6 |       0 |        26 |
| ggml-org/gemma-3-1b-it-GGUF                                 |      6 |        0 |     21 |       5 |         8 |
| gpt-oss:latest                                              |      5 |        0 |     35 |       0 |         0 |
| unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL |      5 |        0 |      1 |      34 |         0 |
| deepseek-r1:latest                                          |      3 |        0 |      5 |       0 |        32 |
| unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL                |      1 |        0 |      4 |      35 |         0 |
| llbingo:latest                                              |      1 |        0 |      0 |      39 |         0 |
| unsloth/gpt-oss-20b-GGUF                                    |      1 |        0 |      0 |      39 |         0 |

## Passed tests by models

| Model                                                       |   smoketest |   test_utils |   smokeimages |   basic_answers |   hello |   patch_file |
|:------------------------------------------------------------|------------:|-------------:|--------------:|----------------:|--------:|-------------:|
| qwen3-coder:30b                                             |          13 |            1 |             1 |               3 |       4 |            4 |
| unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF:Q4_K_M             |          13 |            1 |             1 |               2 |       2 |            0 |
| qwen2.5vl:latest                                            |           9 |            3 |             4 |               1 |       1 |            0 |
| llama3.2-vision:latest                                      |          11 |            1 |             3 |               2 |       0 |            0 |
| qwen3:latest                                                |          13 |            1 |             0 |               1 |       1 |            1 |
| unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M                  |          12 |            1 |             0 |               2 |       1 |            0 |
| unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q4_K_M            |          10 |            1 |             0 |               1 |       3 |            0 |
| unsloth/gemma-3-12b-it-qat-GGUF:Q4_K_M                      |           9 |            1 |             0 |               2 |       2 |            0 |
| gemma3:latest                                               |           7 |            1 |             3 |               2 |       1 |            0 |
| magistral:latest                                            |           8 |            1 |             0 |               0 |       3 |            1 |
| unsloth/Qwen3-4B-Thinking-2507-GGUF:Q4_K_M                  |          11 |            1 |             0 |               1 |       0 |            0 |
| llava-phi3:latest                                           |           9 |            1 |             3 |               0 |       0 |            0 |
| granite3-dense:latest                                       |          10 |            1 |             0 |               1 |       0 |            0 |
| llama3:latest                                               |          10 |            1 |             0 |               1 |       0 |            0 |
| llama3.2:latest                                             |          10 |            1 |             0 |               1 |       0 |            0 |
| qwen3:4b                                                    |           9 |            1 |             0 |               2 |       0 |            0 |
| unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M                           |           7 |            1 |             0 |               1 |       1 |            1 |
| ggml-org/Qwen2.5-Coder-7B-Q8_0-GGUF:Q8_0                    |           9 |            1 |             0 |               0 |       1 |            0 |
| llama2:7b                                                   |           8 |            1 |             2 |               0 |       0 |            0 |
| LiquidAI/LFM2-8B-A1B-GGUF:Q4_K_M                            |           8 |            1 |             0 |               2 |       0 |            0 |
| ibm-granite/granite-4.0-h-micro-GGUF:Q4_K_M                 |           9 |            1 |             0 |               0 |       0 |            0 |
| llava-llama3:latest                                         |           5 |            1 |             3 |               1 |       0 |            0 |
| llava:latest                                                |           5 |            1 |             4 |               0 |       0 |            0 |
| mistral:latest                                              |           7 |            1 |             1 |               0 |       0 |            0 |
| minicpm-v:latest                                            |           4 |            1 |             3 |               1 |       0 |            0 |
| unsloth/gpt-oss-120b-GGUF                                   |           8 |            1 |             0 |               0 |       0 |            0 |
| llama2:latest                                               |           6 |            1 |             1 |               1 |       0 |            0 |
| bakllava:latest                                             |           3 |            1 |             4 |               0 |       0 |            0 |
| deepseek-r1:14b                                             |           6 |            1 |             0 |               1 |       0 |            0 |
| ggml-org/gemma-3-1b-it-GGUF                                 |           4 |            1 |             0 |               1 |       0 |            0 |
| gpt-oss:latest                                              |           3 |            1 |             0 |               1 |       0 |            0 |
| unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF:UD-Q4_K_XL |           1 |            1 |             3 |               0 |       0 |            0 |
| deepseek-r1:latest                                          |           1 |            1 |             0 |               1 |       0 |            0 |
| unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL                |           0 |            1 |             0 |               0 |       0 |            0 |
| llbingo:latest                                              |           0 |            1 |             0 |               0 |       0 |            0 |
| unsloth/gpt-oss-20b-GGUF                                    |           0 |            1 |             0 |               0 |       0 |            0 |

## Results by testsuites

| Model         |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:--------------|-------:|---------:|-------:|--------:|----------:|
| smoketest     |    258 |        0 |    114 |      52 |        44 |
| test_utils    |     38 |        0 |      0 |       0 |         0 |
| smokeimages   |     36 |        0 |     78 |      58 |         8 |
| basic_answers |     32 |       43 |     69 |      20 |        16 |
| hello         |     20 |        0 |     91 |      16 |        17 |
| patch_file    |      7 |        0 |    311 |      48 |        66 |

## Results by tests

| Model                 |   PASS |   ALMOST |   FAIL |   ERROR |   TIMEOUT |
|:----------------------|-------:|---------:|-------:|--------:|----------:|
| test_utils 00         |     38 |        0 |      0 |       0 |         0 |
| smoketest 32          |     28 |        0 |      3 |       3 |         2 |
| smoketest 06          |     28 |        0 |      1 |       4 |         3 |
| smoketest 05          |     27 |        0 |      3 |       4 |         2 |
| smoketest 03          |     27 |        0 |      2 |       4 |         3 |
| smoketest 04          |     26 |        0 |      3 |       4 |         3 |
| smoketest 33          |     24 |        0 |      6 |       5 |         1 |
| smoketest 01          |     20 |        0 |      4 |       4 |         8 |
| basic_answers 0.paris |     16 |       12 |      3 |       4 |         1 |
| smoketest 02          |     16 |        0 |      5 |       4 |        11 |
| basic_answers 4.fact  |     15 |        4 |     12 |       4 |         1 |
| smoketest 13          |     14 |        0 |     16 |       4 |         2 |
| smoketest 11          |     14 |        0 |     17 |       4 |         1 |
| smoketest 12          |     13 |        0 |     18 |       4 |         1 |
| smoketest 10          |     12 |        0 |     19 |       4 |         1 |
| smoketest 31          |      9 |        0 |     17 |       4 |         6 |
| smokeimages 2         |      9 |        0 |     12 |      13 |         2 |
| smokeimages 0         |      9 |        0 |     13 |      13 |         1 |
| smokeimages 4         |      9 |        0 |      9 |      15 |         3 |
| smokeimages 1         |      8 |        0 |     14 |      14 |         0 |
| hello 03git           |      7 |        0 |     20 |       4 |         5 |
| hello 02name          |      5 |        0 |     23 |       4 |         4 |
| hello 01world         |      5 |        0 |     24 |       4 |         3 |
| patch_file 04ed       |      3 |        0 |     23 |       4 |         6 |
| hello 04gitignore     |      3 |        0 |     24 |       4 |         5 |
| patch_file 05python   |      2 |        0 |     25 |       4 |         5 |
| basic_answers 1.llme  |      1 |        8 |     18 |       4 |         5 |
| smokeimages 3         |      1 |        0 |     30 |       3 |         2 |
| patch_file 03patch    |      1 |        0 |     27 |       4 |         4 |
| patch_file 00free     |      1 |        0 |     27 |       4 |         4 |
| basic_answers 3.llme  |      0 |       11 |     17 |       4 |         4 |
| basic_answers 2.llme  |      0 |        8 |     19 |       4 |         5 |
| patch_file 15python   |      0 |        0 |     25 |       4 |         7 |
| patch_file 14ed       |      0 |        0 |     25 |       4 |         7 |
| patch_file 13patch    |      0 |        0 |     26 |       4 |         6 |
| patch_file 12sed      |      0 |        0 |     27 |       4 |         5 |
| patch_file 11cat      |      0 |        0 |     29 |       4 |         3 |
| patch_file 10free     |      0 |        0 |     26 |       4 |         6 |
| patch_file 02sed      |      0 |        0 |     24 |       4 |         8 |
| patch_file 01cat      |      0 |        0 |     27 |       4 |         5 |

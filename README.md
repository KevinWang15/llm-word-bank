# llm-word-bank

## 安装依赖

 ```bash
 pip install -r requirements.txt
 brew install homebrew/cask/wkhtmltopdf
 ```

## 使用指南

1. **Transcribe 视频文件**:
    - 使用 [Descript](https://descript.com/) 将视频文件转换为 Transcript (选择Free Plan即可)。
    - 人工 proofread，或者请求 GPT-4 进行 proofread。
    - 将结果保存到 `files/transcript.txt`。

2. **准备 Word Bank**:
    - 将 Word Bank 内容保存到 `files/wordbank.txt`。

3. **创建标注文件**:
    - 在 `files/annotated_transcript.txt` 文件中标记 Word Bank 中的单词在 Transcript 中出现的位置。例如：

        ```plaintext
        Steve Jobs had a vision. -> Steve Jobs had a [1.vision].
        They whiled away the hours tinkering with electronics in the Jobs house. -> They [32.whiled away] the hours [33.tinkering with] electronics in the Jobs house.
        ```

4. **让 GPT-4 生成解释**:
    - 把 annotated_transcript 放入 `prompts/explain_wordbank.txt`，并通过 ChatGPT 提交给 GPT-4。

5. **保存 GPT-4 输出**:
    - 将 GPT-4 的输出保存到 `files/wordbank_explanation.json`。
    - 人工 proofread 并修改该文件。

6. **生成 Markdown 和 PDF**:
    - 运行 `gen.py` 以生成 Markdown 文件和 PDF 文件。

7. **校对和修订**:
    - 请求 GPT-4 对生成的 Markdown 文件进行 proofread。
    - 根据需要，重复步骤5至7。

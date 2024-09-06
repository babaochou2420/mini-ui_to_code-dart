# Gemini UI to Code Streamlit App

This Streamlit app is designed to convert UI designs into code using the power of AI. It analyzes uploaded images of UI designs and generates corresponding HTML code, making it easier for developers to bring their designs to life.

## 工具資訊

此工具分支於 https://github.com/Doriandarko/gemini-ui-to-code 並進行額外修改，添加生成 Dart 的功能

## 安裝方式

### Windows
1. 安裝環境
    - 架立虛擬環境
        ```
        py -m venv .venv
        ```
    - 進入虛擬環境
        ```
        ./.venv/Scripts/activate
        ```
    - 安裝必要套件
        ```
        pip install -r ./requirements.txt
        ```

2. 修改變數
    - 修改對話金鑰
        搜尋 API_KEY 並更換為自己的 Gemini [FREE] API Key

### MAC
1. 安裝環境
    - 架立虛擬環境
        ```
        python3 -m venv .venv
        ```
    - 進入虛擬環境
        ```
        source .venv/bin/activate
        ```
    - 安裝必要套件
        ```
        pip install -r ./requirements.txt
        ```

2. 修改變數
    - 修改對話金鑰
        搜尋 API_KEY 並更換為自己的 Gemini [FREE] API Key

## 執行方式

```
streamlit run app.py
```
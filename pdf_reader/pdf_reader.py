import pymupdf4llm

md_read = pymupdf4llm.LlamaMarkdownReader()
data = md_read.load_data("data/pdf/eStmt_2025-02-16.pdf")
print(data)
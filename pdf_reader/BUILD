package(default_visibility = ["//visibility:public"])
load("@jsoj_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")



py_library(
  name = "credit-card-statement",
  srcs = ["credit_card_statement.py"],
  deps = [
    "//common:consts",
    "//budget:expense",
    "//budget:expense-type-map",
    requirement("pymupdf4llm"),
    requirement("llama_index"),
    requirement("pymupdf_layout")
  ],
)

py_library(
  name = "bank-statement",
  srcs = ["bank_statement.py"],
  deps = [
    "//common:consts",
    "//budget:expense",
    "//budget:expense-type-map",
    requirement("pymupdf4llm"),
    requirement("llama_index"),
    requirement("pymupdf_layout")
  ],
)
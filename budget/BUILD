package(default_visibility = ["//visibility:public"])
load("@jsoj_deps//:requirements.bzl", "requirement")

py_library(
  name = "budget-io",
  srcs = [
    "budget_io.py",
  ],
  deps = [
    ":expense",
    ":budget-month",
    "//common:input-util",
    requirement("pyyaml"),
  ],
)

py_library(
  name = "budget",
  srcs = [
    "budget.py",
  ],
  deps = [
    ":expense",
    ":budget-month",
    ":budget-io",
    "//common:input-util",
    "//pdf_reader:credit-card-statement",
    requirement("pyyaml"),
  ],
)
py_library(
  name = "expense-type-map",
  srcs = [
    "expense_type_map.py",
  ],
  deps  = [
    ":expense",
  ]
)
py_library(
  name = "expense",
  srcs = [
    "expense.py",
  ],
  deps  = [
    "//common:input-util",
  ]
)

py_library(
  name = "budget-month",
  srcs = [
    "budget_month.py",
  ],
  deps = [
    ":expense",
    "//common:input-util",
    requirement("pyyaml"),
  ],
)
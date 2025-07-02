load("@rules_python//python:defs.bzl", "py_test")
load("@jsoj_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "test-budget",
    size = "small",
    srcs = ["test_budget.py"],
    main = "test_budget.py",
    deps = [
        "//budget:budget",
        "//budget:expense",
        requirement("pytest"),
    ],
)

py_test(
    name = "test-budget-month",
    size = "small",
    srcs = ["test_budget_month.py"],
    main = "test_budget_month.py",
    deps = [
        "//budget:budget-month",
        "//budget:expense",
        requirement("pytest"),
    ],
)

py_test(
    name = "test-budget-io",
    size = "small",
    srcs = ["test_budget_io.py"],
    main = "test_budget_io.py",
    deps = [
        "//budget:budget-io",
        "//budget:budget-month",
        "//budget:expense",
        requirement("pytest"),
    ],
)
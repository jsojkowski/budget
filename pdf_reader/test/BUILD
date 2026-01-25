load("@rules_python//python:defs.bzl", "py_test")
load("@jsoj_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "test-credit-card-statement",
    size = "small",
    srcs = ["test_cc_statement.py"],
    main = "test_cc_statement.py",
    deps = [
        "//pdf_reader:credit-card-statement",
        requirement("pytest"),
    ],
    data = [
        "//data/pdf:credit-card-statements-2025",
    ]
)

py_test(
    name = "test-bank-statement",
    size = "small",
    srcs = ["test_bank_statement.py"],
    main = "test_bank_statement.py",
    deps = [
        "//pdf_reader:bank-statement",
        requirement("pytest"),
    ],
    data = [
        "//data/pdf:bank-statements-2025",
    ]
)
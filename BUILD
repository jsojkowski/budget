package(default_visibility = ["//visibility:public"])
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python//python:defs.bzl", "py_binary")

filegroup(
    name = "requirements",
    data = [
        "requirements.txt",
    ],
)

# See the 'jsoj_deps' pip_parse() in WORKSPACE for further details
# Validate: bazel test <targetname>_update
# Generate: bazel run <targetname>.update
compile_pip_requirements(
    name = "jsoj_deps",
    timeout = "long",  # Increase timeout for underlying py_tests
    extra_args = [
        "--allow-unsafe",
        "--resolver=backtracking",
    ],
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = [
        "long_test",
    ],
)

py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = [
    "//budget:budget",
    "//common:input-util",
  ],
)
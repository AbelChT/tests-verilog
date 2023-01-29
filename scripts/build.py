#!/usr/bin/python3
from typing import List, Tuple, Dict
import os
import pathlib
import argparse
import subprocess
from utils import get_project_root_path
from designs import Design, designs


def configure_source_files(design: Design) -> Tuple[List[str], List[str], str]:
    # List of source files
    source_files = design.source_files

    # List of test files
    test_files = design.test_files

    # Executable name
    executable_name = design.executable_name

    # Obtain absolute paths of the files
    source_files_dir = os.path.join(design.design_path, "src")
    tests_files_dir = os.path.join(design.design_path, "test")
    return ([os.path.join(source_files_dir, src) for src in source_files],
            [os.path.join(tests_files_dir, src) for src in test_files],
            executable_name)


def _run_command(step: str, command: List[str], build_dir: str) -> bool:
    print(f"Executing \"{step}\" step")
    output = subprocess.run(command,
                            capture_output=True,
                            cwd=build_dir)
    if len(output.stdout) > 0:
        print(f"{step} stdout:")
        print(output.stdout.decode("utf-8"))
    if len(output.stderr) > 0:
        print(f"{step} stderr:")
        print(output.stderr.decode("utf-8"))
    print(f"{step} return code: {output.returncode}")

    return output.returncode == 0


def _make_build_dir(design_name: str) -> str:
    build_dir = os.path.join(get_project_root_path(), "out", design_name)
    pathlib.Path(build_dir).mkdir(parents=True, exist_ok=True)
    return build_dir


def configure(design: Design, output_path: str) -> bool:
    # Run configure step
    src, _, _ = configure_source_files(design)
    return _run_command("Configure", ["verilator", "--cc"] + src,
                        output_path)


def build(design: Design, output_path: str) -> bool:
    # Run build step
    src, tst, executable_name = configure_source_files(design)
    return _run_command("Build", ["verilator", "-Wall", "--trace", "--exe", "--build", "-cc"] + src + tst + ["-o", executable_name],
                        output_path)


def execute(design: Design, output_path: str) -> bool:
    # Run execute step
    _, _, executable_name = configure_source_files(design)
    return _run_command("Execute", [os.path.join("obj_dir", executable_name)],
                        output_path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--design', required=True)
    parser.add_argument('-c', '--configure', action='store_true')
    parser.add_argument('-b', '--build', action='store_true')
    parser.add_argument('-r', '--execute', action='store_true')

    args = parser.parse_args()

    if args.design not in designs:
        raise RuntimeError(
            f"Unavailable design selected. Available designs {list(designs.keys())}")

    output_path = _make_build_dir(args.design)

    if args.configure:
        if not configure(designs[args.design], output_path):
            raise RuntimeError("Configure step failed")

    if args.build:
        if not build(designs[args.design], output_path):
            raise RuntimeError("Build step failed")

    if args.execute:
        if not execute(designs[args.design], output_path):
            raise RuntimeError("Execute step failed")

    print(f"Output path: {output_path}")


if __name__ == "__main__":
    main()

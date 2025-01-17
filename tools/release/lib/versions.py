#!/usr/bin/env python3

import fileinput
import re


def update_cmakelists_version(new_version, file_path):
    inside_project = False
    with fileinput.FileInput(file_path, inplace=True) as cmakelists:
        for line in cmakelists:
            if "set(ADA_LIB_VERSION" in line:
                line = re.sub(r"[0-9]+\.[0-9]+\.[0-9]+", new_version, line)

            if "project(" in line:
                inside_project = True
            if inside_project:
                if "VERSION" in line:
                    line = re.sub(r"[0-9]+\.[0-9]+\.[0-9]+", new_version, line)
                    inside_project = False
            print(line, end="")


def update_ada_version_h(new_version, file_path):
    new_version_list = new_version.split(".")
    with fileinput.FileInput(file_path, inplace=True) as ada_version_h:
        inside_enum = False
        for line in ada_version_h:
            if "#define ADA_VERSION" in line:
                line = f'#define ADA_VERSION "{new_version}"\n'

            if "enum {" in line:
                inside_enum = True
            if inside_enum:
                if line.strip().startswith("ADA_VERSION_MAJOR"):
                    line = re.sub(r"\d+", new_version_list[0], line)
                elif line.strip().startswith("ADA_VERSION_MINOR"):
                    line = re.sub(r"\d+", new_version_list[1], line)
                elif line.strip().startswith("ADA_VERSION_REVISION"):
                    line = re.sub(r"\d+", new_version_list[2], line)

            print(line, end="")


def update_doxygen_version(new_version, file_path):
    with fileinput.FileInput(file_path, inplace=True) as doxygen:
        for line in doxygen:
            if line.strip().startswith("PROJECT_NUMBER         ="):
                line = f'PROJECT_NUMBER         = "{new_version}"\n'

            print(line, end="")

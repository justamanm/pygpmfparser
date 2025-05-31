# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/31 19:41
@Author  : luowm
@FileName: build.py
"""
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

ext_modules = [
    Pybind11Extension(
        "pygpmfparser.gpmf_bindings",
        ["pygpmfparser/gpmf_bindings.cpp", "gpmf-parser/GPMF_parser.c", "gpmf-parser/demo/GPMF_mp4reader.c"],
        include_dirs=["gpmf-parser", "gpmf-parser/demo"],
        extra_compile_args={
            "cxx": ["-std=c++11"],
            "c": []
        },
    ),
]

setup(
    name="pygpmfparser",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
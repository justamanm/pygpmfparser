# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/31 19:41
@Author  : luowm
@FileName: build.py
"""
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
import os

# 需要编译的 C 文件
c_sources = [
    "gpmf-parser/GPMF_parser.c",
    "gpmf-parser/demo/GPMF_mp4reader.c"
]

# 生成对应的 .o 文件路径
object_files = [src.replace(".c", ".o") for src in c_sources]

class CustomBuildExt(build_ext):
    def build_objects(self):
        # 编译 C 文件为 .o
        for src, obj in zip(c_sources, object_files):
            self.spawn([
                "cc", "-c", src, "-o", obj, "-I./gpmf-parser", "-I./gpmf-parser/demo"
            ])
    def run(self):
        self.build_objects()
        super().run()

ext_modules = [
    Pybind11Extension(
        "pygpmfparser.gpmf_bindings",
        ["pygpmfparser/gpmf_bindings.cpp"],
        include_dirs=["gpmf-parser", "gpmf-parser/demo"],
        extra_compile_args=["-std=c++11"],
        extra_objects=object_files,
    ),
]

setup(
    name="pygpmfparser",
    ext_modules=ext_modules,
    cmdclass={"build_ext": CustomBuildExt},
)
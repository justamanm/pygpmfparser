# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/31 19:38
@Author  : luowm
@FileName: gpmf_sample.py
"""
class GPMFSample:
    """Represents a GPMF sample with its properties and data."""

    def __init__(self, key_fourcc, type_char, type_string, struct_size, repeat, samples, raw_data):
        self.key = key_fourcc
        self.type_char = type_char
        self.type_string = type_string
        self.struct_size = struct_size
        self.repeat = repeat
        self.samples = samples
        self.raw_data = raw_data

    def __repr__(self):
        return (f"<GPMFSample key='{self.key}' type='{self.type_char}' "
                f"samples={self.samples} repeat={self.repeat} data_len={len(self.raw_data)}>")
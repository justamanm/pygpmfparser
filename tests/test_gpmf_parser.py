# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 2025/5/31 20:12
@Author  : luowm
@FileName: test_gpmf_parser.py
"""
import pytest
from pygpmfparser.gopro_telemetry_extractor import GoProTelemetryExtractor


@pytest.fixture
def sample_video():
    return "gpmf-parser/samples/max-heromode.mp4"


def test_gopro_telemetry_extractor(sample_video):
    extractor = GoProTelemetryExtractor(sample_video)
    assert extractor.validate(), "GPMF data validation failed"

    samples = extractor.get_all_samples()
    assert len(samples) > 0, "No samples found"

    with GoProTelemetryExtractor(sample_video) as extractor:
        for sample in extractor:
            assert sample.key in ["ACCL", "GPS5", "GYRO"], f"Unexpected key: {sample.key}"
            assert isinstance(sample.raw_data, bytes), "Raw data is not bytes"
pygpmfparser
pygpmfparser 是一个用于解析 GoPro 视频中 GPMF（GoPro Metadata Format）数据的 Python 包，基于 GoPro GPMF-parser 库 构建。它通过 pybind11 提供 C++ 绑定，支持以 Pythonic 的方式提取加速度计（ACCL）、GPS（GPS5）、陀螺仪（GYRO）等遥测数据。
功能

从 GoPro MP4 文件中提取 GPMF 遥测数据。
提供 Pythonic 的接口，支持迭代器和上下文管理器。
验证 GPMF 数据的完整性。
兼容 Poetry 进行依赖管理和包分发。

安装
从 PyPI 安装
如果包已发布到 PyPI：
poetry add pygpmfparser

或使用 pip：
pip install pygpmfparser

从源代码安装

克隆仓库并包含子模块：
git clone --recursive https://github.com/yourusername/pygpmfparser.git
cd pygpmfparser

如果 gpmf-parser/ 目录为空，初始化子模块：
git submodule update --init --recursive


安装 Poetry（如果尚未安装）：
pip install poetry


安装依赖并构建包：
poetry install



环境要求

Python：3.8 或更高版本
C++ 编译器：
Linux：gcc 或 clang（Ubuntu 可运行 sudo apt-get install build-essential）
macOS：Xcode 命令行工具（运行 xcode-select --install）
Windows：Microsoft Visual C++ Build Tools（建议安装 Visual Studio Community 2022，包含 C++ 开发工具集）


Git：用于克隆仓库和子模块
依赖：pybind11>=2.6（Poetry 会自动安装）

使用示例
GoProTelemetryExtractor 类提供了一个简单易用的接口，用于从 GoPro MP4 文件中解析 GPMF 数据。
示例代码
from pygpmfparser.gopro_telemetry_extractor import GoProTelemetryExtractor

# 初始化提取器，指定 GoPro MP4 文件路径
filepath = "path/to/your/video.mp4"

# 验证 GPMF 数据
with GoProTelemetryExtractor(filepath) as extractor:
    if extractor.validate():
        print("GPMF 数据有效")

    # 遍历样本
    for sample in extractor:
        if sample.key == "ACCL":
            print(f"加速度计样本: {sample}")
        elif sample.key == "GPS5":
            print(f"GPS 样本: {sample}")

# 获取所有样本列表
extractor = GoProTelemetryExtractor(filepath)
samples = extractor.get_all_samples()
print(f"总样本数: {len(samples)}")

解析原始数据
GPMFSample 类提供原始字节数据（raw_data）。例如，解析加速度计数据为浮点数：
import struct
from pygpmfparser.gopro_telemetry_extractor import GoProTelemetryExtractor

with GoProTelemetryExtractor("video.mp4") as extractor:
    for sample in extractor:
        if sample.key == "ACCL" and sample.type_char == "f":
            floats = struct.unpack(f"<{sample.repeat * sample.samples}f", sample.raw_data)
            print(f"加速度计值: {floats}")

项目结构
pygpmfparser/
├── pygpmfparser/
│   ├── __init__.py
│   ├── gpmf_sample.py
│   ├── gopro_telemetry_extractor.py
│   ├── gpmf_bindings.cpp
├── gpmf-parser/  # GoPro GPMF-parser 子模块
├── tests/
│   ├── __init__.py
│   ├── test_gpmf_parser.py
├── pyproject.toml
├── build.py
├── README.md
├── LICENSE

从源代码构建
确保 gpmf-parser/ 子模块已初始化：
git submodule update --init --recursive

构建包：
poetry build

运行测试：
poetry run pytest

发布到 PyPI
将包发布到 PyPI：
poetry publish --build

先配置 PyPI token：
poetry config pypi-token.pypi <your-token>

故障排除

子模块缺失：如果 gpmf-parser/ 目录为空，运行 git submodule update --init --recursive。
编译错误：
确保安装了 C++ 编译器（见环境要求）。
Windows 用户可能需要从 build.py 中移除 -std=c++11 或使用 MSVC 兼容标志。


测试失败：确保有一个有效的 GoPro MP4 文件（例如 gpmf-parser/samples/max-heromode.mp4）。

许可证
本项目采用 MIT 许可证，详见 LICENSE 文件。
贡献
欢迎贡献代码！请在 GitHub 仓库 提交问题或拉取请求。

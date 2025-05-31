#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../gpmf-parser/GPMF_parser.h"
#include "../gpmf-parser/demo/GPMF_mp4reader.h"
#include <string>
#include <vector>

namespace py = pybind11;

class GPMFStreamCtx {
private:
    GPMF_stream gs_stream;
    void* mp4_handle = nullptr;
    uint32_t current_payload = 0;
    uint32_t total_payloads = 0;
    uint32_t* payload = nullptr;
    uint32_t payload_size = 0;

public:
    GPMFStreamCtx(const std::string& filepath) {
        mp4_handle = OpenMP4Source((char*)filepath.c_str(), MOV_GPMF_TRAK, MOV_GPMF_TRAK);
        if (mp4_handle) {
            total_payloads = GetNumberPayloads(mp4_handle);
        }
    }

    bool next_key() {
        while (current_payload < total_payloads) {
            if (payload) {
                FreePayload(payload);
                payload = nullptr;
            }
            payload = GetPayload(mp4_handle, current_payload);
            payload_size = GetPayloadSize(mp4_handle, current_payload);
            if (payload && GPMF_Init(&gs_stream, payload, payload_size) == GPMF_OK) {
                if (GPMF_OK == GPMF_FindNext(&gs_stream, GPMF_KEY_STREAM, GPMF_RECURSE_LEVELS)) {
                    return true;
                }
                current_payload++;
            } else {
                current_payload++;
            }
        }
        return false;
    }

    std::string get_key_fourcc() {
        uint32_t key = GPMF_Key(&gs_stream);
        char fourcc[5] = {0};
        fourcc[0] = (key >> 24) & 0xFF;
        fourcc[1] = (key >> 16) & 0xFF;
        fourcc[2] = (key >> 8) & 0xFF;
        fourcc[3] = key & 0xFF;
        return std::string(fourcc);
    }

    py::dict get_key_info() {
        py::dict info;
        info["type_char"] = std::string(1, GPMF_Type(&gs_stream));
        info["type_string"] = std::string(GPMF_TypeString(GPMF_Type(&gs_stream)));
        info["struct_size"] = GPMF_StructSize(&gs_stream);
        info["repeat"] = GPMF_Repeat(&gs_stream);
        info["samples"] = GPMF_PayloadSampleCount(&gs_stream);
        return info;
    }

    py::bytes get_raw_data() {
        uint32_t size = GPMF_RawDataSize(&gs_stream);
        void* data = GPMF_RawData(&gs_stream);
        return py::bytes(static_cast<char*>(data), size);
    }

    bool validate() {
        if (!mp4_handle) return false;
        for (uint32_t i = 0; i < total_payloads; i++) {
            uint32_t* temp_payload = GetPayload(mp4_handle, i);
            uint32_t temp_size = GetPayloadSize(mp4_handle, i);
            if (temp_payload) {
                GPMF_stream temp_stream;
                GPMF_Init(&temp_stream, temp_payload, temp_size);
                GPMF_error err = GPMF_Validate(&temp_stream, GPMF_RECURSE_LEVELS);
                FreePayload(temp_payload);
                if (err != GPMF_OK) return false;
            }
        }
        return true;
    }

    void close() {
        if (payload) {
            FreePayload(payload);
            payload = nullptr;
        }
        if (mp4_handle) {
            CloseMP4Source(mp4_handle);
            mp4_handle = nullptr;
        }
    }

    ~GPMFStreamCtx() {
        close();
    }
};

PYBIND11_MODULE(gpmf_bindings, m) {
    py::class_<GPMFStreamCtx>(m, "GPMFStreamCtx")
        .def(py::init<const std::string&>())
        .def("next_key", &GPMFStreamCtx::next_key)
        .def("get_key_fourcc", &GPMFStreamCtx::get_key_fourcc)
        .def("get_key_info", &GPMFStreamCtx::get_key_info)
        .def("get_raw_data", &GPMFStreamCtx::get_raw_data)
        .def("validate", &GPMFStreamCtx::validate)
        .def("close", &GPMFStreamCtx::close)
        .def("__enter__", [](GPMFStreamCtx& self) { return &self; })
        .def("__exit__", [](GPMFStreamCtx& self, py::object, py::object, py::object) { self.close(); });
}
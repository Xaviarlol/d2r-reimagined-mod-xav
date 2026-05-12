#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <strsafe.h>

#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

namespace {

std::wstring now_string()
{
    SYSTEMTIME st{};
    GetLocalTime(&st);

    wchar_t buffer[64]{};
    StringCchPrintfW(
        buffer,
        ARRAYSIZE(buffer),
        L"%04u-%02u-%02u %02u:%02u:%02u",
        st.wYear,
        st.wMonth,
        st.wDay,
        st.wHour,
        st.wMinute,
        st.wSecond);

    return buffer;
}

std::wstring file_version(const wchar_t* path)
{
    DWORD handle = 0;
    const DWORD size = GetFileVersionInfoSizeW(path, &handle);
    if (size == 0) {
        return L"unknown";
    }

    std::vector<unsigned char> data(size);
    if (!GetFileVersionInfoW(path, 0, size, data.data())) {
        return L"unknown";
    }

    VS_FIXEDFILEINFO* info = nullptr;
    UINT info_size = 0;
    if (!VerQueryValueW(data.data(), L"\\", reinterpret_cast<void**>(&info), &info_size) || info == nullptr) {
        return L"unknown";
    }

    wchar_t version[64]{};
    StringCchPrintfW(
        version,
        ARRAYSIZE(version),
        L"%u.%u.%u.%u",
        HIWORD(info->dwFileVersionMS),
        LOWORD(info->dwFileVersionMS),
        HIWORD(info->dwFileVersionLS),
        LOWORD(info->dwFileVersionLS));

    return version;
}

DWORD WINAPI init_thread(LPVOID parameter)
{
    const auto module = reinterpret_cast<HMODULE>(parameter);

    wchar_t dll_path[MAX_PATH]{};
    wchar_t exe_path[MAX_PATH]{};
    GetModuleFileNameW(module, dll_path, ARRAYSIZE(dll_path));
    GetModuleFileNameW(nullptr, exe_path, ARRAYSIZE(exe_path));

    auto log_path = std::filesystem::path(dll_path);
    log_path.replace_filename(L"xav-retail-hook.log");

    std::wofstream log(log_path, std::ios::app);
    if (log) {
        log << L"[" << now_string() << L"] "
            << L"xav-retail-hook loaded"
            << L" pid=" << GetCurrentProcessId()
            << L" exe=\"" << exe_path << L"\""
            << L" exe_version=" << file_version(exe_path)
            << L"\n";
    }

    return 0;
}

} // namespace

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID)
{
    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(module);

        const HANDLE thread = CreateThread(nullptr, 0, init_thread, module, 0, nullptr);
        if (thread != nullptr) {
            CloseHandle(thread);
        }
    }

    return TRUE;
}

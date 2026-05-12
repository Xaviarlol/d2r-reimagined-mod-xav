#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <strsafe.h>

using MMRESULT = UINT;

struct TIMECAPS {
    UINT wPeriodMin;
    UINT wPeriodMax;
};

using LPTIMECAPS = TIMECAPS*;

constexpr MMRESULT kMmsysErrError = 1;

namespace {

HMODULE g_real_winmm = nullptr;

void append_proxy_log(HMODULE module, const wchar_t* message)
{
    wchar_t dll_path[MAX_PATH]{};
    GetModuleFileNameW(module, dll_path, ARRAYSIZE(dll_path));

    wchar_t* last_slash = wcsrchr(dll_path, L'\\');
    if (last_slash == nullptr) {
        return;
    }

    *(last_slash + 1) = L'\0';

    wchar_t log_path[MAX_PATH]{};
    StringCchPrintfW(log_path, ARRAYSIZE(log_path), L"%sxav-retail-proxy.log", dll_path);

    SYSTEMTIME st{};
    GetLocalTime(&st);

    wchar_t exe_path[MAX_PATH]{};
    GetModuleFileNameW(nullptr, exe_path, ARRAYSIZE(exe_path));

    wchar_t line[1024]{};
    StringCchPrintfW(
        line,
        ARRAYSIZE(line),
        L"[%04u-%02u-%02u %02u:%02u:%02u] %s pid=%lu exe=\"%s\"\r\n",
        st.wYear,
        st.wMonth,
        st.wDay,
        st.wHour,
        st.wMinute,
        st.wSecond,
        message,
        GetCurrentProcessId(),
        exe_path);

    const HANDLE file = CreateFileW(
        log_path,
        FILE_APPEND_DATA,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        nullptr,
        OPEN_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        nullptr);

    if (file == INVALID_HANDLE_VALUE) {
        return;
    }

    DWORD bytes_written = 0;
    WriteFile(file, line, lstrlenW(line) * sizeof(wchar_t), &bytes_written, nullptr);
    CloseHandle(file);
}

HMODULE load_real_winmm()
{
    if (g_real_winmm != nullptr) {
        return g_real_winmm;
    }

    wchar_t system_dir[MAX_PATH]{};
    GetSystemDirectoryW(system_dir, ARRAYSIZE(system_dir));

    wchar_t real_path[MAX_PATH]{};
    StringCchPrintfW(real_path, ARRAYSIZE(real_path), L"%s\\winmm.dll", system_dir);

    g_real_winmm = LoadLibraryW(real_path);
    return g_real_winmm;
}

template <typename T>
T resolve_real_proc(const char* name)
{
    const HMODULE module = load_real_winmm();
    if (module == nullptr) {
        return nullptr;
    }

    return reinterpret_cast<T>(GetProcAddress(module, name));
}

DWORD WINAPI init_thread(LPVOID parameter)
{
    append_proxy_log(reinterpret_cast<HMODULE>(parameter), L"xav winmm proxy loaded");
    return 0;
}

} // namespace

extern "C" __declspec(dllexport) MMRESULT WINAPI timeGetDevCaps(LPTIMECAPS ptc, UINT cbtc)
{
    using TimeGetDevCaps = MMRESULT(WINAPI*)(LPTIMECAPS, UINT);
    const auto real_time_get_dev_caps = resolve_real_proc<TimeGetDevCaps>("timeGetDevCaps");
    if (real_time_get_dev_caps == nullptr) {
        return kMmsysErrError;
    }

    return real_time_get_dev_caps(ptc, cbtc);
}

BOOL APIENTRY DllMain(HMODULE module, DWORD reason, LPVOID)
{
    if (reason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(module);
        load_real_winmm();

        const HANDLE thread = CreateThread(nullptr, 0, init_thread, module, 0, nullptr);
        if (thread != nullptr) {
            CloseHandle(thread);
        }
    }

    return TRUE;
}

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <strsafe.h>

namespace {

void append_log_line(HMODULE module)
{
    wchar_t dll_path[MAX_PATH]{};
    GetModuleFileNameW(module, dll_path, ARRAYSIZE(dll_path));

    wchar_t* last_slash = wcsrchr(dll_path, L'\\');
    if (last_slash == nullptr) {
        return;
    }

    *(last_slash + 1) = L'\0';
    wchar_t log_path[MAX_PATH]{};
    StringCchPrintfW(log_path, ARRAYSIZE(log_path), L"%sxav-retail-hook.log", dll_path);

    SYSTEMTIME st{};
    GetLocalTime(&st);

    wchar_t exe_path[MAX_PATH]{};
    GetModuleFileNameW(nullptr, exe_path, ARRAYSIZE(exe_path));

    wchar_t line[1024]{};
    StringCchPrintfW(
        line,
        ARRAYSIZE(line),
        L"[%04u-%02u-%02u %02u:%02u:%02u] xav-retail-hook loaded pid=%lu exe=\"%s\"\r\n",
        st.wYear,
        st.wMonth,
        st.wDay,
        st.wHour,
        st.wMinute,
        st.wSecond,
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

DWORD WINAPI init_thread(LPVOID parameter)
{
    append_log_line(reinterpret_cast<HMODULE>(parameter));
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

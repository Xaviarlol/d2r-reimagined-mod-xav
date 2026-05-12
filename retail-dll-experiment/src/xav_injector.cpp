#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <tlhelp32.h>

#include <cwctype>
#include <filesystem>
#include <iostream>
#include <string>

namespace {

bool parse_pid(const std::wstring& text, DWORD& pid)
{
    if (text.empty()) {
        return false;
    }

    unsigned long value = 0;
    for (const wchar_t ch : text) {
        if (!iswdigit(ch)) {
            return false;
        }
        value = (value * 10) + static_cast<unsigned long>(ch - L'0');
    }

    pid = static_cast<DWORD>(value);
    return pid != 0;
}

DWORD find_process_id(const std::wstring& process_name)
{
    PROCESSENTRY32W entry{};
    entry.dwSize = sizeof(entry);

    const HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }

    DWORD pid = 0;
    if (Process32FirstW(snapshot, &entry)) {
        do {
            if (_wcsicmp(entry.szExeFile, process_name.c_str()) == 0) {
                pid = entry.th32ProcessID;
                break;
            }
        } while (Process32NextW(snapshot, &entry));
    }

    CloseHandle(snapshot);
    return pid;
}

std::wstring last_error_message(DWORD error = GetLastError())
{
    wchar_t* buffer = nullptr;
    const DWORD length = FormatMessageW(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        nullptr,
        error,
        0,
        reinterpret_cast<wchar_t*>(&buffer),
        0,
        nullptr);

    std::wstring message = length == 0 ? L"unknown error" : std::wstring(buffer, length);
    if (buffer != nullptr) {
        LocalFree(buffer);
    }
    return message;
}

} // namespace

int wmain(int argc, wchar_t** argv)
{
    if (argc < 3) {
        std::wcerr << L"Usage: xav-retail-injector.exe <pid|process.exe> <absolute path to dll>\n";
        return 2;
    }

    const std::wstring target = argv[1];
    const std::filesystem::path dll_path = std::filesystem::absolute(argv[2]);

    if (!std::filesystem::exists(dll_path)) {
        std::wcerr << L"DLL not found: " << dll_path.wstring() << L"\n";
        return 3;
    }

    DWORD pid = 0;
    if (!parse_pid(target, pid)) {
        pid = find_process_id(target);
    }

    if (pid == 0) {
        std::wcerr << L"Target process not found: " << target << L"\n";
        return 4;
    }

    const HANDLE process = OpenProcess(
        PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ,
        FALSE,
        pid);

    if (process == nullptr) {
        std::wcerr << L"OpenProcess failed for pid " << pid << L": " << last_error_message();
        return 5;
    }

    const std::wstring dll_string = dll_path.wstring();
    const SIZE_T byte_count = (dll_string.size() + 1) * sizeof(wchar_t);

    void* remote_string = VirtualAllocEx(process, nullptr, byte_count, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (remote_string == nullptr) {
        std::wcerr << L"VirtualAllocEx failed: " << last_error_message();
        CloseHandle(process);
        return 6;
    }

    if (!WriteProcessMemory(process, remote_string, dll_string.c_str(), byte_count, nullptr)) {
        std::wcerr << L"WriteProcessMemory failed: " << last_error_message();
        VirtualFreeEx(process, remote_string, 0, MEM_RELEASE);
        CloseHandle(process);
        return 7;
    }

    const HMODULE kernel32 = GetModuleHandleW(L"kernel32.dll");
    const auto load_library = reinterpret_cast<LPTHREAD_START_ROUTINE>(GetProcAddress(kernel32, "LoadLibraryW"));
    if (load_library == nullptr) {
        std::wcerr << L"Could not locate LoadLibraryW.\n";
        VirtualFreeEx(process, remote_string, 0, MEM_RELEASE);
        CloseHandle(process);
        return 8;
    }

    const HANDLE thread = CreateRemoteThread(process, nullptr, 0, load_library, remote_string, 0, nullptr);
    if (thread == nullptr) {
        std::wcerr << L"CreateRemoteThread failed: " << last_error_message();
        VirtualFreeEx(process, remote_string, 0, MEM_RELEASE);
        CloseHandle(process);
        return 9;
    }

    WaitForSingleObject(thread, 10000);

    DWORD remote_result = 0;
    GetExitCodeThread(thread, &remote_result);

    CloseHandle(thread);
    VirtualFreeEx(process, remote_string, 0, MEM_RELEASE);
    CloseHandle(process);

    if (remote_result == 0) {
        std::wcerr << L"LoadLibraryW returned null in the target process.\n";
        return 10;
    }

    std::wcout << L"Injected " << dll_path.wstring() << L" into pid " << pid << L".\n";
    return 0;
}

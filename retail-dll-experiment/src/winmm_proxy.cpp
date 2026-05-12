#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <strsafe.h>

using MMRESULT = UINT;
using DWORD_PTR = ULONG_PTR;

struct TIMECAPS {
    UINT wPeriodMin;
    UINT wPeriodMax;
};

using LPTIMECAPS = TIMECAPS*;
using LPMMTIME = void*;
using LPTIMECALLBACK = void*;
using HWAVEOUT = HANDLE;
using LPHWAVEOUT = HWAVEOUT*;
using HWAVEIN = HANDLE;
using LPHWAVEIN = HWAVEIN*;
using LPWAVEFORMATEX = void*;
using LPWAVEHDR = void*;
using LPWAVEOUTCAPSA = void*;
using LPWAVEOUTCAPSW = void*;
using LPWAVEINCAPSA = void*;
using LPWAVEINCAPSW = void*;
using LPUINT = UINT*;
using LPDWORD = DWORD*;

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
    const HMODULE module = reinterpret_cast<HMODULE>(parameter);
    append_proxy_log(module, L"xav winmm proxy loaded");

    wchar_t dll_path[MAX_PATH]{};
    GetModuleFileNameW(module, dll_path, ARRAYSIZE(dll_path));

    wchar_t* last_slash = wcsrchr(dll_path, L'\\');
    if (last_slash == nullptr) {
        append_proxy_log(module, L"xav hook path resolution failed");
        return 0;
    }

    *(last_slash + 1) = L'\0';

    wchar_t hook_path[MAX_PATH]{};
    StringCchPrintfW(
        hook_path,
        ARRAYSIZE(hook_path),
        L"%smods\\XavReimaginedExperimental\\tools\\xav-retail-hook.dll",
        dll_path);

    const HMODULE hook = LoadLibraryW(hook_path);
    append_proxy_log(module, hook == nullptr ? L"xav hook load failed" : L"xav hook loaded");
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

extern "C" __declspec(dllexport) MMRESULT WINAPI timeBeginPeriod(UINT period)
{
    using TimeBeginPeriod = MMRESULT(WINAPI*)(UINT);
    const auto real_time_begin_period = resolve_real_proc<TimeBeginPeriod>("timeBeginPeriod");
    if (real_time_begin_period == nullptr) {
        return kMmsysErrError;
    }

    return real_time_begin_period(period);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI timeEndPeriod(UINT period)
{
    using TimeEndPeriod = MMRESULT(WINAPI*)(UINT);
    const auto real_time_end_period = resolve_real_proc<TimeEndPeriod>("timeEndPeriod");
    if (real_time_end_period == nullptr) {
        return kMmsysErrError;
    }

    return real_time_end_period(period);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI timeGetSystemTime(LPMMTIME time, UINT size)
{
    using TimeGetSystemTime = MMRESULT(WINAPI*)(LPMMTIME, UINT);
    const auto real_time_get_system_time = resolve_real_proc<TimeGetSystemTime>("timeGetSystemTime");
    if (real_time_get_system_time == nullptr) {
        return kMmsysErrError;
    }

    return real_time_get_system_time(time, size);
}

extern "C" __declspec(dllexport) DWORD WINAPI timeGetTime()
{
    using TimeGetTime = DWORD(WINAPI*)();
    const auto real_time_get_time = resolve_real_proc<TimeGetTime>("timeGetTime");
    if (real_time_get_time == nullptr) {
        return GetTickCount();
    }

    return real_time_get_time();
}

extern "C" __declspec(dllexport) MMRESULT WINAPI timeKillEvent(UINT timer_id)
{
    using TimeKillEvent = MMRESULT(WINAPI*)(UINT);
    const auto real_time_kill_event = resolve_real_proc<TimeKillEvent>("timeKillEvent");
    if (real_time_kill_event == nullptr) {
        return kMmsysErrError;
    }

    return real_time_kill_event(timer_id);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI timeSetEvent(
    UINT delay,
    UINT resolution,
    LPTIMECALLBACK callback,
    DWORD_PTR user,
    UINT event_flags)
{
    using TimeSetEvent = MMRESULT(WINAPI*)(UINT, UINT, LPTIMECALLBACK, DWORD_PTR, UINT);
    const auto real_time_set_event = resolve_real_proc<TimeSetEvent>("timeSetEvent");
    if (real_time_set_event == nullptr) {
        return 0;
    }

    return real_time_set_event(delay, resolution, callback, user, event_flags);
}

extern "C" __declspec(dllexport) UINT WINAPI waveOutGetNumDevs()
{
    using Fn = UINT(WINAPI*)();
    const auto fn = resolve_real_proc<Fn>("waveOutGetNumDevs");
    return fn == nullptr ? 0 : fn();
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetDevCapsA(UINT_PTR device_id, LPWAVEOUTCAPSA caps, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(UINT_PTR, LPWAVEOUTCAPSA, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetDevCapsA");
    return fn == nullptr ? kMmsysErrError : fn(device_id, caps, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetDevCapsW(UINT_PTR device_id, LPWAVEOUTCAPSW caps, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(UINT_PTR, LPWAVEOUTCAPSW, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetDevCapsW");
    return fn == nullptr ? kMmsysErrError : fn(device_id, caps, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetErrorTextA(MMRESULT error, LPSTR text, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(MMRESULT, LPSTR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetErrorTextA");
    return fn == nullptr ? kMmsysErrError : fn(error, text, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetErrorTextW(MMRESULT error, LPWSTR text, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(MMRESULT, LPWSTR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetErrorTextW");
    return fn == nullptr ? kMmsysErrError : fn(error, text, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutOpen(
    LPHWAVEOUT wave_out,
    UINT_PTR device_id,
    LPWAVEFORMATEX format,
    DWORD_PTR callback,
    DWORD_PTR instance,
    DWORD flags)
{
    using Fn = MMRESULT(WINAPI*)(LPHWAVEOUT, UINT_PTR, LPWAVEFORMATEX, DWORD_PTR, DWORD_PTR, DWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutOpen");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, device_id, format, callback, instance, flags);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutClose(HWAVEOUT wave_out)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT);
    const auto fn = resolve_real_proc<Fn>("waveOutClose");
    return fn == nullptr ? kMmsysErrError : fn(wave_out);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutPrepareHeader(HWAVEOUT wave_out, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutPrepareHeader");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutUnprepareHeader(HWAVEOUT wave_out, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutUnprepareHeader");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutWrite(HWAVEOUT wave_out, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutWrite");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutPause(HWAVEOUT wave_out)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT);
    const auto fn = resolve_real_proc<Fn>("waveOutPause");
    return fn == nullptr ? kMmsysErrError : fn(wave_out);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutRestart(HWAVEOUT wave_out)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT);
    const auto fn = resolve_real_proc<Fn>("waveOutRestart");
    return fn == nullptr ? kMmsysErrError : fn(wave_out);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutReset(HWAVEOUT wave_out)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT);
    const auto fn = resolve_real_proc<Fn>("waveOutReset");
    return fn == nullptr ? kMmsysErrError : fn(wave_out);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutBreakLoop(HWAVEOUT wave_out)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT);
    const auto fn = resolve_real_proc<Fn>("waveOutBreakLoop");
    return fn == nullptr ? kMmsysErrError : fn(wave_out);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetPosition(HWAVEOUT wave_out, LPMMTIME time, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPMMTIME, UINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetPosition");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, time, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetPitch(HWAVEOUT wave_out, LPDWORD pitch)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPDWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutGetPitch");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, pitch);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutSetPitch(HWAVEOUT wave_out, DWORD pitch)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, DWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutSetPitch");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, pitch);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetPlaybackRate(HWAVEOUT wave_out, LPDWORD rate)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPDWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutGetPlaybackRate");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, rate);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutSetPlaybackRate(HWAVEOUT wave_out, DWORD rate)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, DWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutSetPlaybackRate");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, rate);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetVolume(HWAVEOUT wave_out, LPDWORD volume)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPDWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutGetVolume");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, volume);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutSetVolume(HWAVEOUT wave_out, DWORD volume)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, DWORD);
    const auto fn = resolve_real_proc<Fn>("waveOutSetVolume");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, volume);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutGetID(HWAVEOUT wave_out, LPUINT device_id)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, LPUINT);
    const auto fn = resolve_real_proc<Fn>("waveOutGetID");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, device_id);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveOutMessage(
    HWAVEOUT wave_out,
    UINT message,
    DWORD_PTR param1,
    DWORD_PTR param2)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEOUT, UINT, DWORD_PTR, DWORD_PTR);
    const auto fn = resolve_real_proc<Fn>("waveOutMessage");
    return fn == nullptr ? kMmsysErrError : fn(wave_out, message, param1, param2);
}

extern "C" __declspec(dllexport) UINT WINAPI waveInGetNumDevs()
{
    using Fn = UINT(WINAPI*)();
    const auto fn = resolve_real_proc<Fn>("waveInGetNumDevs");
    return fn == nullptr ? 0 : fn();
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetDevCapsA(UINT_PTR device_id, LPWAVEINCAPSA caps, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(UINT_PTR, LPWAVEINCAPSA, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetDevCapsA");
    return fn == nullptr ? kMmsysErrError : fn(device_id, caps, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetDevCapsW(UINT_PTR device_id, LPWAVEINCAPSW caps, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(UINT_PTR, LPWAVEINCAPSW, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetDevCapsW");
    return fn == nullptr ? kMmsysErrError : fn(device_id, caps, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetErrorTextA(MMRESULT error, LPSTR text, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(MMRESULT, LPSTR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetErrorTextA");
    return fn == nullptr ? kMmsysErrError : fn(error, text, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetErrorTextW(MMRESULT error, LPWSTR text, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(MMRESULT, LPWSTR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetErrorTextW");
    return fn == nullptr ? kMmsysErrError : fn(error, text, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInOpen(
    LPHWAVEIN wave_in,
    UINT_PTR device_id,
    LPWAVEFORMATEX format,
    DWORD_PTR callback,
    DWORD_PTR instance,
    DWORD flags)
{
    using Fn = MMRESULT(WINAPI*)(LPHWAVEIN, UINT_PTR, LPWAVEFORMATEX, DWORD_PTR, DWORD_PTR, DWORD);
    const auto fn = resolve_real_proc<Fn>("waveInOpen");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, device_id, format, callback, instance, flags);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInClose(HWAVEIN wave_in)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN);
    const auto fn = resolve_real_proc<Fn>("waveInClose");
    return fn == nullptr ? kMmsysErrError : fn(wave_in);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInPrepareHeader(HWAVEIN wave_in, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInPrepareHeader");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInUnprepareHeader(HWAVEIN wave_in, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInUnprepareHeader");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInAddBuffer(HWAVEIN wave_in, LPWAVEHDR header, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, LPWAVEHDR, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInAddBuffer");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, header, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInStart(HWAVEIN wave_in)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN);
    const auto fn = resolve_real_proc<Fn>("waveInStart");
    return fn == nullptr ? kMmsysErrError : fn(wave_in);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInStop(HWAVEIN wave_in)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN);
    const auto fn = resolve_real_proc<Fn>("waveInStop");
    return fn == nullptr ? kMmsysErrError : fn(wave_in);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInReset(HWAVEIN wave_in)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN);
    const auto fn = resolve_real_proc<Fn>("waveInReset");
    return fn == nullptr ? kMmsysErrError : fn(wave_in);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetPosition(HWAVEIN wave_in, LPMMTIME time, UINT size)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, LPMMTIME, UINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetPosition");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, time, size);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInGetID(HWAVEIN wave_in, LPUINT device_id)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, LPUINT);
    const auto fn = resolve_real_proc<Fn>("waveInGetID");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, device_id);
}

extern "C" __declspec(dllexport) MMRESULT WINAPI waveInMessage(
    HWAVEIN wave_in,
    UINT message,
    DWORD_PTR param1,
    DWORD_PTR param2)
{
    using Fn = MMRESULT(WINAPI*)(HWAVEIN, UINT, DWORD_PTR, DWORD_PTR);
    const auto fn = resolve_real_proc<Fn>("waveInMessage");
    return fn == nullptr ? kMmsysErrError : fn(wave_in, message, param1, param2);
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

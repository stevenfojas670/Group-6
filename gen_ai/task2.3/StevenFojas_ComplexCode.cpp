// HookFunctions.cpp
// This file implements API hooking for Winsock functions `recv` and `send`.
// It intercepts these functions to log data being sent and received over network sockets.

// Required headers
#include "HookFunctions.h"
#include <windows.h>
#include <fstream>
#include <string>

// Global pointers to hold the original addresses of recv and send
void *RecvAddr;
void *SendAddr;

/**
 * Real_Recv - Trampoline function for `recv`
 * This is a "naked" function (no compiler-generated prologue/epilogue).
 * It manually jumps into the original `recv` after our hook's 5-byte overwrite.
 */
__declspec(naked) int __stdcall Real_Recv(
    _In_ SOCKET s,
    _Out_ char *buf,
    _In_ int len,
    _In_ int flags)
{
    __asm {
        mov edi, edi // Standard two-byte NOP for alignment (common in Windows functions)
        push ebp
        mov ebp, esp

        mov eax, [RecvAddr] // Load original address of recv
        add eax, 5 // Skip over the overwritten 5 bytes (JMP we placed)
        jmp eax // Jump directly into the original recv (after the hook jump)
    }
}

/**
 * Real_Send - Trampoline function for `send`
 * Same concept as Real_Recv, but for the `send` function.
 */
__declspec(naked) int __stdcall Real_Send(
    _In_ SOCKET s,
    _In_ const char *buf,
    _In_ int len,
    _In_ int flags)
{
    __asm {
        mov edi, edi
        push ebp
        mov ebp, esp

        mov eax, [SendAddr] // Load original address of send
        add eax, 5 // Skip the overwritten 5 bytes
        jmp eax // Jump into the original send (past the hook)
    }
}

/**
 * Get_Recv - Locate the real `recv` function from WS2_32.dll
 * This must be called before hooking to obtain the real address.
 */
void *Get_Recv()
{
    RecvAddr = (void *)GetProcAddress(GetModuleHandleA("WS2_32.dll"), "recv");
    return RecvAddr;
}

/**
 * Get_Send - Locate the real `send` function from WS2_32.dll
 * This must be called before hooking to obtain the real address.
 */
void *Get_Send()
{
    SendAddr = (void *)GetProcAddress(GetModuleHandleA("WS2_32.dll"), "send");
    return SendAddr;
}

/**
 * PutJMP - Overwrites the beginning of a function with a JMP instruction to a hook.
 * @param WriteTo      Address of the target function (recv or send).
 * @param HookFunction Address of the function that should handle the call (hook function).
 */
void PutJMP(void *WriteTo, void *HookFunction)
{
    DWORD oldProtection, backupProtection;

    // Temporarily make the memory page writable
    VirtualProtect(WriteTo, 5, PAGE_EXECUTE_READWRITE, &oldProtection);

    // Write the JMP opcode (0xE9) at the start of the target function
    memset(WriteTo, 0xE9, 1);

    // Calculate relative offset to the hook function
    DWORD RelOffset = (DWORD)HookFunction - (DWORD)WriteTo - 5;

    // Write the offset after the JMP opcode
    memcpy((void *)((DWORD)WriteTo + 1), &RelOffset, 4);

    // Restore the original protection level
    VirtualProtect(WriteTo, 5, oldProtection, &backupProtection);
}

/**
 * Hook_Recv - Our custom replacement for `recv`
 * This logs data received from the socket into a file.
 * After logging, it calls the real `recv`.
 */
int __stdcall Hook_Recv(SOCKET s, char *buf, int len, int flags)
{
    static int N = 0; // Counter for log file numbering

    // Call the real recv (trampoline call)
    auto ret = Real_Recv(s, buf, len, flags);

    // Create a log file with a unique name (e.g., Recv\Log-0.txt)
    std::string FileName = "Recv\\Log-" + std::to_string(N++) + ".txt";
    std::ofstream File(FileName);

    // Write the received data into the file
    File.write(buf, len);

    // Return the actual result of recv
    return ret;
}

/**
 * Hook_Send - Our custom replacement for `send`
 * This logs data being sent to the socket into a file.
 * After logging, it calls the real `send`.
 */
int __stdcall Hook_Send(SOCKET s, const char *buf, int len, int flags)
{
    static int N = 0; // Counter for log file numbering

    // Call the real send (trampoline call)
    auto ret = Real_Send(s, buf, len, flags);

    // Create a log file with a unique name (e.g., Send\Log-0.txt)
    std::string FileName = "Send\\Log-" + std::to_string(N++) + ".txt";
    std::ofstream File(FileName);

    // Write the sent data into the file
    File.write(buf, len);

    // Return the actual result of send
    return ret;
}

# REVERSE — рабочая шпаргалка

Кубок CTF России, отбор 2026. От ELF/PE до Android, .NET, Rust, Go, Bun и кастомных VM. Цель — за 20 минут определить слой защиты и выбрать инструмент, а не перебирать всё подряд.

## Когда открывать

- Дали бинарь, APK, `.exe`, `.dll`, `.NET`, firmware, `.wasm`, `.pyc`, JS-сборку или «демо» с проверкой ключа.
- Нужно понять алгоритм проверки флага, восстановить ключ, снять антидебаг, распаковать VM.
- В описании: «crackme», «keygen», «лицензия», «пароль», «прошивка», «приложение», «сервер мониторинга».
- `strings` не даёт флага, но бинарь явно что-то проверяет; нужен keygen/эмуляция, а не «взлом».
- `checksec`/`DIE` показывает packed, `.vmp`, `.themida`, высокую энтропию; есть VM, nanomites, SMC, TLS-callback, PEB.
- Задача содержит Android-манифест, `classes.dex`, `lib/arm64-v8a/*.so`.
- Rust/Go: `_ZN...`, `runtime.main`, `rustc`; .NET: `mscoree.dll`, `BSJB`, `#Strings`, `dnSpy`.

## Карта раздела

| § | Тема | Инструменты |
|---|---|---|
| 0 | Первичный триаж | `file`, DIE, `strings`, `rabin2`, `binwalk` |
| 1 | Статический анализ | IDA, Ghidra, Binary Ninja, FLIRT, rizin |
| 2 | Динамический анализ | gdb, x64dbg, Frida, strace, Unicorn |
| 3 | Анти-анализ и обфускация | TLS, PEB, nanomites, SMC, VM, MBA |
| 4 | Рантаймы | Rust, Go, .NET, Android, Bun/JS, Python, WASM |
| 5 | Символическое исполнение | angr, Z3, Triton, Qiling |
| 6 | Крипто и математика в реверсе | Sage, Z3, MITM, GCD, ECC |
| 7 | Чек-лист 20 минут | порядок действий |
| 8 | Разбор 2022–2025 | задача → техника → вывод |
| 9 | Типовые ошибки | перед сдачей флага |

## §0. Первичный триаж

**Признак.** Файл неизвестного происхождения. **Что делать.** Определить формат, архитектуру, упаковку и рантайм до открытия дизассемблера.

```bash
file ./sample
diec ./sample                 # Detect It Easy CLI
strings -a -n 6 ./sample | head -120
strings -el ./sample | head -40   # UTF-16, .NET/Windows
rabin2 -I ./sample            # arch, bits, endian, canary, pic
rabin2 -zzz ./sample | head -80
readelf -hW ./sample; readelf -SW ./sample; readelf -lW ./sample
objdump -d -Mintel ./sample | head -80
nm -C ./sample | head -40
ldd ./sample; binwalk ./sample
capa ./sample                 # ATT&CK/capability, если установлен
floss ./sample                # строки, включая обфусцированные
```

Таблица быстрого определения рантайма:

| Признак | Рантайм | Что смотреть |
|---|---|---|
| `rustc`, `/rustc/`, `_ZN...17h...E`, `core::panicking` | Rust | `rustfilt`, мономорфизация, `panic` |
| `Go build ID`, `gopclntab`, `runtime.main`, `main.main` | Go | `GoReSym`, `go tool nm`, `redress` |
| `mscoree.dll`, `BSJB`, `#Strings`, `#US` | .NET | `dnSpy`, `ILSpy`, `de4dot` |
| `classes.dex`, `AndroidManifest.xml`, `lib/arm64-v8a` | Android | `jadx`, `apktool`, Frida |
| `@bun`, `compiled://`, `Bun.file` | Bun/JS | `rabin2 -zzz`, `dd`, AST-деобфускация |
| `PyInstaller`, `MEI`, `pyi-` | Python | `pyinstxtractor`, `pycdc` |
| `UPX!` | UPX | `upx -d` |
| `.vmp`, `VMProtect`, `Themida` | VM/packer | dump из памяти, Scylla, трассировка |
| высокая энтропия, мало импортов | packed/encrypted | распаковка, `PE-sieve`, `x64dbg` |

```bash
upx -d ./sample -o ./unpacked
binwalk -e ./sample
7z x ./sample -o./extracted
```

**Грабли.** `strings` не видит UTF-16 и сжатые строки; используй `strings -el` и `floss`. `file` может ошибаться на firmware/архивах — проверяй `binwalk` и заголовки. Высокая энтропия бывает у сжатых ресурсов, а не только упаковщика.

## §1. Статический анализ

**Признак.** Нужен алгоритм, а не поведение; бинарь небольшой или есть символы. **Что делать.** Сначала сигнатуры и типы, потом декомпилятор.

### IDA

```text
F5 декомпиляция; Shift+F12 строки; Ctrl+S сегменты; Alt+B поиск
X xrefs; G goto; N rename; Y type; Ctrl+Alt+K stack variables
```

- `Options → Compiler → Visual C++/GCC` — влияет на декомпиляцию; `Parse C header` — структуры.
- `File → Load file → FLIRT signature file` — сигнатуры libc/STL; `Lumina`/`IDAPython` — сигнатуры и автоматизация.

```python
import idautils, idc
for x in idautils.XrefsTo(0x401000): print(hex(x.frm), idc.get_func_name(x.frm))
```

### FLIRT: статически слинкованные библиотеки

```bash
plb.exe libc.a libc.pat        # статическая библиотека -> .pat
# pcf.exe file.obj file.pat    # одиночный объектный файл -> .pat
sigmake.exe libc.pat libc.sig
# IDA: File -> Load file -> FLIRT signature file -> libc.sig
```

**Грабли.** FLIRT по сигнатурам не восстановит инлайн-функции и LTO; для C++ используй `c++filt`/`rustfilt`, для Go — `GoReSym`.

### Ghidra

```bash
analyzeHeadless C:\ghidra_proj proj -import sample -postScript dump.py -scriptPath .
```

- `Data Type Manager` — структуры; `Function ID` — сигнатуры; `Version Tracking`/`BinDiff`/`Diaphora` — diff.
- Скрипты: `flatProgramAPI`, `currentProgram`, `getReferencesTo`.

### Binary Ninja

```python
import binaryninja as bn
bv = bn.open_view("sample")
for f in bv.functions:
    print(hex(f.start), f.name, f.symbol.type)
```

- `SigKit`/`FLIRT` — сигнатуры; HLIL часто лучше на Rust/Go; `Patch`, `Callgraph`, `Xrefs` — в UI.

### rizin/radare2

```bash
rizin -A -q -c 'iI; afl; pdf @ main; iz' ./sample
```

**Грабли.** Декомпилятор врёт в типах и границах массивов; проверяй `movzx/movsx`, размеры структур и выравнивание. Не называй переменные по первому впечатлению — вернись после динамики.

## §2. Динамический анализ

**Признак.** Алгоритм зависит от времени, окружения, антидебага или сам расшифровывается. **Что делать.** Поставить брейкпоинт на проверку и снять состояние.

### gdb

```bash
gdb -q ./sample
set pagination off; set disassembly-flavor intel
b *0x401234; run; info registers; x/20i $pc; x/40gx $rsp; x/s $rdi
```

```text
catch syscall read; catch syscall write
rwatch *(long*)0x404000; awatch *(long*)0x404000
record; reverse-continue; set follow-fork-mode child
```

### x64dbg

```text
bp <addr> / bp <module>.func; run; F7/F8 step; dump <addr>; follow in dump
hr <addr> hardware bp; mr <addr>; TraceInto/TraceOver
```

- `ScyllaHide`/`TitanHide` — скрыть отладчик (PEB, heap flags, NtGlobalFlag); `Scylla` — dump и импорты.
- `API Monitor`, `Process Monitor`, `Wireshark` — поведение и сеть.

### strace/ltrace/rr

```bash
strace -f -s 200 -e trace=openat,read,write,execve ./sample
ltrace -f -S ./sample
rr record ./sample && rr replay
```

**Грабли.** `strace` меняет тайминг и может сорвать антидебаг; `rr` не работает с некоторыми GPU/ioctl. Для Windows `x64dbg` + `ScyllaHide` часто стабильнее, чем патчинг PEB вручную.

### Frida

```bash
frida -U -f com.example.app -l hook.js --no-pause
frida-trace -U -f com.example.app -i "open*" -i "strcmp"
```

```javascript
Interceptor.attach(Module.findExportByName(null, "strcmp"), {
  onEnter(a) { console.log(a[0].readCString(), a[1].readCString()); },
  onLeave(r) { console.log("ret", r.toInt32()); }
});
// подмена возврата: Interceptor.replace(ptr("0x401234"), new NativeCallback(() => 1, "int", []));
```

### LD_PRELOAD / hook

```c
ssize_t read(int fd, void *buf, size_t n) {
    static ssize_t (*real)(int, void *, size_t);
    if (!real) real = dlsym(RTLD_NEXT, "read");
    ssize_t r = real(fd, buf, n); /* логируй/подменяй buf */
    return r;
}
```

```bash
gcc -shared -fPIC -ldl hook.c -o hook.so && LD_PRELOAD=./hook.so ./sample
```

**Грабли.** `LD_PRELOAD` не сработает на статически слинкованный бинарь и на setuid. Для Android нужен `frida-server` под архитектуру и root/эмулятор.

### QEMU/Unicorn для других архитектур

```bash
qemu-arm -L ./lib ./sample
qemu-mips -L ./lib ./sample
qemu-ppc -L ./lib ./sample
```

```python
from unicorn import *
uc = Uc(UC_ARCH_ARM, UC_MODE_ARM); uc.mem_map(0x1000, 0x10000)
uc.mem_write(0x1000, code); uc.reg_write(UC_ARM_REG_SP, 0x8000)
uc.hook_add(UC_HOOK_CODE, lambda uc, a, s, _: print(hex(a)))
uc.emu_start(0x1000, 0x1000 + len(code))
```

**Грабли.** Unicorn не эмулирует syscall/прерывания; для них нужен Qiling или ручные хуки. Проверяй endianness (MIPS BE/LE) и режим ARM/Thumb.

## §3. Анти-анализ и обфускация

### Windows anti-debug

**Признак.** `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`, TLS-callback, проверка `PEB`. **Что делать.** Найти проверку, снять её или скрыть отладчик.

```text
PEB x64: gs:[0x60]
+0x002 BeingDebugged
+0x010 ImageBaseAddress
+0x018 Ldr
+0x0BC NtGlobalFlag   (x86: fs:[0x30], +0x068)
Heap flags: Flags/ForceFlags
```

```c
CheckRemoteDebuggerPresent(GetCurrentProcess(), &b);
NtQueryInformationProcess(h, 7,    &port,   sizeof(port),   NULL); // DebugPort
NtQueryInformationProcess(h, 0x1e, &handle, sizeof(handle), NULL); // DebugObject
NtQueryInformationProcess(h, 0x1f, &flags,  sizeof(flags),  NULL); // DebugFlags
NtSetInformationThread(GetCurrentThread(), 0x11, NULL, 0);         // HideFromDebugger
```

- `ScyllaHide`: `BeingDebugged`, `NtGlobalFlag`, `HeapFlags`, `DebugPort`, `DebugObject`, `TLS`; патч `PEB->BeingDebugged=0`, `NtGlobalFlag=0`, heap `Flags=2`, `ForceFlags=0`.
- Hardware bp вместо `int3` (антидебаг ищет `0xCC`); TLS-callback — `bp` на `AddressOfCallBacks` до `main`.

```python
import pefile
pe = pefile.PE("sample.exe"); tls = pe.DIRECTORY_ENTRY_TLS.struct
cb = tls.AddressOfCallBacks - pe.OPTIONAL_HEADER.ImageBase
while (fn := pe.get_qword_at_rva(cb)): print(hex(fn)); cb += 8
```

**Грабли.** В x64 `gs:[0x60]`, в x86 `fs:[0x30]`; `NtGlobalFlag` имеет разный offset. `bp main` пропускает TLS. Если проверка идёт по хешу кода, патч в памяти не поможет — патчь саму проверку.

### Linux anti-debug

```text
ptrace(PTRACE_TRACEME, 0, 0, 0);       // вернёт -1 под отладчиком
cat /proc/self/status | grep TracerPid
prctl(PR_SET_DUMPABLE, 0); personality(ADDR_NO_RANDOMIZE);
```

Обход: `LD_PRELOAD` с фиктивным `ptrace`, патч `TracerPid`, запуск без отладчика и дамп после инициализации, `gdb` `set follow-fork-mode`.

### Self-modifying code

**Признак.** `mprotect`/`VirtualProtect`, запись в `.text`, код меняется после запуска. **Что делать.** Брейк на смену прав, дампнуть расшифрованную страницу.

```text
gdb -q ./sample -ex 'catch syscall mprotect' -ex run
dump memory dumped.bin 0x401000 0x402000
x64dbg: bp VirtualProtect; run; dump <base>; Scylla dump
```

**Грабли.** Дамп после `mprotect` может быть ещё не расшифрован; ставь брейк на запись (`awatch`) или на выход из decrypt-функции. Не забудь про relocations.

### Nanomites

**Признак.** Родительский процесс `fork`/`ptrace`, ребёнок падает по `SIGSEGV`/`INT3`, арифметика выполняется отладчиком. **Что делать.** Перехватить `ptrace`/`waitpid`, заменить trap на реальную операцию или эмулировать.

```text
strace -f -e trace=ptrace,wait4,clone ./sample
gdb -p <child>   # или attach к родителю и b *ptrace
// LD_PRELOAD: long ptrace(int req, ...) { /* логируй PTRACE_POKETEXT/GETREGS */ }
```

**Грабли.** Trap может быть `int3`, `ud2`, `SIGILL`; обработчик восстанавливает байт. Если эмулируешь — нужно точно повторить семантику регистров и флагов. В `nanomachines` арифметика ECC шла через SIGSEGV-обработчик.

### VM reverse

**Признак.** Огромный `switch`, таблица handler'ов, `bytecode` в `.rodata`, счётчик `pc`. **Что делать.** Найти dispatch, восстановить набор opcode/operand, написать дизассемблер.

```text
1. Найди цикл fetch -> decode -> dispatch -> pc++; таблица переходов — рядом со switch
2. Для каждого handler: что читает из bytecode, что пишет в регистры/память
3. Составь enum opcode и lift в Python/C; проверь на трассе pc/регистры
```

**Грабли.** Operand бывает переменной длины; handler может менять `pc` нелинейно. Не путай VM-регистры с регистрами хоста. Для больших VM используй `angr`/Unicorn после лифта.

### Обфускация

- MBA (mixed boolean-arithmetic): упрощай `z3`/`simplify` или `D810`/`GOOMBA`.
- Control-flow flattening: найди state-переменную и `switch`; `D810`, `GOOMBA`, декомпилятор.
- Opaque predicates: проверь через `z3`; патчь переход.
- Строки: массив + индекс, XOR/RC4; break после decrypt и дампни память.
- Packer: `UPX`, `VMProtect`, `Themida`; снимай дамп после распаковки, восстанавливай импорты `Scylla`.

**Грабли.** Онлайн-деобфускаторы не понимают кастомные VM и `sus`; лучше написать свой AST-проход. Не трать часы на восстановление имён — сначала найди проверку.

## §4. Рантаймы

### Rust

**Признак.** `_ZN...`, `rustc`, `core::panicking`, `alloc::vec`, строки `thread 'main' panicked`. **Что делать.** Демутировать символы, найти `main`, учесть layout `Vec`/`String`.

```bash
strings -a ./bin | grep -E 'rustc|/rustc/|cargo'; readelf -S ./bin | grep -i rust
nm -C ./bin | grep -E 'main|check|flag'
rustfilt -i < symbols.txt
```

- IDA `rust-ida`/`rust-demangler`, Ghidra `Rust` analyzer; `panic!`/`unwrap` дают имена и строки.
- `Vec<T>`/`String`: ptr, cap, len; `Option<T>` — ниша; `RUST_BACKTRACE=full`, `rust-gdb`.
- Мономорфизация раздувает код; ищи `main` и `check`.

**Грабли.** `#[inline]` и LTO убивают границы функций; не доверяй декомпилятору в `match`. В pwn-задачах Rust может быть вектором атаки через `unsafe`/lifetime (см. pwn.md, cve-rs).

### Go

**Признак.** `Go build ID`, `runtime.main`, `main.main`, `gopclntab`, много статических функций. **Что делать.** Восстановить имена и сигнатуры, найти `main.main`.

```bash
go version -m ./bin; redress -src ./bin
go tool nm ./bin | grep -E ' main\.|runtime\.main'
GoReSym -t ./bin > syms.json
```

- Ghidra/IDA: GoReSym, golang loader; `gopclntab` даёт имена и границы; ABI — стек до 1.17, регистры 1.17+.
- `panic`/`defer`/`goroutine` усложняют CFG; ищи `main.main`.

**Грабли.** `go tool nm` не работает на stripped; используй `GoReSym`. Не путай `runtime.main` и `main.main`. В Go строки — `{ptr,len}`, а не C-string.

### .NET

**Признак.** `mscoree.dll`, `BSJB`, `#Strings`, `#US`, `dnSpy` открывает IL. **Что делать.** Открыть в dnSpy/ILSpy, снять обфускацию, при необходимости отладить.

```bash
strings -el ./sample.exe | head -50
monodis ./sample.exe | head -80; ildasm /out=out.il sample.exe
```

- `dnSpy`: Open/Debug, bp по методам, `Edit Method (C#)`/`Edit IL`; `ILSpy` + `de4dot`.
- `ConfuserEx`/`SmartAssembly`: `de4dot`, `UnConfuserEx`, `NoFuserEx`; проверь strings/reflection.
- Single-file bundle: `dotnet` extractor, `7z`/`binwalk`.

**Грабли.** Обфускатор может шифровать строки и прятать reflection; `de4dot` не всегда справляется. После правки IL сохраняй модуль и проверяй подпись/strong name.

### Android

**Признак.** APK, `classes.dex`, `AndroidManifest.xml`, `lib/arm64-v8a/*.so`. **Что делать.** Java/Kotlin — jadx; нативка — IDA/Ghidra; проверки — Frida.

```bash
jadx -d out app.apk; apktool d -f app.apk -o apktool_out
unzip -o app.apk -d apk_raw
adb shell pm path com.example.app
adb pull /data/app/.../base.apk
frida -U -f com.example.app -l hook.js --no-pause
objection -g com.example.app explore
```

```javascript
Java.perform(() => {
  const C = Java.use("com.example.app.Check");
  C.verify.implementation = function (s) { console.log("verify", s); return true; };
});
```

- Manifest: permissions, exported activities, `android:debuggable`; Kotlin/Hilt — логика в `ViewModel`/DI, ищи `R.raw`.
- Сертификат: `GET_SIGNING_CERTIFICATES`/`getApkContentsSigners`, Frida-хук; нативка — `Java_*` JNI, `frida-trace`.
- Repack: `apktool b`, `apksigner`/`uber-apk-signer`, `adb install -r`.

**Грабли.** Эмулятор/x86 может не иметь нужной `.so`; ставь arm64 image или Frida gadget. Проверка подписи может быть на сервере — патч клиента не поможет. `jadx` не декомпилирует нативный код.

### Bun/JS/Python/WASM

```bash
# Bun standalone: ищем встроенный JS
rabin2 -zzz ./monitoring | head
dd if=./monitoring of=extracted.js bs=1 skip=<offset>
```

- Bun: `@bun`, `compiled://`, `Bun.file`, `eval`; исходники в конце бинаря.
- Обфускация: `sus`, строковый массив, `[attr]`; `webcrack`, `deobfuscator`, Babel AST.
- Deno: `--allow-read=./entry`, несколько путей через запятую — bypass.
- Python: `pyinstxtractor`, `pycdc`; WASM: `wasm2wat`, `wasm-decompile`, `wasm-tools`.

**Грабли.** `strings` может не показать JS из-за длины строки; `rabin2 -zzz`/`binwalk` надёжнее. Для Bun нужен offset из `rabin2`, а не начало файла.

### Multi-arch / Unicorn

**Признак.** В бинаре несколько blob'ов, `unicorn_engine`, `qemu`, MIPS/PPC/SPARC. **Что делать.** Определить архитектуру каждого blob, эмулировать и снять ограничения.

```python
from unicorn import *
uc = Uc(UC_ARCH_MIPS, UC_MODE_MIPS32 + UC_MODE_BIG_ENDIAN)
uc.mem_map(0x1000, 0x10000); uc.mem_write(0x1000, blob); uc.reg_write(UC_MIPS_REG_SP, 0x8000)
uc.emu_start(0x1000, 0x1000 + len(blob))
```

**Грабли.** Endianness и delay slots MIPS; SPARC register windows; PPC64 ELFv1 vs ELFv2. Сверяй ABI по прологу/эпилогу.

## §5. Символическое исполнение

**Признак.** Ввод короткий, проверка — ветвления и арифметика, нет хешей/крипты. **Что делать.** Дать angr найти путь к `win`, избегая `exit`.

```python
import angr, claripy
p = angr.Project("./chall", auto_load_libs=False)
st = p.factory.entry_state()
sm = p.factory.simulation_manager(st)
sm.explore(find=0x401234, avoid=0x401300)
print(sm.found[0].posix.dumps(0))
```

```python
# ограничения на флаг
flag = claripy.BVS("flag", 8 * 32)
st = p.factory.call_state(0x401000, flag)
sm.explore(find=lambda s: b"Correct" in s.posix.dumps(1))
```

```python
# хук внешней функции
p.hook(0x401100, angr.SIM_PROCEDURES["libc"]["strcmp"]())
```

- `find`/`avoid` — адреса или lambda; `solver.eval(flag)`; `eval_upto`.
- `SimProcedure` для `strcmp`, `scanf`, `memcmp`; `call_state` для функций.
- Ускорение: `auto_load_libs=False`, `unicorn` engine, `veritesting`, `ZERO_FILL_UNCONSTRAINED_MEMORY`.
- `Triton`, `Miasm`, `Qiling`, `manticore` — альтернативы.

**Грабли.** Path explosion на циклах; ограничивай длину и `avoid`. Символическое исполнение плохо переживает крипту/хеши — там лучше brute force или инверсия. `angr` может не знать syscall — хукай.

### Z3

```python
from z3 import *
x = BitVec("x", 32)
s = Solver()
s.add((x * 0x41C64E6D + 0x3039) & 0xffffffff == 0x12345678)
print(s.check(), s.model())
```

**Грабли.** `BitVec` без `& mask` даёт бесконечную арифметику; для 32-bit всегда маскируй. Таймауты на нелинейной арифметике; упрощай вручную.

### Patch/hook

```python
from pwn import *
elf = ELF("./sample")
elf.write(0x1234, b"\x90\x90")
elf.save("./patched")
```

```python
import lief
b = lief.parse("sample")
b.patch_address(0x1234, [0x90, 0x90])
b.write("patched")
```

- IDA: `Edit → Patch program → Change byte`; Binary Ninja: `Patch` в HLIL.
- x64dbg: `Space` → assemble, `Ctrl+P` → patch file.
- Frida: `Interceptor.replace`; `LD_PRELOAD`; `detours`.

**Грабли.** Патч по file offset ≠ VA ≠ RVA. Для PIE пересчитывай базу; для подписанных PE патч ломает подпись.

## §6. Крипто и математика в реверсе

**Признак.** Много констант, таблиц, раундов, `mod`, `pow`, ECC. **Что делать.** Идентифицировать примитив по константам, затем инвертировать или решать уравнения.

| Константа | Что это |
|---|---|
| `67452301 efcdab89 98badcfe 10325476` | MD5 init |
| `6a09e667 bb67ae85 3c6ef372` | SHA-256 init |
| `0x9e3779b9` | TEA delta / golden ratio |
| `0x41C64E6D 0x3039` | LCG (MSVC) |
| `0x9908B0DF` | MT19937 |
| `0xEDB88320` | CRC32 reflected |
| `63 7c 77 7b f2 6b 6f c5` | AES S-box |
| `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/` | Base64 |

### Feistel / раундовые шифры

**Признак.** Пары `left/right`, XOR с round key, rotate/multiply, 16 раундов. **Что делать.** Повторить `F`, развернуть порядок раундов.

```python
def F(r, k):
    t = ((((r << 13 | r >> 19) ^ k) * 0x9E3779B9) ^ 0x85EBCA6B) + 0x1337 & 0xffffffff
    t = ((t << 7 | t >> 25) ^ (k >> 8))
    return t ^ (k & 0xff)

def decrypt(block, keys):
    l, r = block
    for k in reversed(keys): l, r = r ^ F(l, k), l
    return l, r
```

**Грабли.** `FeistelCipher.decrypt` в `Wincrack` меняет местами `new_left/new_right`; проверь на одном блоке. Ключи могут генерироваться Markov chain/MT — сначала восстанови seed.

### ECC

```python
from sage.all import *
F = GF(P); C = EllipticCurve(F, [a, b])
G = C(x, y)
d = discrete_log(Q, G, operation="+")   # если порядок гладкий
```

**Грабли.** Для суперсингулярной кривой порядок считается; `C.order()` может быть большим. В `nanomachines` проверяли `Q = P * 31337`, решение — `P = Q * inverse(31337, order)`.

### Полиномы

```python
R.<x> = PolynomialRing(GF(2))
g = gcd(poly1 - (x - r1), poly2 - (x - r2))
```

**Грабли.** В `magick_lock` остаток от деления на полином флага даёт `x - root`; НОД нескольких полиномов восстанавливает флаг. Следи за старшим коэффициентом.

### Knapsack / MITM

```python
# n <= 40: 2^(n/2)
left = {sum(...): mask for mask in range(1 << (n//2))}
for mask in range(1 << (n - n//2)):
    if target - sum(...) in left: ...
```

**Грабли.** В `miracle` рюкзак на Rust: 56 весов, MITM делит их на 28+28 бит (2^28 вариантов на половину). Проверь, что веса и target в одном поле.

### Golomb / кодирование

**Признак.** Унарный префикс + бинарный остаток, битовый поток. **Что делать.** Восстановить параметр `M`, читать `q` единиц, затем `ceil(log2 M)` бит.

**Грабли.** В `simple_encoder` ARM/C++ и статическая линковка; сигнатуры FLIRT помогают найти `std::vector`. Проверь порядок бит.

### Timing / side-channel

```python
import time
def measure(x):
    t = time.perf_counter_ns(); run(x); return time.perf_counter_ns() - t
# медиана по 100+ запусков, сравнивай по байтам/битам
```

**Грабли.** Шум; закрепляй CPU, отключай turbo, делай много повторов. В `crackme2077` VMP/WinAPI — время проверки; в `watcher` — утечка по страницам кода.

## §7. Чек-лист на 20 минут

1. Триаж: `file`/`diec`/`strings`/`rabin2`/`binwalk`; запусти — что просит, сеть/файлы/антидебаг.
2. Найди ввод: `scanf`, `fgets`, `read`, `GetWindowText`, `strcmp`, `memcmp`, `Verify`.
3. Кросс-референсы к «Correct/Invalid/flag» — выйди на проверку.
4. Декомпилируй `main`/`check`; переименуй функции и типы; найди константы.
5. Брейк на сравнении; сравни буферы и регистры с вводом.
6. Ветвление — патчь jump или keygen; проверь на 2–3 входах.
7. Код меняется — `mprotect`/дамп; VM — dispatch, handler, bytecode, лифт.
8. Android/.NET/Rust/Go — декомпилятор и хуки; математика — Sage/Z3/MITM.
9. Флаг: формат, регистр, `\n`, динамический источник; отправь ровно то, что просит checker.

## §8. Разбор задач Кубка 2022–2025

| Задача | Год | Техника | Вывод |
|---|---|---|---|
| `Wincrack` | 2025 | Windows TLS-callback, PEB seed, антидебаг, Feistel + Markov chain | callback патчит фейковую проверку; seed в `PEB+0x400/0x800`, снять anti-debug |
| `annabelle` | 2025 | staged RWX-буферы, ARC4 с ключом-хешем кода, Angr по стадиям | расшифровать стадии, идти с конца, решать каждую символьно |
| `nanomachines` | 2025 | Rust ECC + nanomites (fork/ptrace/SIGSEGV), `P = Q * 31337^-1 mod order` | арифметика в отладчике; обратная операция по порядку кривой |
| `miracle` | 2025 | Rust, рюкзачная криптосистема, meet-in-the-middle | не брутить 2^n, делить на 2^(n/2) |
| `2fac` | 2023 | Android Kotlin/ProGuard/Hilt, сертификат приложения, Fibonacci nonce, Frida | алгоритм восстанавливается по `TwoFacViewModel`; подпись — из `PackageManager` |
| `magick_lock` | 2023 | полиномы над GF(2), остатки, GCD | `poly = (x-root) + k*flag_poly`; НОД восстанавливает флаг |
| `monitoring` | 2023 | Bun standalone, встроенный JS, `sus`-обфускация, Deno `--allow-read` | `rabin2 -zzz` + `dd`; несколько путей через запятую обходят sandbox |
| `time_capsule` | 2023 | кастомная VM, модифицированный MD5, соль, brute 256 | реализовать хеш; альтернатива — подменить `getrandom` |
| `bebrus` | 2022 | патченное ядро, проверка в `vfs_read`, скрытые строки | diff `vmlinux`, искать добавленный код в syscall |
| `crackme2077` | 2022 | VMProtect, timing-атака, WinAPI | не реверсить VM, измерять время проверки |
| `simple_encoder` | 2022 | ARM C++, stripped, статическая линковка, Golomb | FLIRT/сигнатуры, затем декодер Голомба |
| `unicorn_plc` | 2022 | Unicorn Engine, MIPS/PowerPC/SPARC blobs | эмулировать каждый blob или переписать и брутить |

## §9. Типовые ошибки на контесте

- **Архитектура/адреса.** ARM как x86, MIPS BE/LE, Thumb; file offset ≠ RVA ≠ VA, PIE-база, не тот сегмент. `file`, `rabin2 -I`, `readelf -lW`.
- **Типы.** Декомпилятор показывает `int`, а там `size_t`/`uint64_t`; массив на самом деле структура. Проверяй `movzx/movsx` и размеры.
- **Антидебаг.** Проверка меняет поведение; `bp main` пропускает TLS; `int3` детектится. ScyllaHide/hardware bp/патч проверки.
- **Упаковка.** Дамп до распаковки; не восстановлены импорты; `.text` ещё зашифрован. Дамп после `mprotect`/`VirtualProtect`, Scylla.
- **VM.** Неверная длина операнда, перепутаны VM-регистры и регистры хоста, не учтён нелинейный `pc`.
- **Крипта/Angr.** Брутфорс вместо алгебры, неверный модуль/порядок; path explosion, нет hook, плохие `find/avoid`. Sage/Z3, лимит длины, Unicorn.
- **Рантаймы.** Rust/Go: мономорфизация, `Vec`/`String`, Go ABI; .NET: обфускатор, IL, strong name; Android: ABI, подпись, Frida. `rustfilt`, `GoReSym`, `de4dot`.
- **Флаг.** `ctfcup{}` vs `CTFCup{}`, лишний `\n`, обрезанная `}`, динамический флаг. Копируй ровно из checker'а.

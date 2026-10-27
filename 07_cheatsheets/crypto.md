# Крипто — шпаргалка к X Кубку CTF России 2026

> Формат: «увидел артефакт → что делать». Команды для Linux/Kali; в Sage и Python считать в отдельных процессах.
> Обозначения сложности: `[B]` beginners, `[M]` medium, `[H]` hard.

## Когда открывать

| Видишь | Открывай раздел |
|---|---|
| `n, e, c`, PEM-ключ, «RSA» в названии | 1. RSA |
| Один и тот же `n` в нескольких файлах | 1.3 Common modulus / shared primes |
| `e=3`, `e=5`, короткий ciphertext | 1.1 Малый e, 1.2 Hastad |
| Огромный `e`, близкие `p` и `q` | 1.4 Wiener, 1.5 Fermat |
| Сервер отдаёт «padding ok / error» | 2.5 Padding oracle, 3.8 Bleichenbacher |
| CTR/GCM, повтор nonce | 2.7 Nonce reuse, 2.8 GCM |
| Бинарник с эллиптикой, «curve», «point» | 3.1 ECC |
| `p-1` гладкое, маленький порядок генератора | 3.2 DH, 3.3 Pohlig-Hellman |
| Матрицы, «trace», «det», подписывание матрицами | 3.5 Matrix DLP |
| Рюкзак, супервозрастающая последовательность | 3.6 Subset sum / LLL, 3.7 Knapsack MITM |
| `random`, `seed`, `randint`, `getrandbits` | 4. PRNG |
| Хэш в MAC, `sha256(secret + msg)` | 5.1 Length extension |
| `bcrypt`, длинный пароль, обрезание | 5.3 Salt overflow |
| «Быстро/медленно», замеры времени | 3.9 Timing |
| Кастомный шифр из слоёв XOR/подстановок | 2.1 XOR, 7. babycrypto |
| Трафик с DH и обменом точками | 3.1–3.2, 7. geometry |

## 0. Триаж за 3 минуты

```bash
file *; wc -c *; strings -n 8 * | head -50
python3 -c "print(open('task.py').read())"    # исходник часто важнее условия
sage -c "print(factor(12345678901234567890))"
```

1. Выпиши все числа и их роли: модуль, экспонента, ciphertext, порядок группы, размер в битах.
2. Проверь, не дан ли уже приватный ключ/секрет: `grep -R "BEGIN\|flag\|secret" .`.
3. Проверь малые/особые случаи: `m=0/1`, `c<n`, `gcd(c,n)>1`, `e=1`, `d=1`.
4. Только потом строй атаку. 80% тасков Кубка ломаются на первом-втором шаге.

## 1. RSA
### 1.1 Малый e (без паддинга)

`c = m^e mod n`, если `m^e < n`, корень берётся точно.

```python
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes
m, ok = iroot(c, 3)
if ok: print(long_to_bytes(int(m)))
```

Если `c` чуть больше `n` — пробуй `iroot(c + k*n, e)` для `k = 1..10000`.
Если `e` и `phi` не взаимно просты — `e` часто чётное; реши для `e' = e/2`, затем извлеки корень.

### 1.2 Hastad broadcast

Одно сообщение, одинаковый `e`, разные `n_i`:

```python
from sympy.ntheory.modular import crt
from gmpy2 import iroot
M, _ = crt(ns, cs)          # M = m^e mod prod(ns)
m, ok = iroot(int(M), e)
print(long_to_bytes(int(m)))
```

Условие: сообщений не меньше `e`, и `m^e < prod(n_i)`. Иначе — Coppersmith с частично известным сообщением.

### 1.3 Common modulus / общие простые

Одинаковый `n`, разные `e`, одно `m`:

```python
from math import gcd
from sympy import gcdex
g, a, b = gcdex(e1, e2)                  # a*e1 + b*e2 = 1
m = pow(c1, a, n) * pow(c2, b, n) % n
```

`gcd(n1, n2) > 1` → общий простой, факторизация мгновенная:

```python
p = gcd(n1, n2); q1 = n1 // p; q2 = n2 // p
d = pow(e, -1, (p-1)*(q1-1))
```

### 1.4 Wiener (малый d)

Условие `d < n^0.25 / 3`. Разложение `e/n` в цепную дробь; подходят подходящие дроби `k/d`.

```python
# sage
for k, d in continued_fraction(e/n).convergents():
    if k == 0: continue
    if (e*d - 1) % k: continue
    phi = (e*d - 1) // k
    # x^2 - (n - phi + 1)x + n = 0
    D = (n - phi + 1)^2 - 4*n
    if D >= 0 and is_square(D):
        p = (n - phi + 1 + sqrt(D)) // 2
        assert n % p == 0
```

Расширение: Boneh–Durfee `d < n^0.292` — lattice-атака, есть в `RsaCtfTool --attack boneh_durfee`.

### 1.5 Факторизация

```bash
RsaCtfTool.py --publickey pub.pem --private          # всё сразу
RsaCtfTool.py --publickey pub.pem --attack all --dumpkey
yafu "factor(123456789012345678901234567890)"
ecm -c 200 1e6 < n.txt
msieve -q -v n.txt
cado-nfs.py n.txt
```

Fermat — если `|p-q|` мало:

```python
from math import isqrt
a = isqrt(n) + 1
while True:
    b2 = a*a - n
    b = isqrt(b2)
    if b*b == b2:
        print(a-b, a+b); break
    a += 1
```

Pollard p-1 — если `p-1` гладкое:

```python
# sage
p = pollard_pm1(n, B=10^6)
```

Pollard rho / ECM — средние множители; ECM лучше для 20–60 бит.
SQUFOF — до ~60 бит, есть в `RsaCtfTool`.

Проверь также: `n` — квадрат/куб (`iroot`), `n` — произведение близнецов, `n = p^k`, `p` восстановим из `dp`, `dq`, `d`.

### 1.6 Partial key exposure

- Дан `d` целиком → `m = pow(c, d, n)`; факторизация не нужна.
- Дан `dp = d mod (p-1)`:
  ```python
  for a in range(2, 100):
      p = gcd(pow(a, e*dp, n) - a, n)
      if 1 < p < n: break
  ```
- Даны старшие/младшие биты `p`: Coppersmith, `f(x) = p_high + x`, корень `< N^0.25`.
- Даны младшие биты `d`: Howgrave-Graham / Boneh–Durfee; в `RsaCtfTool` — `--attack partial_d`.
- Даны `p ^ q`, `p + q`, `phi` → решай квадратное уравнение.

```python
# sage: известны старшие 50% p
P.<x> = PolynomialRing(Zmod(n))
f = (p_high + x).monic()
for r in f.small_roots(X=2^(bits_missing), beta=0.5):
    p = gcd(int(p_high + r), n)
```

### 1.7 Franklin–Reiter (связанные сообщения)

Даны `c1 = m1^e`, `c2 = (a*m1 + b)^e`, один `n`:

```python
# sage
R.<x> = PolynomialRing(Zmod(n))
g1 = (a*x + b)^e - c2
g2 = x^e - c1
g = gcd(g1, g2)
print(g.roots())
```

Для `e=3` и линейной связи — работает почти всегда; для произвольного полинома — resultant.

### 1.8 Coppersmith

Ищет малый корень `f(x) ≡ 0 mod N`, `|x| < N^(1/deg)`. Обязательно `monic()`.

```python
# sage
P.<x> = PolynomialRing(Zmod(N))
f = (known_high + x)^e - c
f = f.monic()
roots = f.small_roots(X=2^unknown_bits, beta=1.0, epsilon=0.01)
```

Типовые применения: стереотипный паддинг, частично известный `m`, младшие биты `p`, `d`, утечка старших бит секрета, `m = m_high + x`.
Если корень не находится: увеличивай `X`, меняй `beta`, добавляй `epsilon`, используй `f.small_roots(..., algorithm='boneh_durfee')` или несколько полиномов (multi-coppersmith).

### 1.9 LLL / решётки

- Subset sum: строй базис `[I | a_i]`, последняя строка `[0...0 | S]`, ищи короткий вектор.
- Coppersmith — это тоже LLL; в Sage `small_roots` уже содержит её.
- Приближённый GCD, implicit factorization, Knapsack — через `Matrix(ZZ, ...).LLL()` / `.BKZ()`.
- Проверяй норму и знаки: LLL возвращает `±` вектор, биты читай по модулю.

```python
# sage, шаблон subset sum
M = block_matrix(ZZ, [[identity_matrix(n), matrix(ZZ, n, 1, a)],
                      [matrix(ZZ, 1, n), matrix(ZZ, 1, 1, [S])]])
for row in M.LLL():
    if row[-1] == 0:
        print([abs(x) for x in row[:-1]])
```

## 2. Классика

### 2.1 XOR

- `xor(ct, b'key')` (pwntools) — повторяющийся ключ.
- Один байт: перебор 256 с оценкой печатаемости/частот.
- Повторяющийся ключ: угадай длину по Hamming distance / IC, затем решай каждый столбец как single-byte XOR.
- Known plaintext: `key = ct xor pt`; проверь `ct1 xor ct2 = pt1 xor pt2`.
- Crib dragging: ищи `ctfcup{`, `flag`, `{`, `}`.

```python
def score(b):
    return sum(chr(c) in ' etaonrishdlcupfm' for c in b)
```

### 2.2 Vigenere / частотный анализ

- Индекс совпадения: `IC = sum(n_i*(n_i-1)) / (N*(N-1))`; для английского ≈ 0.066, для случайного ≈ 0.038.
- Длина ключа: Kasiski (повторы) или максимум среднего IC по столбцам.
- Затем каждый столбец — Caesar; реши сдвиг по частотам/словарю.
- Affine (`c=a*p+b`), Hill (матрица над `Z_26`), Playfair/Bacon/ADFGX — реши по известным парам/алфавиту.

```python
from collections import Counter
def ic(s):
    n = len(s); return sum(v*(v-1) for v in Counter(s).values())/(n*(n-1))
```

### 2.3 ECB

- Одинаковые блоки → одинаковый plaintext: ищи повторы по 16 байт.
- Cut-and-paste: собери блоки `admin=1`, `;role=`, переставь.
- Byte-at-a-time: подавай префиксы, сравнивай блоки, восстанавливай по одному байту.
- Детект: `len(set(ct[i:i+16] for i in range(0,len(ct),16)))` мал.

### 2.4 CBC bit flipping

Меняй предыдущий блок, чтобы получить нужный байт в следующем:

```python
ct = bytearray(ct)
ct[pos - 16] ^= old ^ desired
```

Помни про padding: ломается только один блок, хвост может не расшифроваться.

### 2.5 Padding oracle

- Оракул: «padding ok / error», разный код/время.
- Атака: перебирай последний байт предыдущего блока, пока не станет `0x01`; затем `0x02 0x02` и т.д.
- Автоматизация: `padbuster`, `padding-oracle` (python), собственный скрипт с параллельными запросами.

```bash
padbuster http://host/ct.php 5f3c... 16 -cookies "PHPSESSID=..."
```

### 2.6 CRC

CRC — аффинная функция над GF(2): `CRC(a xor b) = CRC(a) xor CRC(b) xor CRC(0)`.
- Восстановление текста по CRC: обрати таблицу, иди с конца (см. `important_task`).
- Подделка CRC: измени 4 байта в сообщении и пересчитай; CRC не защищает от намеренных изменений.
- `crcmod.predefined.mkPredefinedCrcFun('crc-32')`, `binascii.crc32`, `zlib.crc32`.

### 2.7 Nonce reuse (CTR/GCM/ChaCha)

- CTR: `C1 xor C2 = P1 xor P2` — crib dragging.
- GCM: при одном nonce и ключе восстанавливается `H = E_K(0^128)` и tag-ключ; далее подделка tag.
- ChaCha20-Poly1305: аналогично, keystream recovery.

### 2.8 GCM forbidden attack

Собери два сообщения с одинаковым nonce:
`T1 xor T2 = GHASH_H(C1) xor GHASH_H(C2)` — линейно по `H`; реши полином в `GF(2^128)`, найди `H`, затем `E_K(J0)` и tag-ключ.

```python
# sage / gf2
F.<x> = GF(2^128, modulus=...)
```

### 2.9 Self-keying / прочее

- Trithemius: `c_i = p_i xor p_{i-1}`; гамма восстанавливается из известного заголовка (см. `stolen_blueprints`).
- Base64/hex/URL/ROT — сначала CyberChef (Magic), потом код.

## 3. Современная

### 3.1 ECC

```python
# sage
p = ...
E = EllipticCurve(GF(p), [a, b])
print(E.order(), E.abelian_group())
G = E(gx, gy); Q = E(qx, qy)
print(G.discrete_log(Q))
```

- Invalid curve: тот же `a`, другой `b`; сервер не проверяет, что точка на кривой. Подставь точку малого порядка на слабой кривой.
- Small subgroup: порядок точки делит маленький множитель `E.order()`; реши DLP в подгруппе и сложи по CRT.
- Singular curve: дискриминант 0; кривая изоморфна `GF(p)^+` или `GF(p)^*` — DLP сводится к простому.
- Anomalous (`#E = p`): Smart attack, p-адический lift.
- Supersingular / малая степень вложения: MOV, сведение в `GF(p^k)`.
- Twist: точка не на основной кривой, а на twist с гладким порядком.
- Проверь `gcd(order, ...)`, `E.order() == p`, `p == q`, малые коэффициенты.
- Диагностика: `factor(E.order())`, `E.is_singular()`.

### 3.2 Diffie–Hellman

- Маленький порядок `g`: перебор `g^i`, сравни `A`/`B`.
- `p-1` гладкое: Pohlig–Hellman.
- Composite modulus: DLP по CRT.
- Invalid public key: подставь элемент малого порядка, получи утечку секрета по модулю.
- Проверь, не равен ли общий секрет `1`, `-1`, `0`.

```python
# sage
F = GF(p)
g = F(g); h = F(A)
x = discrete_log(h, g, ord=p-1, algorithm='pohlig-hellman')
```

### 3.3 Pohlig–Hellman

Работает, если порядок группы гладкий. Для каждого простого множителя `q^e` решай DLP в подгруппе порядка `q`, затем CRT. Если порядок не гладкий — проверь малое `p`, `g` не образующий, anomalous, pairing.

```python
# sage
n = G.order()
print(factor(n))
x = discrete_log(Q, G, ord=n, algorithm='pohlig-hellman')
```

### 3.4 Pairing / p-адики

- Pairing: `e(P,Q)` bilinear; если задача даёт `e(P,Q)^x`, DLP переносится в `GF(p^k)`.
- Sage: `E.weil_pairing(Q, n)`, `E.tate_pairing(Q, n, k)`.
- p-адики: Hensel lifting, логарифм в `Z/p^k`, трюк Paillier `((x^(p-1) mod p^2) - 1)/p`.
- Полезно, когда модуль `p^2`, а нужно найти `n` (см. `lateralus`): `Zp(p, prec=10)`, `log(R(x))`.

### 3.5 Matrix DLP

- Если `A = G^x` над полем — сведи к DLP через собственные значения/жорданову форму.
- Если матрицы над `Z/N`, а `N` составное — реши по модулю каждого простого и собери CRT.
- Экспонента матрицы: `A^x` считается быстро; логарифм — через порядок и `discrete_log` в компонентах.
- Проверь `det`, `trace`, `charpoly`: часто утечка модуля/порядка (`A.charpoly().factor()`, `A.multiplicative_order()`).

### 3.6 Subset sum / LLL

- Плотность `d = n / log2(max(a_i))`; при `d < 0.94` LLL почти всегда находит решение.
- Строй решётку с целевой суммой, ищи вектор с нулевой последней координатой.
- Если не вышло: BKZ с большим блоком, перебор последних бит, добавь `+1` к базису.
- Проверяй знаки и порядок бит (MSB/LSB).

### 3.7 Knapsack meet-in-the-middle

- Дели пополам, считай все суммы первой половины в `dict`, затем ищи дополнение во второй.
- Сложность `O(2^(n/2))`; для `n=56` это `2^28` — реально.
- Оптимизация: фильтр `sum <= target`, сортировка, `wrapping_add` для `u128`.

```python
left = {}
for mask in range(1 << (n//2)):
    s = sum(a[i] for i in range(n//2) if mask >> i & 1)
    left[s] = mask
for mask in range(1 << (n - n//2)):
    s = sum(a[n//2+i] for i in range(n - n//2) if mask >> i & 1)
    if target - s in left:
        print(left[target-s] | (mask << (n//2)))
```

### 3.8 Bleichenbacher

- Оракул: «padding valid» для RSA PKCS#1 v1.5.
- Держи интервал возможных `m`; для каждого запроса `c * s^e` сужай интервалы.
- Нужны тысячи запросов; параллель и таймауты.
- Вариант с своим паддингом: выбирай байт, который проверяет оракул (см. `good_pad_bad_pad`).
- Реализация: `interval narrowing`, `binary search`; следи за `ceil/floor`.

### 3.9 Timing

- Замеряй время операции для набора открытых текстов.
- Восстанавливай биты экспоненты по разнице времени (Montgomery extra reduction).
- Нужна статистика: много замеров, медиана, отбрасывание выбросов.
- Сначала проверь, что задержка сети не убивает сигнал; используй локальный бинарь/сервис.

## 4. PRNG

### 4.1 MT19937

- 624 подряд `getrandbits(32)` → полное состояние; дальше предсказывай всё.
- Python `random` — MT19937; `randrange`/`randint` используют rejection, поэтому не все выходы «чистые».
- Инструмент: `randcrack`.

```python
from randcrack import RandCrack
rc = RandCrack()
for x in outputs[:624]:
    rc.submit(x)
print(rc.predict_getrandbits(32))
print(rc.predict_randrange(0, 1000))
```

- Если дают `random.random()` (53 бита) — один выход содержит два 32-битных слова; восстанови старшие/младшие биты.
- Если дают `shuffle` — состояние восстанавливается по перестановке, но проще брутить seed.

### 4.2 Python random seed brute

```python
import random
for seed in range(100000):
    random.seed(seed)
    if random.randbytes(4) == known[:4]:
        print(seed); break
```

`babycrypto`: seed — `int(time.time()) % 100000`, 100k вариантов, проверка печатаемости после расшифровки.

### 4.3 LCG

```python
from math import gcd
def recover_lcg(xs):
    ds = [xs[i+1] - xs[i] for i in range(len(xs)-1)]
    m = 0
    for i in range(len(ds)-2):
        m = gcd(m, ds[i+2]*ds[i] - ds[i+1]*ds[i+1])
    if m == 0: return None
    a = (xs[2]-xs[1]) * pow(xs[1]-xs[0], -1, m) % m
    b = (xs[1] - a*xs[0]) % m
    return m, a, b
```

- Если `m` известно — хватит трёх выходов.
- Если `m` неизвестно — gcd определителей; проверь кратные `m`.
- LCG с усечёнными выходами — lattice/LLL или z3.

### 4.4 Java Random

- 48-битное состояние: `seed = (seed * 0x5DEECE66D + 0xB) & ((1<<48)-1)`.
- `nextInt()` возвращает старшие 32 бита; два подряд выхода дают 48-битное состояние с точностью до 16 бит — брути 2^16.
- `nextInt(bound)` — rejection; восстанавливай через z3 или библиотеки `java-random`.

### 4.5 Seed brute

- Маленький seed (время, PID, `os.urandom` не поможет) — перебор.
- Проверяй `seed = int(time.time())`, `% 100000`, `pid`, `uuid`.
- Для `random.seed(str)` — перебирай строки/словарь, не числа.

## 5. Хэши / HMAC

### 5.1 Length extension

Работает для MD5/SHA-1/SHA-256 при схеме `MAC = H(secret || msg)`.

```bash
hashpump -s <hex_sig> -d 'user=guest' -a '&admin=1' -k 16
hash_extender --data 'user=guest' --secret-min 16 --secret-max 32 \
  --append '&admin=1' --format md5 --out-data - --out-signature -
```

Для HMAC length extension **не работает**; ищи утечку ключа/слабый ключ.

### 5.2 Коллизии

- MD5: `fastcoll` (identical-prefix), `hashclash` (chosen-prefix).
- SHA-1: SHAttered; на практике в CTF — готовые пары.
- Проверь, сравнивают ли хэши как строки/числа (`int(hash,16)`), есть ли `==` вместо `hmac.compare_digest`.

### 5.3 Salt overflow / truncation

- bcrypt обрезает пароль до 72 байт: два пароля с одинаковыми первыми 72 байтами эквивалентны.
- DES `crypt` — 8 символов; PHP-исторические схемы — свои лимиты.
- Если соль/пароль обрезается, добавь хвост, который не влияет на хэш, и обойди проверку.
- Murmur3 — не криптохэш: `int(murmur3('')) = 0`, preimage ищется брутом/z3 (см. `murdata`).

### 5.4 HMAC

`HMAC(K,m)=H((K xor opad)||H((K xor ipad)||m))`; length extension не применим — атакуй слабый/короткий ключ, сравнение или утечку `K`. Если ключ — пароль, `hashcat`/`john`.

## 6. Инструменты

| Инструмент | Зачем | Команда |
|---|---|---|
| SageMath | факторизация, LLL, ECC, Coppersmith | `sage -python solve.py`, `sage -c "..."` |
| PARI/GP | factor, znlog, elllog | `gp -q` → `factor(n)`, `znlog(h,g)` |
| RsaCtfTool | авто-атаки RSA | `RsaCtfTool.py --publickey pub.pem --private` |
| z3 | моделирование, брут бит | `Solver()`, `BitVec` |
| angr | символьное исполнение | `angr.Project(...)`, `call_state` |
| pycryptodome | AES/RSA/утилиты | `from Crypto.Util.number import *` |
| gmpy2 | быстрые корни/инверсии | `iroot`, `invert`, `next_prime` |
| hashcat | перебор хэшей | `hashcat -m 0 -a 0 h.txt rockyou.txt` |
| john | хэши/архивы | `john --format=raw-md5 h.txt` |
| CyberChef | быстрый decode/convert | локально/в браузере |

Коды hashcat: `0` MD5, `100` SHA1, `1400` SHA256, `1700` SHA512, `1000` NTLM, `22000` WPA, `11600` 7-Zip, `13600` WinZip, `1800` sha512crypt, `16500` JWT.

```bash
zip2john file.zip > z.hash && john z.hash --wordlist=rockyou.txt
pdf2john file.pdf > p.hash && john p.hash
ssh2john id_rsa > s.hash && john s.hash
```

## 7. Разбор задач Кубка

| Задача | Год | Техника | Ключевая идея |
|---|---|---|---|
| babycrypto | 2025 | кастомный шифр + brute seed | seed = `time % 100000`; снимай слои с конца, перебирай 100k и проверяй печатаемость |
| cursed | 2025 | p-адики + matrix DLP + LLL | `N=p^2q^2`; `E=e^M`; факторизуй по `gcd(E-I,N)`, логарифм в `Z/p^2`, затем subset sum по `trace` через BKZ |
| miracle | 2025 | knapsack MITM | 56 коэффициентов, `2^28` в каждой половине; сумма → маска → число-флаг |
| geometry | 2023 | DH в малой группе | группа симметрий 1337-угольника, порядок `2*1337`; перебор степени, MD5, AES-ECB |
| lateralus | 2023 | Fibonacci mod p^2 + p-адики | `phi^n` через квадратное уравнение; sqrt по Cipolla+Hensel; логарифм по трюку Paillier |
| murdata | 2023 | hash length extension + Murmur3 | пустой пароль = hash 0; HLE подписывает `.../../admin`; путь до flag |
| dinosaurs | 2022 | корреляционная атака на LFSR | фильтрующий генератор → комбинирующий; порционная корреляционная атака, восстановление состояния |
| good_pad_bad_pad | 2022 | Bleichenbacher | свой PKCS-оракул; сужение интервалов по «валидным» запросам + бинарный поиск |
| important_task | 2022 | CRC preimage | обратная таблица CRC-128, восстановление текста с конца по контрольной сумме |
| stolen_blueprints | 2022 | self-keying / Trithemius | `c_i = p_i xor p_{i-1}`; известный JPEG-заголовок даёт гамму, ключ 252 |
| the_time_has_come | 2022 | timing side channel | время Montgomery-возведения; побитовое восстановление 168-битной экспоненты с look-ahead |

## 8. Чек-лист «15 минут на крипто-таск»

1. **0–2 мин.** `file`, `strings`, прочитай исходник/условие, выпиши все параметры и их размеры.
2. **2–4 мин.** Проверь халяву: `gcd(c,n)`, `e=1/3`, `m^e<n`, `n` — квадрат, приватный ключ рядом, `d` маленькое.
3. **4–6 мин.** Определи примитив: RSA / ECC / DH / PRNG / хэш / кастом. Открой соответствующий раздел.
4. **6–9 мин.** Запусти готовое: `RsaCtfTool`, `factor`, `discrete_log`, `randcrack`, `hashpump`.
5. **9–12 мин.** Если не берёт — ищи утечку: partial key, общий модуль, малый порядок, повтор nonce, линейность CRC, слабый seed.
6. **12–15 мин.** Напиши минимальный скрипт, проверь на локальном примере, только потом бей remote. Зафиксируй таймаут и параллельность.

## 9. Грабли

- **Порядок группы ≠ модуль.** Для ECC `E.order()`, для `Z/p` `p-1`, для матриц — порядок матрицы. DLP решай в правильной группе.
- **`p` vs `q` vs `N`.** В `cursed` выдают `p`, а модуль `N` маскируют через `R`; не подставляй `p` вместо `N`.
- **Кодировки.** Флаг может быть в UTF-8/UTF-16/latin-1; пробуй `long_to_bytes`, `.decode('utf-8', 'replace')`, `bytes.fromhex`.
- **Endianness.** Python `to_bytes(..., 'little')` vs `'big'`; в задачах с матрицами/битами порядок часто обратный.
- **`ceil/floor`.** В Bleichenbacher и интервалах ошибка на 1 ломает всё; используй целочисленную арифметику и проверяй границы.
- **Таймауты.** Remote-оракул может отвечать секунды; запускай в потоках, но не устраивай DDoS. Для локального — `timeout`.
- **Отрицательный `d`.** В Python 3.8+ `pow(c, d, n)` при `d<0` возвращает инверсию `c^|d|`; если `c` не взаимно прост с `n`, сначала проверь `gcd`.
- **Sage vs Python.** `^` в Sage — степень, в Python — XOR. `/` в Sage — рациональное, используй `//` или `Zmod`.
- **`small_roots` требует monic.** Приводи полином к `monic()`, иначе корни не те.
- **Паддинг.** Если `m^e > n`, малый `e` не сработает; проверь, есть ли PKCS/OAEP.
- **Один и тот же `k` в ECDSA/DSA.** Nonce reuse → `k = (z1-z2)/(s1-s2)`, затем приватный ключ.
- **Не выдумывай флаг.** Если расшифровка даёт мусор — вернись на шаг назад, проверь модуль и порядок байт.

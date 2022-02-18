from functools import reduce
from math import sqrt
import random
from random import SystemRandom


def is_prime(p, base=50):
    '''
    Tests whether p is prime, using the given base.
    The result False implies that p is definitely not prime.
    The result True implies that p **might** be prime.
    It is a probabilistic test!
    '''
    result = 1
    exponent = p-1
    modulus = p
    # Chop off the '0b' part of the binary expansion of exponent
    bitstring = bin(exponent)[2:]
    # Iterates through the "letters" of the string.  Here the letters are '0' or '1'.
    for bit in bitstring:
        # We need to compute this in any case.
        sq_result = result*result % modulus
        if sq_result == 1:
            # Note that exponent is congruent to -1, mod p.
            if (result != 1) and (result != exponent):
                return False  # a ROO violation occurred, so p is not prime
        if bit == '0':
            result = sq_result
        if bit == '1':
            result = (sq_result * base) % modulus
    if result != 1:
        return False  # a FLT violation occurred, so p is not prime.

    # If we made it this far, no violation occurred and p might be prime.
    return True


def getprimeover(N):
    """Return a random N-bit prime number
    """
    randfunc = random.SystemRandom()
    n = randfunc.randrange(2**(N-1), 2**N) | 1
    while not is_prime(n):
        n += 2
    return n


def is_primroot_safe(b, p, size):
    q = getprimeover(size)
    '''
    Checks whether b is a primitive root modulo p,
    when p is a safe prime.  If p is not safe,
    the results will not be good
    '''
    # q = (p-1) / 2   # q is the Sophie Germain prime
    if b % p == 1:  # Is the multiplicative order 1?
        return False
    if (b*b) % p == 1:  # Is the multiplicative order 2?
        return False
    if pow(b, q, p) == 1:  # Is the multiplicative order q?
        return False
    return True  # If not, then b is a primitive root mod p.


def mult_inverse(a, m):
    '''
    Finds the multiplicative inverse of a, mod m.
    If gcd(a,m) = 1, this is returned via its natural representative.
    Otherwise, None is returned.
    We modify the solve_le() function
    '''
    u = a  # We use u instead of dividend.
    v = m  # We use v instead of divisor.
    u_hops, u_skips = 1, 0  # u is built from one hop (a) and no skips.
    v_hops, v_skips = 0, 1  # v is built from no hops and one skip (b).
    while v != 0:   # We could just write while v:
        q = u // v  # q stands for quotient.
        r = u % v  # r stands for remainder.  So u = q(v) + r.

        r_hops = u_hops - q * v_hops  # Tally hops
        r_skips = u_skips - q * v_skips  # Tally skips

        u, v = v, r  # The new dividend,divisor is the old divisor,remainder.
        u_hops, v_hops = v_hops, r_hops  # The new u_hops, v_hops is the old v_hops, r_hops
        # The new u_skips, v_skips is the old v_skips, r_skips
        u_skips, v_skips = v_skips, r_skips

    g = u  # The variable g now describes the GCD of a and b.
    if g == 1:
        return u_hops % m
    else:  # When gcd(a,m) is not 1...
        return None


"""
Plaintext: messaggio.
Ciphertext: messaggio cifrato, dipende dal plaintext e dalla chiave.
Algoritmo di cifratura: trasforma il plaintext in ciphertext.
Key: usata come input dall'algoritmo di cifratura, non dipende dal plaintext.
Algoritmo di decifratura: trasforma il ciphertext in plaintext.
"""

# CIFRARIO DI CESARE


def inrange(n, range_min, range_max):
    range_len = range_max - range_min + 1
    a = n % range_len
    if a < range_min:
        a = a + range_len
    return a


def caesar_shift(c, shift):
    ascii = ord(c)
    a = ascii + shift  # Now we have a number between 32+shift and 126+shift.
    a = inrange(a, 32, 126)  # Put the number back in range.
    return chr(a)


def caesar_cipher(plaintext, shift):
    ciphertext = ''
    for c in plaintext:  # Iterate through the characters of a string.
        ciphertext = ciphertext + caesar_shift(c, shift)
    return ciphertext


m = 'Hello! Can you read this?'
print('Message: ', m)
# Message:  Hello! Can you read this?

c = caesar_cipher(m, 6)
print('Ciphertext: ', c)
# Ciphertext:  Nkrru'&Igt& u{&xkgj&znoyE

m_2 = caesar_cipher(c, -6)
print('Plaintext: ', m_2)
# Plaintext:  Hello! Can you read this?

# BRUTE FORCE IL CIFRARIO DI CESARE

for i in range(26):
    print('#', i, ': ', caesar_cipher(c, -i))

"""
# 0 :  Nkrru'&Igt& u{&xkgj&znoyE
# 1 :  Mjqqt&%Hfs%~tz%wjfi%ymnxD
# 2 :  Lipps%$Ger$}sy$vieh$xlmwC
# 3 :  Khoor$#Fdq#|rx#uhdg#wklvB
# 4 :  Jgnnq#"Ecp"{qw"tgcf"vjkuA
# 5 :  Ifmmp"!Dbo!zpv!sfbe!uijt@
# 6 :  Hello! Can you read this?
# 7 :  Gdkkn ~B`m~xnt~qd`c~sghr>
# 8 :  Fcjjm~}A_l}wms}pc_b}rfgq=
# 9 :  Ebiil}|@^k|vlr|ob^a|qefp<
# 10 :  Dahhk|{?]j{ukq{na]`{pdeo;
# 11 :  C`ggj{z>\iztjpzm`\_zocdn:
# 12 :  B_ffizy=[hysioyl_[^ynbcm9
# 13 :  A^eehyx<Zgxrhnxk^Z]xmabl8
# 14 :  @]ddgxw;Yfwqgmwj]Y\wl`ak7
# 15 :  ?\ccfwv:Xevpflvi\X[vk_`j6
# 16 :  >[bbevu9Wduoekuh[WZuj^_i5
# 17 :  =Zaadut8VctndjtgZVYti]^h4
# 18 :  <Y``cts7UbsmcisfYUXsh\]g3
# 19 :  ;X__bsr6TarlbhreXTWrg[\f2
# 20 :  :W^^arq5S`qkagqdWSVqfZ[e1
# 21 :  9V]]`qp4R_pj`fpcVRUpeYZd0
# 22 :  8U\\_po3Q^oi_eobUQTodXYc/
# 23 :  7T[[^on2P]nh^dnaTPSncWXb.
# 24 :  6SZZ]nm1O\mg]cm`SORmbVWa-
# 25 :  5RYY\ml0N[lf\bl_RNQlaUV`,
"""

# CIFRATURA ASIMMETRICA


def is_prime_v2(n):
    i = 2
    while i < sqrt(n):
        if n % i == 0:
            print(str(i) + " is a factor of " + str(n))
            return False
        i += 1
    return True


n = 84579321
print(n, ' e\' primo? ', is_prime_v2(n))
# 23 is a factor of 10100000007987493
# 10100000007987493  e' primo?  False

# Crivello di Eratostene


def erathostenes_sieve(n):
    # the values between square brackets form a list
    primes = [False, False] + [True] * (n - 2)
    # that is different from an array, for example
    i = 2
    while i < n:
        # we do not deal with composite numbers
        if not primes[i]:
            i += 1
            continue
        k = i * i
        # mark multiples of i as composite numbers
        while k < n:
            primes[k] = False
            k += i
        i += 1
    return primes


def whereTrue(list):
    return [i for i in range(len(list)) if list[i]]


print('I numeri primi fino a 75 sono: ', whereTrue(erathostenes_sieve(75)))
# I numeri primi fino a 75 sono:  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73]


def powermod_1(base, exponent, modulus):
    return (base**exponent) % modulus


def powermod_2(base, exponent, modulus):
    p = 1
    e = 0
    while e < exponent:
        p = (p*base) % modulus
        e += 1
    return p


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


gcd(102, 10010300101)  # 1


def rsa_privatekey(bitlength):
    p = getprimeover(bitlength)
    q = getprimeover(bitlength)
    return p, q


def rsa_publickey(p, q, e=65537):
    N = p*q
    return N, e


def rsa_encrypt(message, N, e):
    return pow(message, e, N)


def rsa_decrypt(ciphertext, p, q, N, e):
    totient = N - (p + q) + 1
    # This uses the extended Euclid's algorithm... very quick
    d = mult_inverse(e, totient)
    return pow(ciphertext, d, N)


def text2Int(text):
    """Convert a text string into an integer"""
    return reduce(lambda x, y: (x << 8) + y, map(ord, text))


def int2Text(number, size):
    """Convert an integer into a text string"""
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")


def modSize(mod):
    """Return length (in bytes) of modulus"""
    modSize = len("{:02x}".format(mod)) // 2
    return modSize


messaggio = text2Int("we meet at 11")

# ESEMPIO

# Chave Privata
p, q = rsa_privatekey(1024)

print("p = " + str(p))
print("q = " + str(q))


# Chiave Pubblica
N, e = rsa_publickey(p, q)

print("N = " + str(N))
print("e = " + str(e))


# Cifriamo
c = rsa_encrypt(messaggio, N, e)
print(int2Text(c, modSize(N)))


# Decifriamo
m = rsa_decrypt(c, p, q, N, e)
print(int2Text(m, modSize(N)))


# Diffie-Hellman protocol

q = getprimeover(256)

print('q è: ', q)
# q è:  85594276417829527473700530760982827083429947468288912255400114061242210989461


def findprimroot_safe(prime, size):
    b = 2  # Start trying with 2.
    while True:  # We just keep on looking.
        if is_primroot_safe(b, prime, size):
            return b
        b = b + 1  # Try the next base.  Shouldn't take too long to find one


g = findprimroot_safe(q, 256)
print(g)
# 2

Xa = SystemRandom().getrandbits(256)  # Alice's secret number
Xb = SystemRandom().getrandbits(256)  # Bob's secret number

print('Alice a: ', Xa) # Alice a:  88240788970133105991468135449122465663712488004493495670012224920137342627473
print('Bob b: ', Xb) # Bob b:  8419181208617066159442953510001672908490666525743690658042712767533976093640

Ya = pow(g, Xa, q) # computed by Alice
Yb = pow(g, Xb, q) # computed by Bob

print(pow(Yb, Xa, q)) # 48306524634097119391379203805772513859410510615365622551633349031025403890630
print(pow(Ya, Xb, q)) # 48306524634097119391379203805772513859410510615365622551633349031025403890630

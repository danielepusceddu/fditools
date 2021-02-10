from math import log

def removeprefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix):]
    else:
        return self[:]

def getPower(a, b):
    'If a is b^k, return k. Else return false.'
    l = int(round(log(a, b)))
    if b ** l == a:
        return l
    else:
        return False

def chunks_rightaligned(l, n):
    orphan = len(l) % n
    if orphan:
        yield l[:orphan]
    for i in range(orphan, len(l), n):
        yield l[i:i+n]

def baseXtobase10(base, n: str, print_procedure = False):
    assert(base >= 2 and base <= 16)
    weights = {hex(x)[2:]:x for x in range(0, 0x10)}
    result = 0

    if print_procedure:
        print(f'Converting {n} from base {base} to base 10.')

    for i, symbol in enumerate(n[::-1]):
        symbol = symbol.lower()
        value = weights[symbol] * base**i
        result += value

        if print_procedure:
            print(f'{weights[symbol]} * {base**i} = {value}')

    if print_procedure:
        print(f'Result: {result}')
    return result

def base10tobaseX(n: int, base, print_procedure = False):
    result = ''
    weights = {x:hex(x)[2:] for x in range(0, 0x10)}

    if print_procedure:
        print(f'Converting {n} from base 10 to base {base} using successive division.')

    q = n
    if q == 0:
        return '0'
    while q != 0:
        original = q
        r = q % base
        q //= base

        if print_procedure:
            print(f'{original} / {base} = \t ({q}, {r})')

        result = weights[r] + result

    if print_procedure:
        print(f'Result: {result}')
        print('')

    return result

def fractionalBaseXtoBase10(fractional: str, basesrc: int, print_procedure = False):
    if print_procedure:
        print(f'Converting fractional part 0.{fractional} from {basesrc} to Base 10.')

    weights = {hex(x)[2:]:x for x in range(0, 0x10)}
    result = 0

    for i, symbol in enumerate(fractional, 1):
        symbol = symbol.lower()
        modifier = basesrc ** (-i)
        weight = weights[symbol] * modifier
        result += weight

        if print_procedure:
            print(f'{symbol} * (1 / {basesrc ** i}) = {weight}')

    if print_procedure:
        print(f'Result: {round(result, 8)}')

    return str(result).replace('0.', '')


def fractionalBaseYToBaseX(fractional, basesrc, basedest, print_procedure = False):
    result = ''
    result_view = ''
    weights = {x:hex(x)[2:] for x in range(0, 0x10)}

    if basesrc != 10:
        fractional = fractionalBaseXtoBase10(fractional, basesrc, print_procedure=True)
        pass

    if basedest != 10:
        if print_procedure:
            print(f'Converting fractional part 0.{fractional} from base 10 to {basedest}.')

        f = float('0.' + fractional)
        while len(result) != 16:
            mul = round(f * basedest, 8)
            digit = int(mul)
            digit_str = weights[digit]

            if print_procedure:
                print(f'{basedest} * {f} = {mul} \t\t {digit_str}')
            f = round(mul - digit, 8)

            result += digit_str
            result_view += digit_str
            if len(result) % 4 == 0:
                result_view += ' '
                print('')

    if print_procedure:
        print(f'Result: {result_view}')

    return result

def twos_complement(bits: str, num_bits: int):
    assert len(bits) <= num_bits, f'Too many bits! {len(bits)} inserted, should be {num_bits} max'
    assert all([bit in ['0', '1'] for bit in bits]), f'Bits should be 1 or 0 only!'
    inversion_map = {'0': '1', '1': '0'}
    bits = bits.zfill(num_bits)

    result = ''
    invert = False
    for bit in reversed(bits):
        if not invert:
            result = bit + result
            if bit == '1':
                invert = True
        else:
            result = inversion_map[bit] + result


    return result


def baseconversion(basesrc: int, basedest: int, n: str):
    valid_symbols = '0123456789ABCDEF,.'
    assert basesrc >= 2 and basesrc <= 16, 'Base should be from 2 to 16'
    assert basedest >= 2 and basedest <= 16, 'Base should be from 2 to 16'
    assert '-' not in n, 'Conversion of negative numbers not allowed!'
    base_symbols = '0123456789ABCDEF'[:basesrc] + ',.'
    assert all([c.lower() in base_symbols.lower() for c in n]), 'Invalid symbols'

    p1 = getPower(basesrc, basedest)
    p2 = getPower(basedest, basesrc)
    fraction = ''
    result: str = ''
    negative = False

    for c in (',', '.'):
        if c in n:
            n, fraction = n.split(c)
            print(f'Fraction detected. Whole: {n}, Decimal: {fraction}')
            break

    # From base 10 to base x
    if basesrc == 10:
        result = base10tobaseX(int(n), basedest, print_procedure=True)

    # From base x to base 10
    elif basedest == 10:
        result = baseXtobase10(basesrc, n, print_procedure=True)

    # Converting from b^k to b
    elif p1:
        print(f'Converting {n} from {basesrc} to {basedest} using base b^k to base b method.')
        k = p1
        for symbol in n:
            symbol_weight = baseXtobase10(basesrc, symbol)
            symbol_converted = base10tobaseX(symbol_weight, basedest).zfill(k)
            print(f'{symbol} \t {symbol_converted}')
            result += symbol_converted

        print(f'Result: {result}')

    # Converting from b to b^k
    elif p2:
        print(f'Converting {n} from {basesrc} to {basedest} using base b to base b^k method.')
        k = p2
        chunks = chunks_rightaligned(n, k)
        for chunk in chunks:
            chunk_base10 = baseXtobase10(basesrc, chunk)
            chunk_basedest = base10tobaseX(chunk_base10, basedest)
            result += chunk_basedest
            print(f'{chunk} \t {chunk_base10} \t {chunk_basedest}')
        print(f'Result: {result}')

    else:
        print(f'Algorithm: Base X ({basesrc}) to Base Y ({basedest})')
        n_base10 = baseXtobase10(basesrc, n, print_procedure=True)
        n_base10 = base10tobaseX(n_base10, basedest, print_procedure=True)

    if fraction:
        fraction_result = fractionalBaseYToBaseX(fraction, basesrc, basedest, print_procedure=True)
        result = f'{result}.{fraction_result}'
        print(f'Result: {result}')

    return result

def twos_complement_convert(n: int, num_bits: int):
    assert n >= -(2**(num_bits - 1)), f'{n} (base 10) cannot be represented with only {num_bits} bits (two\'s complement).'
    assert n <= 2**(num_bits - 1) - 1, f'{n} (base 10) cannot be represented with only {num_bits} bits (two\'s complement).'

    negative = n < 0
    if negative:
        n *= -1

    result = baseconversion(10, 2, str(n))
    result = result.zfill(num_bits)

    if negative:
        print(f'Doing two\'s complement of {n}.')
        print(result)
        result = twos_complement(result, num_bits)
        print(result)
        print('')

    return result

def sum_dec(x: int, y: int, num_bits: int, difference=False, print_procedure=True):
    result = ''
    carry = '0'

    if difference:
        if print_procedure:
            print(f'Difference: changing {y} to {y * -1}')
        y *= -1

    x_bin = twos_complement_convert(x, num_bits)
    y_bin = twos_complement_convert(y, num_bits)


    for  a, b in zip(reversed(x_bin), reversed(y_bin)):
        s = int(a) + int(b) + int(carry[0])
        if s > 1:
            carry = '1' + carry
        else:
            carry = '0' + carry

        result = str(s % 2) + result

    if print_procedure:
        carry_len = len(carry)
        print(f'Summing {x} and {y}')
        print(carry.replace('0', ' '))
        print(x_bin.rjust(carry_len))
        print(y_bin.rjust(carry_len))
        print('-' * carry_len)
        print(result.rjust(carry_len))

        if carry[0] != carry[1]:
            print('OVERFLOW: carry ', end='')
            if carry[0] == '1':
                print('after sign bit.')
            else:
                print('on sign bit.')

        print('')

    return result

def italianToBuglisi(italian: str):
    translation = {'p': 'b', 't': 'd', 'q': 'g', 'z': 'zz'}
    result = italian
    for t in translation:
        result = result.replace(t, translation[t])
        result = result.replace(t.upper(), translation[t].upper())
    result = result.replace('z', 'Z')

    return result


def decimalToIEEE(n):
    binary = baseconversion(10, 2, n)
    point_pos = binary.find('.')

    # Find first meaningful digit
    meaningful_digit: int = None
    for i, c in enumerate(binary):
        if c not in ('0', '.'):
            meaningful_digit = i
            break

    exponent = point_pos - meaningful_digit
    if exponent < 0:
        exponent += 1
    normalized = '0.' + binary[meaningful_digit:].replace('.', '')
    print(f'Normalized Mantissa: {normalized}')
    print(f'Exponent:            {exponent}')



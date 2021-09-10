import sys
import traceback
import numpy as np
import math


def write_to_file(file, string1):
    f = open(file, mode='w')
    f.write(string1)
    f.close()


def read_file(file):
    f = open(file, mode='r')
    message = ''
    for ch in f.read():
        if ch != '\n':
            message += ch
    if not message:
        print("НЕТ СООБЩЕНИЯ В ФАЙЛЕ in.txt")
        sys.exit()
    f.close()
    return message

def get_alphabet(file):
    f = open(file, mode='r')
    alphabet = ''
    for ch in f.read():
        if ch != '\n':
            alphabet += ch
    if alphabet:
        y = []
        for i in alphabet:
            if i not in y:
                y.append(i)
        alphabet = (''.join(y))
    else:
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
    f.close()
    return alphabet


ALPHABET = get_alphabet("alphabet.txt")
len_of_alphabet = len(ALPHABET)


def get_key_cesar(file, array):
    f = open(file, mode='r')
    letter = ''
    for ch in f.read():
        if ch != '\n':
            letter += ch
    key = array.index(letter)
    if not letter:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    f.close()
    return key


def get_key_affine(file, array):
    f = open(file, mode='r')
    letter1 = f.read(1)
    letter2 = f.read(1)
    key1 = array.index(letter1)
    key2 = array.index(letter2)
    if not key1 or not key2:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    f.close()
    return key1, key2


def get_key_substitution(file):
    f = open(file, mode='r')
    key = ''
    for ch in f.read():
        if ch != '\n':
            key += ch
    if not key:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    if len(key) != len_of_alphabet:
        print("НЕПРАВИЛЬНЫЙ КЛЮЧ")
        sys.exit()
    f.close()
    return key


def get_key_hill(file):
    f = open(file, mode='r')
    key = ''
    for ch in f.read():
        if ch != '\n':
            key += ch
    if not key:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    if len(key) != 4:
        print("НЕПРАВИЛЬНЫЙ КЛЮЧ")
        sys.exit()
    key1 = np.matrix(
        [[ALPHABET.index(key[0]), ALPHABET.index(key[1])], [ALPHABET.index(key[2]), ALPHABET.index(key[3])]])
    f.close()
    return key1


def get_key_columnar(file):
    f = open(file, mode='r')
    key = ''
    for ch in f.read():
        if ch != '\n':
            key += ch
    if not key:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    if len(key) > len_of_alphabet:
        print("НЕПРАВИЛЬНЫЙ КЛЮЧ")
        sys.exit()
    f.close()
    return key


def get_key_vigenere(file):
    f = open(file, mode='r')
    key = ''
    for ch in f.read():
        if ch != '\n':
            key += ch
    if not key:
        print("НЕТ КЛЮЧА В ФАЙЛЕ key.txt")
        sys.exit()
    f.close()
    return key


def offset(char, offset):
    return ALPHABET[(ALPHABET.index(char) + offset) % len_of_alphabet]


class Caesar:
    @staticmethod
    def encrypt(message, key):
        return ''.join(map(offset, list(message), [key, ] * len(message)))

    @staticmethod
    def decrypt(ciphertext, key):
        return ''.join(map(offset, list(ciphertext), [len_of_alphabet - key, ] * len(ciphertext)))


class Vigenere:
    @staticmethod
    def encrypt(message, key):
        return ''.join(
            map(offset, message, list(map(lambda x: ALPHABET.index(x), key)) * (len(message) // len(key) + 1)))

    @staticmethod
    def decrypt(ciphertext, key):
        return ''.join(map(offset, ciphertext,
                           list(map(lambda x: len_of_alphabet - ALPHABET.index(x), key)) * (
                                   len(ciphertext) // len(key) + 1)))


class Substitution:
    @staticmethod
    def encrypt(message, key):
        cipher_alph = Substitution.buildAlphabet(key)
        return ''.join(cipher_alph[ALPHABET.index(ch)] for ch in message)

    @staticmethod
    def buildAlphabet(key):
        offseted_alph = ''.join(map(offset, list(ALPHABET), [ALPHABET.index(key[-1]) + 1, ] * len(ALPHABET)))
        return (key + ''.join([ch for ch in offseted_alph if not (ch in key)]))

    @staticmethod
    def decrypt(ciphertex, key):
        cipher_alph = Substitution.buildAlphabet(key)
        return ''.join(ALPHABET[cipher_alph.index(ch)] for ch in ciphertex)


class Affine:
    @staticmethod
    def modReverse(a, b):
        r, s, t = [min(a, b), max(a, b)], [1, 0], [0, 1]
        while r[-1] != 1:
            q = r[-2] // r[-1]
            r.append(r[-2] - q * r[-1])
            s.append(s[-2] - q * s[-1])
            t.append(t[-2] - q * t[-1])
        return (s[-1] % r[1])

    @staticmethod
    def encrypt(message, key):
        if math.gcd(key[0], len_of_alphabet) != 1:
            print('Индекс первой буквы ключа должен быть взаимнопростым с длинной алфавита')
            sys.exit()
        return ''.join(ALPHABET[(ALPHABET.index(ch) * key[0] + key[1]) % len_of_alphabet] for ch in message)

    @staticmethod
    def decrypt(ciphertext, key):
        if math.gcd(key[0], len_of_alphabet) != 1:
            print('Индекс первой буквы ключа должен быть взаимнопростым с длинной алфавита')
            sys.exit()
        try:
            return ''.join(
                ALPHABET[Affine.modReverse(key[0], len_of_alphabet) * (ALPHABET.index(ch) - key[1]) % len_of_alphabet]
                for ch in
                ciphertext)
        except ZeroDivisionError:
            pass


class ColumnarTransposition:
    @staticmethod
    def encrypt(message, key):
        message = message + ' ' * ((0 - len(message) % len(key)) % len(key))
        res = ''.join([message[k] for i in ColumnarTransposition.transformkey(key) for k in range(len(message)) if
                       k % len(key) == i])
        return res

    @staticmethod
    def decrypt(ciphertext, key):
        return ''.join(
            [ciphertext[ColumnarTransposition.transformkey(key).index(i) * len(ciphertext) // len(key) + k] for k in
             range(len(ciphertext) // len(key)) for i in range(len(key))])

    @staticmethod
    def transformkey(key):
        return [i[0] for i in sorted([i for i in enumerate(key)], key=lambda x: x[1])]


letter_to_index = dict(zip(ALPHABET, range(len(ALPHABET))))
index_to_letter = dict(zip(range(len(ALPHABET)), ALPHABET))


class Hill:
    @staticmethod
    def work_condition(matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        if math.gcd(det, modulus) != 1:
            print("Детерминант должен быть взаимнопростым с длинной алфавита")
            sys.exit()
        else:
            pass


    @staticmethod
    def matrix_mod_inv(matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = Affine.modReverse(det,modulus)
        matrix_modulus_inv = (
                det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus)
        return matrix_modulus_inv

    @staticmethod
    def encrypt(message, K):
        encrypted = ""
        message_in_numbers = []

        for letter in message:
            message_in_numbers.append(letter_to_index[letter])

        split_P = [
            message_in_numbers[i: i + int(K.shape[0])]
            for i in range(0, len(message_in_numbers), int(K.shape[0]))
        ]

        for P in split_P:
            P = np.transpose(np.asarray(P))[:, np.newaxis]

            while P.shape[0] != K.shape[0]:
                P = np.append(P, letter_to_index[" "])[:, np.newaxis]

            P = np.transpose(np.asarray(P))

            numbers = np.dot(P, K) % len_of_alphabet
            numbers = np.transpose(numbers)
            n = numbers.shape[0]

            for idx in range(n):
                number = int(numbers[idx, 0])
                encrypted += index_to_letter[number]
        return encrypted

    @staticmethod
    def decrypt(cipher, Kinv):
        decrypted = ""
        cipher_in_numbers = []

        for letter in cipher:
            cipher_in_numbers.append(letter_to_index[letter])

        split_C = [
            cipher_in_numbers[i: i + int(Kinv.shape[0])]
            for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
        ]

        for C in split_C:
            numbers = np.dot(C, Kinv) % len_of_alphabet
            numbers = np.transpose(numbers)
            n = numbers.shape[0]

            for idx in range(n):
                number = int(numbers[idx, 0])
                decrypted += index_to_letter[number]
        return decrypted


if __name__ == '__main__':
    which_cipher = int(input(
        '1 - Шифр сдвига\n2 - Афинный шифр\n3 - Шифр простой замены\n4 - Шифр Хилла\n5 - Шифр перестановки\n6 - Шифр Виженера\n'))

    what_to_do = int(input("1 - Зашифровать\n2 - Расшифровать\n"))

    if which_cipher == 1 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            c = Caesar.encrypt(test, get_key_cesar('key.txt', ALPHABET))
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 1 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            c = Caesar.decrypt(test, get_key_cesar('key.txt', ALPHABET))
            write_to_file('encrypt.txt', c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
    elif which_cipher == 2 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            c = Affine.encrypt(test, get_key_affine('key.txt', ALPHABET))
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 2 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            c = Affine.decrypt(test, get_key_affine('key.txt', ALPHABET))
            write_to_file('encrypt.txt', c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
    elif which_cipher == 3 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            c = Substitution.encrypt(test, get_key_substitution('key.txt'))
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 3 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            c = Substitution.decrypt(test, get_key_substitution('key.txt'))
            write_to_file("encrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
    elif which_cipher == 4 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            K = get_key_hill('key.txt')
            Hill.work_condition(K,len_of_alphabet)
            c = Hill.encrypt(test, K)
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 4 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            K = get_key_hill('key.txt')
            Hill.work_condition(K, len_of_alphabet)
            Kinv = Hill.matrix_mod_inv(K, len_of_alphabet)
            c = Hill.decrypt(test, Kinv)
            write_to_file("encrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
    elif which_cipher == 5 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            c = ColumnarTransposition.encrypt(test, get_key_columnar('key.txt'))
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 5 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            c = ColumnarTransposition.decrypt(test, get_key_columnar('key.txt'))
            write_to_file("encrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
    elif which_cipher == 6 and what_to_do == 1:
        test = read_file('in.txt')
        try:
            c = Vigenere.encrypt(test, get_key_vigenere('key.txt'))
            write_to_file("decrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле decrypt.txt!')
    elif which_cipher == 6 and what_to_do == 2:
        test = read_file('in.txt')
        try:
            c = Vigenere.decrypt(test, get_key_vigenere('key.txt'))
            write_to_file("encrypt.txt", c)
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc().splitlines()[-1])
            sys.exit()
        print('Ответ в файле encrypt.txt!')
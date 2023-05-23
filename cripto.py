# Модуль RSA шифрования
import math
import random
import time


class Cripto():
    '''
    Генерирует приватный и публичный ключи, шифрует и дешифрует текст
    '''
    def __init__(self):
        self.START_GENERATOR = 65 * pow(10, 7)
        self.END_GENERATOR = 75 * pow(10, 7)

    def get_decrypt(self, data: str, d: int, n: int) -> str:
        '''
        Дешифрует текст
        :param data: текст сообщения
        :param d: секретный ключ
        :param n: модуль 
        '''
        result = ''
        for j in range(3, len(data), 22):
            temp = int(data[j:j+19])
            temp = pow(temp, d, n)
            result += chr(temp)
        return result

    def get_encrypt(self, text: str, e: int, n: int) -> str:
        '''
        Шифрует текст
        :param data: текст сообщения
        :param e: публичный ключ
        :param n: модуль - произведение двух простых, не равных чисел
        '''
        result = ''
        for i in range(0,len(text)):
            temp = str(pow(ord(text[i]), e, n))
            temp = temp.zfill(19)
            while len(temp) < 22:
                temp =  str(random.randint(1, 9)) + temp
            result += temp
        return result

    def get_gcd(self, a: int, b: int) -> int:
        '''
        Находит наибольший общий делитель для чисел a и b
        :param a, b: простые числа a != b
        '''
        if(b == 0):
            return a
        return self.get_gcd(b, a % b)

    def get_keys(self) -> tuple:
        '''
        Генерирует кортедж чисел для шифрования/дешифрования
        '''
        p, q = self.get_prime_pair()
        n = p * q
        phi = (p - 1) * (q - 1)
        public_key = self.get_public_key(phi)
        secret_key = self.get_secret_key(public_key, phi)
        return n, public_key, secret_key

    def get_prime_pair(self) -> tuple:
        '''
        Генерирует пару простых чисел
        '''
        while 1:
            while 1:
                p = random.randint(self.START_GENERATOR, self.END_GENERATOR)
                if self.is_prime(p):
                    break
            while 1:
                q = random.randint(self.START_GENERATOR, self.END_GENERATOR)
                if self.is_prime(q):
                    break
            if p != q:
                break
        return p, q

    def get_public_key(self, phi: int) -> int:
        '''
        Генерирует публичный ключ
        :param phi: Функция Эйлера – функция, равная количеству натуральных
        чисел, меньших n и взаимно простых с ним
        '''
        while 1:
            public_key = random.randrange(1, phi)
            if self.get_gcd(public_key, phi) == 1:
                break
        return public_key

    def get_secret_key(self, public_key: int, phi: int) -> int:
        '''
        Генерирует приватный ключ
        :param phi: Функция Эйлера – функция, равная количеству натуральных
        чисел, меньших n и взаимно простых с ним
        '''
        secret_key = self.multiplicative_inverse(public_key, phi)
        return secret_key

    def is_prime(self, n: int) -> bool:
        '''
        Проверка на простое число
        '''
        if n == 1:
            return False
        for i in range(2, int(math.sqrt(n))+1):
            if n % i == 0:
                return False
        return True

    def multiplicative_inverse(self, e: int, phi: int) -> int:
        '''
        Генерация приватного ключа
        :param e: публичный ключ
        :param phi: Функция Эйлера – функция, равная количеству натуральных
        чисел, меньших n и взаимно простых с ним
        '''
        u1, u2, u3 = 1, 0, e
        v1, v2, v3 = 0, 1, phi
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % phi


if __name__ == '__main__':

    crp = Cripto()
    n, public_key, secret_key = crp.get_keys()
    print('n',n)
    print('public_key', public_key)
    print('secret key= ', secret_key)

    #sentence = '''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ ёЁ qwertyuiop[]asdfghjkl;\'zxcvbnm,./  `   QWERTYUIOP[]ASDFGHJKL;\'ZXCVBNM,./'''
    sentence = 'abc абв \nqwer йцук'

    start_time = time.time()
    enc =  crp.get_encrypt(sentence, public_key, n)
    runTime = (time.time() - start_time)
    print('Time encr: %s' % runTime)

    start_time = time.time()
    res = crp.get_decrypt(enc, secret_key, n)
    runTime = (time.time() - start_time)
    print('Time decr: %s' % runTime)
    print(res)
    print(res == sentence)





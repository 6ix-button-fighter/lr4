class BlowFish:

    def __init__(self, p, s):
        self.p = p
        self.s = s

    def __f(self, number: int) -> int:
        temp = self.s[0, number >> 24]
        temp = (temp + self.s[1, number >> 16 & 0xff]) % (0x1 << 32)
        temp = temp ^ self.s[2, number >> 8 & 0xff]
        temp = (temp + self.s[3, number & 0xff]) % (0x1 << 32)
        return temp

    def str_to_int(self, string: str):
        return sum([ord(string[i]) << (24 - 8 * i) for i in range(4)])

    def encrypt(self, plain_text: str) -> tuple[str, int]:
        added_symbols_length = (8 - len(plain_text) % 8) % 8
        text = str(plain_text) + 'k' * added_symbols_length
        result_text = ''
        for i in range((len(plain_text) - 1) // 8 + 1):
            left = self.str_to_int(text[8 * i:8 * i + 4])
            right = self.str_to_int(text[8 * i + 4:8 * (i + 1)])
            for j in range(16):
                left ^= self.p[j]
                right = self.__f(left) ^ right
                # print(f'Epoch : {i + 1}\nRound : {j + 1}')
                left, right = right, left
            left, right = right, left
            left = left ^ self.p[17]
            right = self.p[16] ^ right
            left <<= 32
            result = left + right
            result_text += ''.join([chr(result >> (56 - 8 * n) & 0xff) for n in range(8)])
        return result_text, added_symbols_length

    def decrypt(self, plain_text: str, added_symbols_length: int) -> str:
        text = str(plain_text)
        result_text = ''
        for i in range((len(plain_text) - 1) // 8 + 1):
            left = self.str_to_int(text[8 * i:8 * i + 4])
            right = self.str_to_int(text[8 * i + 4:8 * (i + 1)])
            left = left ^ self.p[17]
            right = self.p[16] ^ right
            for j in range(16):
                right = self.__f(left) ^ right
                # print(f'Epoch : {i + 1}\nRound : {j + 1}')
                left = left ^ self.p[15 - j]
                left, right = right, left
            left, right = right, left
            left <<= 32
            result = left + right
            result_text += ''.join([chr(result >> (56 - 8 * n) & 0xff) for n in range(8)])
        return result_text[:len(result_text) - added_symbols_length]

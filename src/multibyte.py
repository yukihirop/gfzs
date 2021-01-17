# copy from: https://qiita.com/t4t5u0/items/bd5270d0a7b3def35a03

import unicodedata

# from local

import debug


# https://seiai.ed.jp/sys/text/cs/mcodes/ucodeutf8.html
INVALID_BYTE_START = 0x80
INVALID_BYTE_END = 0xbf
BYTE1_START = 0x00
BYTE1_END = 0x7f
BYTE2_START = 0xc0
BYTE2_END = 0xdf
BYTE3_START = 0xe0
BYTE3_END = 0xef
BYTE4_START = 0xf0
BYTE4_END = 0xff

# ref: https://qiita.com/masakielastic/items/8eb4bf4efc2310ee7baf


class Multibyte:
    def __init__(self, stdscr = None):
        self.stdscr = stdscr

    # https://note.nkmk.me/python-unicodedata-east-asian-width-count/
    def get_east_asian_width_count(self, text):
        count = 0
        for c in text:
            if self.is_full_width(c):
                count += 2
            else:
                count += 1
        return count

    def is_full_width(self, c):
        return unicodedata.east_asian_width(c) in 'FWA'

    def marked_full_width(self, text, mark="\0") -> str:
        result = ''
        for c in text:
            if self.is_full_width(c):
                result += "%s%s" % (c, mark)
            else:
                result += c

        return result

    def getch(self):
        key = self.stdscr.getch()
        text_pool = [key]
        codepoint = key

        if BYTE1_START <= key <= BYTE1_END:
            # e.g.) ascii
            pass
        elif INVALID_BYTE_START <= key <= INVALID_BYTE_END:
            raise 'Invalid Byte: %s' % key
            exit(1)
        elif BYTE2_START <= key <= BYTE2_END:
            # e.g.) Umlaut
            text_pool.append(self.stdscr.getch())
            a, b = text_pool
            tmp = map(lambda x: bin(x)[2:], [0b00011111 & a, 0b00111111 & b])
            tmp = ''.join(item.zfill(6) for item in tmp)
            codepoint = int(tmp, 2)
        elif BYTE3_START <= key <= BYTE3_END:
            # e.g.) Japanease
            for _ in range(2):
                text_pool.append(self.stdscr.getch())

            # e.g) 'あ' = [227, 129, 130]
            a, b, c = text_pool
            tmp = map(lambda x: bin(x)[2:], [
                0b00001111 & a, 0b00111111 & b, 0b00111111 & c])
            tmp = ''.join([item.zfill(6) for item in tmp])
            codepoint = int(tmp, 2)
        elif BYTE4_START <= key <= BYTE4_END:
            for _ in range(3):
                text_pool.append(self.stdscr.getch())

            a, b, c, d = text_pool
            tmp = map(lambda x: bin(x)[2:], [
                0b00000111 & a, 0b00111111 & b, 0b00111111 & c, 0b00111111 & d])
            tmp = ''.join([item.zfill(6) for item in tmp])
            codepoint = int(tmp, 2)
        else:
            pass
        
        return codepoint



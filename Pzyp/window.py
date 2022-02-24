
ENCODED_OFFSET_SIZE = 12

class Window:
    def __init__(self, offset_len=ENCODED_OFFSET_SIZE):
        self._window = []
        self._max_size = 2 ** offset_len
    #:

    def extend(self, data: str):
        self._window.extend(data)
        if len(self._window) >= self._max_size:
            num_bytes_to_remove = len(self._window) - self._max_size
            del self._window[:num_bytes_to_remove]
    #:

    def find_prefix(self, data: str) -> int:
        # procurar por data[:len(data)], data[:len(data)-1], data[:len(data)-2] 
        # (utilizando o algo. de baixo) até encontrar um prefixo 
        # devolve a pos do prefix e o comprimento do prefixo, caso tenha
        # sido encontrado um prefixo; -devolve 1 e 0 caso nenhum prefixo tenha 
        # sido encontrado
        pass
    #:

    def find(self, data: str) -> int:
        w = self._window
        for i, ch in enumerate(w):
            if ch == data[0]:
                j = i
                k = 0
                while k < len(data) and j < len(w):
                    if data[k] != w[j]:
                        break
                    k += 1
                    j += 1
                if k == len(data):
                    return i
                    # return len(self._window) - i
        return -1
    #:

    def get(self, pos: int, prefix_len: int) -> str:
        assert pos + prefix_len < len(self._window)
        return ''.join(self._window[pos:pos + prefix_len])
    #:

    def __repr__(self):
        return f'Window{self._window}'
    #:
#:
















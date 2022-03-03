'''
Usage:
    pzip [-c [-l LEVEL] | -d | -h] [-s] [-p PASSWORD] FILE
Operation:
    -c, --encode, --compress            Compress FILE whith PZYP
    -d, --decode, --decompress          Decompress FILE compressed with PZYP
Options:
    -l, --level                         Compression level [default: 2] 
    -s, --summary                       Resume of compressed file      
    -h, --help                          Shows this help message and exits.
    -p PASSWORD, --password=PASSWORD    An optional password to encrypt the file (compress only)
    FILE                                The path to the file to compress / decompress
'''
# imports
from docopt import docopt
from typing import Union, BinaryIO, Tuple
import math
import lzss_io
import bitstruct
from bitarray import bitarray
import pzypapp as mw



# da referencia lzss_io
UNENCODED_STRING_SIZE = 8   # in bits
ENCODED_OFFSET_SIZE = 12    # in bits
ENCODED_LEN_SIZE = 4        # in bits
ENCODED_STRING_SIZE = ENCODED_OFFSET_SIZE + ENCODED_LEN_SIZE  # in bits

WINDOW_SIZE = 2 ** ENCODED_OFFSET_SIZE        # in bytes
BREAK_EVEN_POINT = ENCODED_STRING_SIZE // 8   # in bytes
MIN_STRING_SIZE = BREAK_EVEN_POINT + 1        # in bytes
MAX_STRING_SIZE = 2 ** ENCODED_LEN_SIZE - 1 + MIN_STRING_SIZE  # in bytes

ctx = lzss_io.PZYPContext(
    encoded_offset_size=4,   # janela terá 16 bytes
    encoded_len_size=3       # comprimentos de 8 + 1 - 1 = 8 bytes
)

DEFAULT_EXT = 'LZS'

# RESUMO DO ALGORITMO:
# itera caractere por caractere
# Verifica se já viu o caractere antes
# Se sim, verifica o próximo caractere e prepara um token para ser emitido
# Se o token for maior que o texto que está representando, não gera um token
# Adiciona o texto ao buffer de pesquisa e continua
# Caso contrário, adiciona o caractere ao buffer de pesquisa e continua


# Verificação do buffer de pesquisa para mais caracteres

def elements_in_array(check_elements, elements):
    i = 0
    offset = 0
    for element in elements:
        if len(check_elements) <= offset:

            # Todos os elementos no check_elements estão nos elements
            return i - len(check_elements)

        if check_elements[offset] == element:
            offset += 1
        else:
            offset = 0

        i += 1
    return -1


encoding = "utf-8"

# compressor


def encode(text, max_sliding_window_size=4096):
    text_bytes = text.encode(encoding)

    search_buffer = []  # Array de numeros inteiros, representando bytes
    check_characters = []  # Array de numeros inteiros, representando bytes
    output = []  # Saída do array

    i = 0
    for char in text_bytes:
        # O index onde os caracteres aparecem na nossa janela/buffer de pesquisa
        index = elements_in_array(check_characters, search_buffer)

        if elements_in_array(check_characters + [char], search_buffer) == -1 or i == len(text_bytes) - 1:
            if i == len(text_bytes) - 1 and elements_in_array(check_characters + [char], search_buffer) != -1:
                # Se for o ultimo caractere, adiciona o proximo caractere ao texto que o token representa
                check_characters.append(char)

            if len(check_characters) > 1:
                index = elements_in_array(check_characters, search_buffer)
                # Calcular a distância relativa
                offset = i - index - len(check_characters)
                # Definir o comprimento do token (Por quantos caracteres o representa)
                length = len(check_characters)

                token = f"<{offset},{length}>"  # Construir o nosso token

                if len(token) > length:
                    # Comprimento do token é maior que o comprimento que o representa, por isso imprime os caracteres
                    output.extend(check_characters)  # Imprime os caracteres
                else:
                    # Imprime o nosso token
                    output.extend(token.encode(encoding))

                # Adiciona os caracteres ao nosso buffer de pesquisa
                search_buffer.extend(check_characters)
            else:
                output.extend(check_characters)  # Imprime o caractere
                # Adiciona os caracteres ao nosso buffer de pesquisa
                search_buffer.extend(check_characters)

            check_characters = []

        check_characters.append(char)

        # Verifica se o search buffer está a exceder o tamanho maximo da janela
        if len(search_buffer) > max_sliding_window_size:
            # Remove o primeiro elemento do buffer de pesquisa
            search_buffer = search_buffer[1:]

        i += 1

    return bytes(output)
    # descompressor
    encoding = "utf-8"


def decode(text):

    text_bytes = text.encode(encoding)  # O texto codificado em bytes
    output = []  # Os caracteres de saída

    inside_token = False
    scanning_offset = True

    length = []  # Numero do comprimento codificado em bytes
    offset = []  # Numero da distância codificada em bytes

    for char in text_bytes:
        if char == "<".encode(encoding)[0]:
            inside_token = True  # Aqui estamos dentro de um token
            scanning_offset = True  # Aqui estamos a procurar pelo numero do comprimento
        elif char == ",".encode(encoding)[0] and inside_token:
            scanning_offset = False
        elif char == ">".encode(encoding)[0]:
            inside_token = False  # Já não estamos dentro do token

            # Converter comprimentos e distancias para um numero inteiro
            length_num = int(bytes(length).decode(encoding))
            offset_num = int(bytes(offset).decode(encoding))

            # Recebe o texto que o token representa
            referenced_text = output[-offset_num:][:length_num]

            # referenced_text é uma lista de bytes para que nós usemos o 'extend' para adicionar cada byte na saída
            output.extend(referenced_text)

            # Reset comprimento e distância
            length, offset = [], []
        elif inside_token:
            if scanning_offset:
                offset.append(char)
            else:
                length.append(char)
        else:
            output.append(char)  # Adiciona o caractere ao nosso output

    return bytes(output)


def main():
    args = docopt(__doc__, version='0.1')
    file = args['FILE']

    if args['--compress']:
        encode(file, args["--encode"], args["--summary"])
    if args['--decompress']:
        decode(file, args["--decode"], args["--summary"])


if __name__ == '__main__':
    main()

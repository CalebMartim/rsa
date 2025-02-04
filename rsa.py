from OAEP import oaep_encode, oaep_decode
import base64

def encriptar(mensagem, chave_publica):
  e, n = chave_publica

  # Hashing por OAEP:
  hash_oaep = oaep_encode(mensagem.encode('utf-8'), 1026)
  
  # Convertemos a cifra OAEP para um número decimal:
  m = int.from_bytes(hash_oaep, 'big')
 
  # Nossa cifra:
  C = pow(m, e, n)

  encriptado = C.to_bytes((n.bit_length() + 7) // 8, 'big')
  return encriptado

def decriptar(cifra, chave_privada):
  d, n = chave_privada

  # Cifra do hashing por OAEP:
  h =  int.from_bytes(cifra, 'big')
  
  M = pow(h, d, n)

  decriptado = M.to_bytes((1026 + 7) // 8, 'big')  
  return oaep_decode(decriptado, 1026).decode('utf-8')

from OAEP import oaep_encode, oaep_decode
from math import ceil

def encriptar(mensagem, chave_publica):
  """
  Args:
      mensagem (str): Mensagem em claro 
      chave_publica: Tupla (e, n)

  Returns:
      bytes: Mensagem cifrada codificada em utf-8
  """
  
  e, n = chave_publica
  bits = n.bit_length()

  # Hashing por OAEP em codificação utf-8:
  hash_oaep = oaep_encode(mensagem.encode('utf-8'), bits)
  
  # Convertemos a cifra OAEP para um número inteiro:
  m = int.from_bytes(hash_oaep)
  
  # Nossa cifra:  
  C = pow(m, e, n)

  bytes_necessarios = ceil(bits / 8) # Função teto
  mensagem_encriptada = C.to_bytes(bytes_necessarios)
  return mensagem_encriptada # Mensagem encriptada codificada em utf-8

def decriptar(cifra, chave_privada):
  """
  Args:
      cifra (str): Mensagem cifrada codificada em utf-8 
      chave_privada: Tupla (d, n)

  Returns:
      bytes: Mensagem decriptada codificada em utf-8
  """
  d, n = chave_privada
  bits = n.bit_length()

  # Cifra do hashing por OAEP:
  h = int.from_bytes(cifra)
  
  # Mensgem recuperada
  M = pow(h, d, n)

  bytes_necessarios = ceil(bits / 8)
  mensagem_codificada = M.to_bytes(bytes_necessarios)  
  return oaep_decode(mensagem_codificada, bits)

from random import randint
from crivo import primos
from OAEP import oaep_encode, oaep_decode
import rsa
from base64 import b64encode, b64decode 

def aleatorio_1024bits():
  s = ""
  # O primeiro dígito será algum diferente de 0:
  s += str(randint(1, 9)) 
  # Os próximos podem ser qualquer um entre 0 e 9:
  for _ in range(307):
    s += str(randint(0, 9))
  
  # Escolhemos algum ímpar aleatório diferente de 5
  # para ser o dígito final:
  impares = [1, 3, 7, 9]
  s += str(impares[randint(0, 3)])

  return int(s) 

def primo(n:int, k = 20):
  # Testando os primeiros primos no Crivo de Eratóstenes:
  for primo in primos:
    if n % primo == 0:
      return False
  
  # Algoritmo de Miller-Rabin:
  d = n - 1
  s = 0
  while d % 2 == 0:
    d //= 2
    s += 1
  for _ in range(k):
      a = randint(2, n - 2)
      x = pow(a, d, n)
      if x == 1 or x == n - 1:
          continue
      for __ in range(s - 1):
          x = pow(x, 2, n)
          if x == n - 1:
              break
      else:
          return False
  return True

def main():
  # Geração de chaves
  p = aleatorio_1024bits()
  q = aleatorio_1024bits()
  while not primo(p):
    p = aleatorio_1024bits()
  while not primo(q):
    q = aleatorio_1024bits()
  
  n = p * q;

  # Função totiente de Euler 
  phi = (p - 1) * (q - 1)
  
  # Expoente público:
  e = 65537

  # Inverso multiplicativo de e módulo phi(n):
  d = pow(e, -1, phi)

  # Chaves em si:
  chave_publica = (e, n)
  chave_privada = (d, n)

  # Leitura da mensagem em claro:
  M = ""
  with open("mensagem.txt", "r") as file:
     M = file.read()
    
  # Mensagem cifrada codificada em UTF-8:
  C = rsa.encriptar(M, chave_publica)

  # Mensagem cifrada codificada em base64:
  x = b64encode(C)
  print(f'Mensagem encriptada:\n{x.decode('utf-8')}\n')

  # Mensagem cifrada decodificada da base64:
  y = b64decode(x)
  mensagem_recuperada = rsa.decriptar(y, chave_privada)
  print(f'Mensagem recuperada:\n{mensagem_recuperada.decode('utf-8')}', end="")
    
if __name__ == "__main__":
  main()
  

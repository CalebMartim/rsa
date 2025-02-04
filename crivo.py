marcado = [False] * 400
primos = []

for i in range(2, 400):
  if not marcado[i]:
    primos.append(i)
    for j in range(i + i, 400, i):
      marcado[j] = True

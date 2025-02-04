import hashlib
import secrets

def mascara(semente, tamanho_mascara):
    
    def funcao_hash(data):
        return hashlib.sha3_256(data).digest()
    
    tamanho_hash = 32 
    
    if tamanho_mascara > (tamanho_hash * (2**32)):
        raise ValueError("Máscara grande demais")
    
    mask = b''
    counter = 0
    
    while len(mask) < tamanho_mascara:
        C = counter.to_bytes(4, 'big')
        hash_input = semente + C
        hash_output = funcao_hash(hash_input)
        mask += hash_output
        counter += 1
    
    return mask[:tamanho_mascara]

def oaep_encode(message, n_bit_len, label=b''):
    # Função de hash (SHA3-256):
    funcao_hash = hashlib.sha3_256

    tamanho_hash = 32 
    
    # Calculate message and semente lengths
    k = (n_bit_len + 7) // 8  # Byte length of the modulus
    msg_max_len = k - 2 * tamanho_hash - 2
    
    if len(message) > msg_max_len:
      raise ValueError(f"Mensagem grande demais. Máximo de {msg_max_len} bytes")
    
    # Hash da label:
    lhash = funcao_hash(label).digest()
    
    # Fazemos o padding na mensagem:
    ps = b'\x00' * (msg_max_len - len(message))
    db = lhash + ps + b'\x01' + message
    
    # Geramos uma semente aleatória:
    semente = secrets.token_bytes(tamanho_hash)
    
    # Geramos uma máscara para o data block:
    mascara_db = mascara(semente, k - tamanho_hash - 1)
    db_mascarada = bytes(a ^ b for a, b in zip(db, mascara_db))
    
    # geramos uma máscara para a semente:
    semente_mascara = mascara(db_mascarada, tamanho_hash)
    semente_mascarada = bytes(a ^ b for a, b in zip(semente, semente_mascara))
    
    # Combinamos a mensagem codificada:
    mensagem_codificada = b'\x00' + semente_mascarada + db_mascarada
    
    return mensagem_codificada

def oaep_decode(mensagem_codificada, n_bit_len, label=b''):

    funcao_hash = hashlib.sha3_256
    tamanho_hash = 32  
    
    # Calculamos os tamanhos
    k = (n_bit_len + 7) // 8  # Número de bytes do módulo
    
    # Valida o tamanho da mensagem codificada
    if len(mensagem_codificada) != k:
        raise ValueError("Tamanho de mensagem codificada inválida")
    
    # Separando os
    semente_mascarada = mensagem_codificada[1:tamanho_hash+1]
    db_mascarada = mensagem_codificada[tamanho_hash+1:]
    
    # Recupera a semente
    semente_mascara = mascara(db_mascarada, tamanho_hash)
    semente = bytes(a ^ b for a, b in zip(semente_mascarada, semente_mascara))
    
    # Recupera data block
    mascara_db = mascara(semente, k - tamanho_hash - 1)
    db = bytes(a ^ b for a, b in zip(db_mascarada, mascara_db))
    
    # Separa componentes de data block
    lhash = db[:tamanho_hash]
    
    # Verifica o label do hash
    expected_lhash = funcao_hash(label).digest()
    if lhash != expected_lhash:
        raise ValueError("Label do hash não condizente")
    
    # Encontra a mensagem
    for i in range(tamanho_hash, len(db)):
        if db[i] == 0x01:
            inicio_mensagem = i + 1
            break
    else:
        raise ValueError("Padding na mensagem inválido")
    
    # Extrai a mensagem
    mensagem = db[inicio_mensagem:]
    
    return mensagem
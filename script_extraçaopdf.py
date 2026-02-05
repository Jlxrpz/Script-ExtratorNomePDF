import os
import fitz

# Pega a pasta onde o .exe está rodando
pasta_atual = os.path.dirname(os.path.abspath(__file__))

# Cria o caminho para a pasta PDFs (vai funcionar em qualquer PC)
pasta_pdfs = os.path.join(pasta_atual, "PDFs")

print("Iniciando processamento de PDFs...")
print(f"📁 Procurando PDFs em: {pasta_pdfs}")

# Verifica se a pasta PDFs existe
if not os.path.exists(pasta_pdfs):
    print("❌ ERRO: Pasta 'PDFs' não encontrada!")
    print("👉 Crie uma pasta chamada 'PDFs' na mesma pasta deste programa.")
    print("Pressione Enter para fechar...")
    input()
    exit()

# Verifica se há PDFs na pasta
arquivos_pdf = [
    f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")
]
if not arquivos_pdf:
    print("❌ Nenhum arquivo PDF encontrado na pasta 'PDFs'!")
    print("👉 Coloque os PDFs na pasta 'PDFs' e execute novamente.")
    print("Pressione Enter para fechar...")
    input()
    exit()

print(f"📄 Encontrados {len(arquivos_pdf)} arquivo(s) PDF para processar")
print("-" * 50)

for nome_arquivo in arquivos_pdf:
    caminho_arquivo = os.path.join(pasta_pdfs, nome_arquivo)
    print(f"📄 Processando: {nome_arquivo}")

    try:
        documento = fitz.open(caminho_arquivo)
        texto_completo = ""
        for pagina in documento:
            texto_completo += pagina.get_text()
        documento.close()

        linhas = [
            linha.strip()
            for linha in texto_completo.split('\n')
            if linha.strip()
        ]
        nome_extraido = None

        # IDENTIFICAÇÃO POR CONTEÚDO ESPECÍFICO
        # Primeiro verifica se é um PDF de Folha
        # (contém "Pagamento de Folha" na linha 2)
        if len(linhas) > 1 and "Pagamento de Folha" in linhas[1]:
            # É um PDF de Folha - pega nome da linha 7
            if len(linhas) > 6:
                nome_extraido = linhas[6].replace("Nome:", "").strip()
                print(f"✅ NOME ENCONTRADO (Folha - linha 7): {nome_extraido}")

        # Se não é Folha, verifica se é PIX (contém "PIX" na linha 2)
        elif len(linhas) > 1 and "PIX" in linhas[1]:
            # É um PDF PIX - pega nome da linha 9
            if len(linhas) > 8:
                nome_extraido = linhas[8].replace("Favorecido:", "").strip()
                print(f"✅ NOME ENCONTRADO (PIX - linha 9): {nome_extraido}")

        # Se não identificou pelos padrões acima, usa a lógica original
        else:
            print(f"⚠️  Usando lógica original para: {nome_arquivo}")
            for i, linha in enumerate(linhas):
                if "Favorecido:" in linha:
                    # O nome está na linha ANTERIOR (i-1)
                    if i - 1 >= 0:
                        nome_candidato = linhas[i - 1]
                        # Verificação básica
                        sem_digitos = not any(
                            char.isdigit() for char in nome_candidato
                        )
                        tem_tamanho = len(nome_candidato) > 5
                        if (len(nome_candidato) > 5
                                and sem_digitos
                                and "CNPJ" not in nome_candidato
                                and "CPF" not in nome_candidato):
                            nome_extraido = nome_candidato
                            print(
                                f"✅ NOME ENCONTRADO: {nome_extraido}"
                            )
                            break

            # Fallback: Procura pela linha antes do CPF
            if not nome_extraido:
                for i, linha in enumerate(linhas):
                    if "CPF:" in linha and i - 1 >= 0:
                        nome_candidato = linhas[i - 1]
                        if (len(nome_candidato) > 5 and
                                not any(
                                    char.isdigit() for char in nome_candidato
                                )):
                            nome_extraido = nome_candidato
                            print(
                                f"✅ Nome encontrado (antes do CPF): "
                                f"{nome_extraido}"
                            )
                            break

        if nome_extraido:
            # Limpeza do nome
            caracteres_invalidos = '<>:"/\\|?*.'
            for char in caracteres_invalidos:
                nome_extraido = nome_extraido.replace(char, '_')

            nome_extraido = ' '.join(nome_extraido.split())
            novo_nome_arquivo = f"{nome_extraido}.pdf"
            novo_caminho = os.path.join(pasta_pdfs, novo_nome_arquivo)

            # Evita duplicatas
            contador = 1
            temp_novo_caminho = novo_caminho
            while os.path.exists(temp_novo_caminho):
                base, ext = os.path.splitext(novo_nome_arquivo)
                temp_novo_caminho = os.path.join(
                    pasta_pdfs, f"{base}_{contador}{ext}"
                    )
                contador += 1

            os.rename(caminho_arquivo, temp_novo_caminho)
            print(
                f"🎉 SUCESSO: '{nome_arquivo}' → "
                f"'{os.path.basename(temp_novo_caminho)}'"
            )
        else:
            print(f"❌ NÃO ENCONTRADO: {nome_arquivo}")
            # Debug das linhas relevantes
            print("  Primeiras 15 linhas para análise:")
            for i, linha in enumerate(linhas[:15]):
                print(f"    Linha {i+1}: {linha}")

        print("-" * 50)

    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        continue

print("✅ Processamento concluído!")
print("Pressione Enter para fechar...")
input()

import os
import fitz  # PyMuPDF

pasta_pdfs = r"C:\Dev\Script-ExtratorNomePDF\PDFs"

print("Iniciando processamento de PDFs...")

for nome_arquivo in os.listdir(pasta_pdfs):
    if nome_arquivo.lower().endswith(".pdf"):
        caminho_arquivo = os.path.join(pasta_pdfs, nome_arquivo)
        print(f"📄 Processando: {nome_arquivo}")

        try:
            documento = fitz.open(caminho_arquivo)
            texto_completo = ""
            for pagina in documento:
                texto_completo += pagina.get_text()
            documento.close()

            # Divide o texto em linhas
            linhas = [
                linha.strip() for linha in texto_completo.split('\n')
                if linha.strip()
            ]

            # DEBUG: Mostra todas as linhas numeradas
            print("📋 Todas as linhas do PDF:")
            for i, linha in enumerate(linhas):
                print(f"  {i:02d}: {linha}")

            nome_extraido = None
            tipo_documento = None

            # 1. IDENTIFICA O TIPO DE DOCUMENTO
            for i, linha in enumerate(linhas):
                linha_lower = linha.lower()

                # Verifica se é PIX
                palavras_pix = ['pix', 'pagamento via pix']
                if any(palavra in linha_lower for palavra in palavras_pix):
                    tipo_documento = "PIX"
                    break
                # Verifica se é Folha de Pagamento
                palavras_folha = ['folha', 'salário', 'salario',
                                  'pagamento de folha']
                if any(palavra in linha_lower for palavra in palavras_folha):
                    tipo_documento = "FOLHA"
                    break

            # Se não identificou pelo conteúdo, tenta pelo nome do arquivo
            if not tipo_documento:
                nome_lower = nome_arquivo.lower()
                if 'pix' in nome_lower:
                    tipo_documento = "PIX"
                elif 'folha' in nome_lower or 'pagamento' in nome_lower:
                    tipo_documento = "FOLHA"

            print(f"🔍 Tipo identificado: {tipo_documento}")

            # 2. EXTRAI O NOME COM BASE NO TIPO
            if tipo_documento == "PIX":
                # PIX: pega linha 09 (índice 8, pois começa em 0)
                if len(linhas) > 39:
                    nome_extraido = linhas[39]  # Linha 09 (índice 8)
                    print(f"✅ PIX - Nome extraído da linha 09: "
                          f"{nome_extraido}")
                else:
                    print("❌ PIX: PDF não tem linha 09")

            elif tipo_documento == "FOLHA":
                # Folha de Pagamento: pega linha 07 (índice 6)
                if len(linhas) > 25:
                    nome_extraido = linhas[25]  # Linha 07 (índice 6)
                    print(f"✅ FOLHA - Nome extraído da linha 07: "
                          f"{nome_extraido}")
                else:
                    print("❌ FOLHA: PDF não tem linha 07")
            else:
                print("❌ Tipo de documento não identificado")

            # 3. RENOMEIA O ARQUIVO
            if nome_extraido:
                # Limpeza do nome
                caracteres_invalidos = '<>:"/\\|?*.'
                for char in caracteres_invalidos:
                    nome_extraido = nome_extraido.replace(char, '_')

                nome_extraido = ' '.join(nome_extraido.split())

                # Remove prefixos/sufixos indesejados
                if nome_extraido.startswith("Nome:"):
                    nome_extraido = nome_extraido[5:].strip()
                if nome_extraido.startswith("Favorecido:"):
                    nome_extraido = nome_extraido[11:].strip()

                # Verificação final
                palavras_invalidas = ['CNPJ', 'CPF', 'LOGISTICA',
                                      'LTDA', 'COMPROVANTE']
                if (len(nome_extraido) >= 3 and
                    not any(palavra in nome_extraido.upper() for palavra in
                            palavras_invalidas)):

                    # Adiciona o tipo ao nome do arquivo (opcional)
                    if tipo_documento:
                        novo_nome_arquivo = (
                            f"{nome_extraido}_{tipo_documento}.pdf"
                        )
                    else:
                        novo_nome_arquivo = f"{nome_extraido}.pdf"

                    novo_caminho = os.path.join(pasta_pdfs, novo_nome_arquivo)

                    # Evita duplicatas
                    contador = 1
                    temp_novo_caminho = novo_caminho
                    while os.path.exists(temp_novo_caminho):
                        base, ext = os.path.splitext(novo_nome_arquivo)
                        nome_temp = f"{base}_{contador}{ext}"
                        temp_novo_caminho = os.path.join(
                            pasta_pdfs, nome_temp
                        )
                        contador += 1

                    os.rename(caminho_arquivo, temp_novo_caminho)
                    novo_basename = os.path.basename(temp_novo_caminho)
                    print(f"🎉 RENOMEADO: '{nome_arquivo}' → "
                          f"'{novo_basename}'")
                else:
                    print(f"❌ Nome inválido: '{nome_extraido}'")
            else:
                print(f"❌ Não foi possível extrair nome de: {nome_arquivo}")

            print("-" * 60)

        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            continue

print("✅ Processamento concluído!")

import os
import fitz

def extrair_linhas_pdf(caminho_pdf):
    """Extrai todas as linhas não vazias de um PDF."""
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
    return linhas

def extrair_nome(linha, metodo, separador=None, posicao=None):
    """
    Extrai o nome da linha conforme método escolhido.
    metodos:
        'separador': usa separador e pega a parte na posicao
        'primeiro_token': pega tudo após o primeiro token (assume CPF)
        'linha_inteira': usa a linha inteira (se já for só o nome)
    """
    if metodo == 'separador' and separador:
        partes = linha.split(separador)
        if len(partes) > posicao:
            return partes[posicao].strip()
    elif metodo == 'primeiro_token':
        tokens = linha.split()
        if len(tokens) > 1:
            return ' '.join(tokens[1:]).strip()
    elif metodo == 'linha_inteira':
        return linha.strip()
    return None

def main():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_pdfs = os.path.join(pasta_atual, "PDFs")

    print("📁 Verificando pasta PDFs...")
    if not os.path.exists(pasta_pdfs):
        print("❌ Pasta 'PDFs' não encontrada!")
        input("Pressione Enter para sair...")
        return

    arquivos_pdf = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith('.pdf')]
    if not arquivos_pdf:
        print("❌ Nenhum PDF encontrado na pasta 'PDFs'!")
        input("Pressione Enter para sair...")
        return

    print(f"📄 Encontrados {len(arquivos_pdf)} PDFs.")

    # --- ESCOLHA DO PDF DE EXEMPLO ---
    print("\n🔍 Escolha um PDF para análise:")
    for i, nome in enumerate(arquivos_pdf[:10], 1):  # Mostra no máximo 10
        print(f"   {i}. {nome}")
    if len(arquivos_pdf) > 10:
        print("   ... (mais arquivos não listados)")

    escolha = input("\nDigite o número do PDF para análise (padrão=1): ").strip()
    try:
        idx = int(escolha) - 1 if escolha else 0
        if idx < 0 or idx >= len(arquivos_pdf):
            print("Número inválido, usando o primeiro.")
            idx = 0
    except ValueError:
        print("Entrada inválida, usando o primeiro.")
        idx = 0

    pdf_exemplo = arquivos_pdf[idx]
    caminho_exemplo = os.path.join(pasta_pdfs, pdf_exemplo)

    print(f"\n📄 Analisando: {pdf_exemplo}")
    linhas = extrair_linhas_pdf(caminho_exemplo)

    print("\n📃 Linhas encontradas no PDF:")
    for i, linha in enumerate(linhas, 1):
        print(f"{i:3d}: {linha}")

    # --- CONFIGURAÇÃO DA EXTRAÇÃO ---
    print("\n⚙️  Configuração da extração do nome:")

    while True:
        try:
            num_linha = int(input("👉 Número da linha que contém o nome: "))
            if 1 <= num_linha <= len(linhas):
                linha_alvo = linhas[num_linha-1]
                print(f"   Linha escolhida: {linha_alvo}")
                break
            else:
                print(f"   Número inválido. Digite entre 1 e {len(linhas)}.")
        except ValueError:
            print("   Digite um número válido.")

    print("\n📌 Como extrair o nome dessa linha?")
    print("   1. Usar um separador (ex: ' - ' ) e pegar uma parte")
    print("   2. Ignorar o primeiro token (assume que é CPF)")
    print("   3. Usar a linha inteira (já é o nome)")

    opcao = input("Escolha uma opção (1/2/3): ").strip()

    metodo = None
    separador = None
    posicao = None

    if opcao == '1':
        separador = input("Digite o separador (ex: ' - '): ").strip()
        if not separador:
            print("Separador vazio, usando padrão ' - '")
            separador = ' - '
        try:
            posicao = int(input("Qual parte pegar? (0 = primeira, 1 = segunda, ...): ").strip())
        except ValueError:
            posicao = 1
            print("Valor inválido, usando posição 1.")
        metodo = 'separador'
    elif opcao == '2':
        metodo = 'primeiro_token'
    elif opcao == '3':
        metodo = 'linha_inteira'
    else:
        print("Opção inválida, usando 'ignorar primeiro token'.")
        metodo = 'primeiro_token'

    # Testar extração no exemplo
    nome_teste = extrair_nome(linha_alvo, metodo, separador, posicao)
    if nome_teste:
        print(f"\n✅ Nome extraído no exemplo: '{nome_teste}'")
    else:
        print(f"\n❌ Falha ao extrair nome. Verifique a configuração.")
        input("Pressione Enter para sair...")
        return

    confirmar = input("Deseja aplicar esta configuração a todos os PDFs? (S/n): ").strip().lower()
    if confirmar == 'n':
        print("Operação cancelada.")
        input("Pressione Enter para sair...")
        return

    # --- PROCESSAMENTO DE TODOS OS PDFs ---
    print("\n🔄 Processando todos os PDFs...")
    sucessos = 0
    falhas = 0

    for nome_arquivo in arquivos_pdf:
        caminho_arquivo = os.path.join(pasta_pdfs, nome_arquivo)
        print(f"\n📄 Processando: {nome_arquivo}")

        try:
            linhas_pdf = extrair_linhas_pdf(caminho_arquivo)
            if len(linhas_pdf) < num_linha:
                print(f"   ⚠️  PDF tem apenas {len(linhas_pdf)} linhas. Pulando.")
                falhas += 1
                continue

            linha_atual = linhas_pdf[num_linha-1]
            nome_extraido = extrair_nome(linha_atual, metodo, separador, posicao)

            if not nome_extraido:
                print(f"   ❌ Não foi possível extrair nome da linha {num_linha}: {linha_atual}")
                falhas += 1
                continue

            # Limpeza do nome para nome de arquivo
            caracteres_invalidos = '<>:"/\\|?*'
            for char in caracteres_invalidos:
                nome_extraido = nome_extraido.replace(char, '_')
            nome_extraido = ' '.join(nome_extraido.split())

            novo_nome = f"{nome_extraido}.pdf"
            novo_caminho = os.path.join(pasta_pdfs, novo_nome)

            # Evitar duplicatas
            contador = 1
            caminho_final = novo_caminho
            while os.path.exists(caminho_final):
                base, ext = os.path.splitext(novo_nome)
                caminho_final = os.path.join(pasta_pdfs, f"{base}_{contador}{ext}")
                contador += 1

            os.rename(caminho_arquivo, caminho_final)
            print(f"   ✅ Renomeado para: {os.path.basename(caminho_final)}")
            sucessos += 1

        except Exception as e:
            print(f"   ❌ Erro: {str(e)}")
            falhas += 1

    print(f"\n📊 Resumo: {sucessos} sucesso(s), {falhas} falha(s).")
    input("Pressione Enter para fechar...")

if __name__ == "__main__":
    main()

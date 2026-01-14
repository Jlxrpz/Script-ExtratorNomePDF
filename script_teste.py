import os
import fitz

def ler_pdf_detalhado(caminho_pdf):
    """
    Lê um PDF e exibe todas as linhas numeradas com seus conteúdos
    """
    if not os.path.exists(caminho_pdf):
        print(f"❌ Arquivo não encontrado: {caminho_pdf}")
        return
    
    print(f"\n{'='*60}")
    print(f"📖 ANALISANDO PDF: {os.path.basename(caminho_pdf)}")
    print(f"Caminho: {caminho_pdf}")
    print(f"{'='*60}")
    
    try:
        # Abre o PDF
        documento = fitz.open(caminho_pdf)
        texto_completo = ""
        
        # Extrai texto de todas as páginas
        for pagina_num, pagina in enumerate(documento):
            print(f"\n📄 PÁGINA {pagina_num + 1}:")
            print("-" * 40)
            
            texto_pagina = pagina.get_text()
            texto_completo += texto_pagina + "\n"
            
            linhas_pagina = [
                linha.strip() 
                for linha in texto_pagina.split('\n') 
                if linha.strip()
            ]
            
            for i, linha in enumerate(linhas_pagina, 1):
                print(f"P{pagina_num+1}L{i:2d}: {linha}")
        
        documento.close()
        
        # Processa todas as linhas do documento completo
        print(f"\n{'='*60}")
        print("📋 RESUMO DE TODAS AS LINHAS (documento completo):")
        print(f"{'='*60}")
        
        todas_linhas = [
            linha.strip() 
            for linha in texto_completo.split('\n') 
            if linha.strip()
        ]
        
        print(f"Total de linhas com conteúdo: {len(todas_linhas)}")
        print(f"\n📝 Conteúdo das linhas (com índices começando em 1):")
        print("-" * 60)
        
        for indice, linha in enumerate(todas_linhas):
            # Mostra índice começando em 1 (para facilitar a leitura humana)
            num_linha = indice + 1
            print(f"L{num_linha:3d}: {linha}")
            
            # Pausa a cada 20 linhas
            if num_linha % 20 == 0:
                input("\n⏸️  Pressione Enter para continuar... ")
        
        # Informações úteis específicas para seu script
        print(f"\n{'='*60}")
        print("🔍 INFORMAÇÕES PARA AJUSTAR SEU SCRIPT PRINCIPAL:")
        print(f"{'='*60}")
        
        if len(todas_linhas) >= 1:
            print(f"\n1. LINHA 1 (índice 0 na programação):")
            print(f"   '{todas_linhas[0]}'")
            
            print(f"\n2. LINHA 2 (índice 1 na programação) - para IDENTIFICAÇÃO:")
            if len(todas_linhas) >= 2:
                linha_2 = todas_linhas[1]
                print(f"   '{linha_2}'")
                
                # Verifica o que tem na linha 2
                print(f"\n   🔎 Análise da Linha 2:")
                if "Pagamento de Folha" in linha_2:
                    print(f"   ✅ CONTÉM 'Pagamento de Folha'")
                elif "PIX" in linha_2:
                    print(f"   ✅ CONTÉM 'PIX'")
                else:
                    print(f"   ❌ NÃO CONTÉM 'Pagamento de Folha' nem 'PIX'")
                    print(f"   Possíveis conteúdos para identificar:")
                    print(f"   - 'Pagamento de Folha': {linha_2 == 'Pagamento de Folha'}")
                    print(f"   - 'Folha': {'Folha' in linha_2}")
                    print(f"   - 'PIX': {'PIX' in linha_2}")
                    print(f"   - 'pix': {'pix' in linha_2.lower()}")
            else:
                print(f"   ❌ Não há linha 2 neste PDF")
        
        # Mostra linhas 7 e 9
        print(f"\n3. LINHA 7 (índice 6) - para EXTRAÇÃO se for Folha:")
        if len(todas_linhas) >= 7:
            linha_7 = todas_linhas[6]
            print(f"   '{linha_7}'")
            
            # Verifica se tem "Nome:"
            if "Nome:" in linha_7:
                nome_extraido = linha_7.replace("Nome:", "").strip()
                print(f"   ✅ CONTÉM 'Nome:' → Nome extraído: '{nome_extraido}'")
            else:
                print(f"   ❌ NÃO CONTÉM 'Nome:'")
                print(f"   Buscando padrões alternativos...")
                if "nome" in linha_7.lower():
                    print(f"   ✅ Tem 'nome' (minúsculo) na linha")
        else:
            print(f"   ❌ Não há linha 7 neste PDF")
        
        print(f"\n4. LINHA 9 (índice 8) - para EXTRAÇÃO se for PIX:")
        if len(todas_linhas) >= 9:
            linha_9 = todas_linhas[8]
            print(f"   '{linha_9}'")
            
            # Verifica se tem "Favorecido:"
            if "Favorecido:" in linha_9:
                nome_extraido = linha_9.replace("Favorecido:", "").strip()
                print(f"   ✅ CONTÉM 'Favorecido:' → Nome extraído: '{nome_extraido}'")
            else:
                print(f"   ❌ NÃO CONTÉM 'Favorecido:'")
                print(f"   Buscando padrões alternativos...")
                if "favorecido" in linha_9.lower():
                    print(f"   ✅ Tem 'favorecido' (minúsculo) na linha")
        else:
            print(f"   ❌ Não há linha 9 neste PDF")
        
        # Busca por padrões em todo o documento
        print(f"\n5. BUSCA POR PADRÕES EM TODO O DOCUMENTO:")
        
        padroes_encontrados = []
        
        # Procura por "Nome:" em qualquer linha
        for indice, linha in enumerate(todas_linhas):
            if "Nome:" in linha:
                padroes_encontrados.append((indice + 1, "Nome:", linha))
        
        # Procura por "Favorecido:" em qualquer linha
        for indice, linha in enumerate(todas_linhas):
            if "Favorecido:" in linha:
                padroes_encontrados.append((indice + 1, "Favorecido:", linha))
        
        # Procura por "Pagamento de Folha" ou "Folha" em qualquer linha
        for indice, linha in enumerate(todas_linhas):
            if "Pagamento de Folha" in linha or "Folha" in linha:
                padroes_encontrados.append((indice + 1, "Folha", linha))
        
        # Procura por "PIX" em qualquer linha
        for indice, linha in enumerate(todas_linhas):
            if "PIX" in linha or "pix" in linha.lower():
                padroes_encontrados.append((indice + 1, "PIX", linha))
        
        if padroes_encontrados:
            print(f"   Padrões encontrados:")
            for num, padrao, conteudo in padroes_encontrados:
                print(f"   Linha {num:3d} [{padrao:12}]: {conteudo}")
        else:
            print(f"   Nenhum padrão encontrado")
        
        # Sugestão final
        print(f"\n{'='*60}")
        print("💡 SUGESTÃO PARA SEU SCRIPT PRINCIPAL:")
        print(f"{'='*60}")
        
        if len(todas_linhas) >= 2:
            linha_2 = todas_linhas[1]
            
            print(f"\nif len(linhas) > 1 and '{linha_2}' in linhas[1]:")
            print(f"    # É um PDF de Folha - pega nome da linha 7")
            
            if len(todas_linhas) >= 7:
                print(f"    nome_extraido = linhas[6].replace('Nome:', '').strip()")
                print(f"    # Linha 7 atual: '{todas_linhas[6]}'")
            
            print(f"\nelif len(linhas) > 1 and '{linha_2}' in linhas[1]:")
            print(f"    # É um PDF PIX - pega nome da linha 9")
            
            if len(todas_linhas) >= 9:
                print(f"    nome_extraido = linhas[8].replace('Favorecido:', '').strip()")
                print(f"    # Linha 9 atual: '{todas_linhas[8]}'")
        
        print(f"\n{'='*60}")
        
    except Exception as e:
        print(f"❌ ERRO ao ler o PDF: {str(e)}")

# Interface principal com caminho fixo
def main():
    print("🔍 ANALISADOR DE PDF - Encontre as linhas corretas")
    print("-" * 50)
    
    # Caminho fixo que você forneceu
    caminho_fixo = r"C:\Dev\Script-ExtratorNomePDF\pdf_teste\seu_arquivo.pdf"
    caminho_pasta = r"C:\Dev\Script-ExtratorNomePDF\pdf_teste"
    
    print(f"📁 Caminho da pasta: {caminho_pasta}")
    
    # Verifica se o caminho fixo existe
    if os.path.exists(caminho_fixo):
        print(f"✅ Arquivo encontrado: {caminho_fixo}")
        ler_pdf_detalhado(caminho_fixo)
    else:
        print(f"❌ Arquivo não encontrado: {caminho_fixo}")
        
        # Lista arquivos na pasta
        if os.path.exists(caminho_pasta):
            print(f"\n📄 Arquivos disponíveis na pasta:")
            arquivos = os.listdir(caminho_pasta)
            pdfs = [f for f in arquivos if f.lower().endswith(".pdf")]
            
            if pdfs:
                for i, pdf in enumerate(pdfs, 1):
                    print(f"  {i}. {pdf}")
                
                try:
                    escolha = int(input(f"\n👉 Escolha um PDF (1-{len(pdfs)}): ")) - 1
                    if 0 <= escolha < len(pdfs):
                        caminho = os.path.join(caminho_pasta, pdfs[escolha])
                        ler_pdf_detalhado(caminho)
                    else:
                        print("❌ Escolha inválida!")
                except ValueError:
                    print("❌ Digite um número válido!")
            else:
                print("❌ Nenhum PDF encontrado na pasta")
        else:
            print(f"❌ Pasta não encontrada: {caminho_pasta}")
    
    # Opção para caminho manual
    print(f"\n{'='*50}")
    caminho_manual = input("Ou digite outro caminho completo para um PDF (Enter para sair): ").strip()
    
    if caminho_manual:
        if os.path.exists(caminho_manual):
            ler_pdf_detalhado(caminho_manual)
        else:
            print(f"❌ Arquivo não encontrado: {caminho_manual}")
    
    print("\n✅ Análise concluída!")
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
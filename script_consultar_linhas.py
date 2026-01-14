import pdfplumber
from pathlib import Path


def ler_pdf_linha_por_linha(caminho_pdf):
    """
    Lê um PDF e mostra cada linha numerada
    """
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            print(f"Arquivo: {Path(caminho_pdf).name}")
            print("=" * 60)

            for pagina_num, pagina in enumerate(pdf.pages, 1):
                texto = pagina.extract_text()

                if texto:
                    linhas = texto.split('\n')
                    num_linhas = len(linhas)
                    print(f"\n--- Página {pagina_num} "
                          f"({num_linhas} linhas) ---")

                    for i, linha in enumerate(linhas, 1):
                        # Mostra o número da linha e o conteúdo
                        print(f"linha{i:03d}: {linha}")
                else:
                    print(f"\n--- Página {pagina_num} ---")
                    print("linha001: [SEM TEXTO EXTRAÍVEL]")

    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado - {caminho_pdf}")
    except Exception as e:
        print(f"ERRO: {e}")


# USO DIRETO - APONTE PARA SEU PDF
caminho_do_pdf = r"C:\Dev\Script-ExtratorNomePDF\pdf_teste\seu_arquivo.pdf"
ler_pdf_linha_por_linha(caminho_do_pdf)

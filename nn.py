import spacy
import nltk

nltk.download("punkt_tab")

from goose3 import Goose
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
import en_core_web_sm
import pt_core_news_lg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer

# Instalar pacotes ausentes

# Baixar o modelo de idioma do spaCy
nlp_en = spacy.load("en_core_web_sm")

nlp_pt = spacy.load("pt_core_news_lg")
nltk.download("punkt")

g = Goose()


def idioma(termo, lang=""):
    url = f"https://{lang}.wikipedia.org/wiki/{termo.replace(' ', '_')}"
    article = g.extract(url)
    return article.cleaned_text, article.title


# ainda nao consegui implementar portugues para selecionar sozinho
def processar_texto(texto, lang):
    if lang == "pt":
        nlp = nlp_pt
    else:
        nlp = nlp_en

    doc = nlp(texto)
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]  #
    return " ".join(tokens)


def processar_texto_resumo(texto, lang):
    if lang == "pt":
        nlp = nlp_pt
    else:
        nlp = nlp_en

    doc = nlp(texto)
    tokens = [token.text for token in doc if not token.is_stop]  # and token.is_alpha
    return " ".join(tokens)


# nuvem de palavras
def nuvemPalavras(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras")
    # plt.savefig("nuvem_de_palavras.png")
    plt.tight_layout()
    plt.show()


#   resumo
def resumo(texto_processado_resumo, lang):
    quantidade = int(input("Quantidade de frases que deseja exibir no rensumo: "))
    if lang == "pt":
        parser = PlaintextParser.from_string(
            texto_processado_resumo, Tokenizer("portuguese")
        )
    else:
        parser = PlaintextParser.from_string(
            texto_processado_resumo, Tokenizer("english")
        )

    summarizer = SumBasicSummarizer()
    sumario = summarizer(parser.document, quantidade)

    html_content = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resumo Textual</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
                text-align: center;
            }
            .container {
                max-width: 800px;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                margin: auto;
            }
            h1 {
                color: #333;
            }
            p {
                font-size: 18px;
                color: #555;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Resumo Gerado</h1>
    """
    for sentence in sumario:
        html_content += f"<p>{str(sentence)}</p>"
    html_content += "</div></body></html>"
    with open("resumo.html", "w", encoding="utf-8") as file:
        file.write(html_content)


def menu() -> int:

    print("[1] - Apresentar nuvem de palavras \n")
    print("[2] - Resumo textual \n")
    print("[3] - Pesquisar no por termo \n")
    print("[4] - Sair")
    opcao = int(input("Escolha uma opção: "))
    return opcao


def sub_menu():
    print("[1] - Exibir nuvem")
    print("[2] - Voltar")
    opcao = int(input("Escolha uma opção: "))


def main():
    dados = input("\nEscolha o idioma (en/pt): ")
    termo = input("Digite o verbete da Wikipedia ou a URL da página de interesse: ")
    text, title = idioma(termo, dados)
    texto_processado = processar_texto(text, dados)
    texto_processado_resumo = processar_texto_resumo(text, dados)
    print(f"\nTema escolhido: {title}\n")

    opcao = menu()
    while opcao != 4:
        if opcao == 1:
            nuvemPalavras(texto_processado)

        elif opcao == 2:
            resumo(texto_processado_resumo, dados)

        opcao = menu()

    print("Programa terminado!!")


if __name__ == "__main__":
    main()

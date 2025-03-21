import spacy
import nltk
from goose3 import Goose


# !python -m spacy download pt_core_news_sm
# !python -m spacy download pt_core_news_lg
# import goose
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import en_core_web_sm
import pt_core_news_lg
from spacy.matcher import Matcher
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
import matplotlib.font_manager as fm

# Instalar pacotes ausentes
# Baixar o modelo de idioma do spaCy
nlp_en = spacy.load("en_core_web_sm")

nlp_pt = spacy.load("pt_core_news_lg")
nltk.download("punkt")
font_path = fm.findSystemFonts(fontpaths=None, fontext="ttf")[0]
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = "DejaVu Sans"
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
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


# nuvem de palavras
def nuvemPalavras(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras", fontsize=20, fontweight="bold", pad=20, color="blue")
    # plt.savefig("nuvem_de_palavras.png")
    plt.tight_layout()
    plt.show()


def sumario(texto_processado, dados):
    quantidade = int(
        input("Informe a quantidade de frases que deseja exibir no seu resumo: \n")
    )
    if dados == "pt":
        parser = PlaintextParser.from_string(texto_processado, Tokenizer("portuguese"))
    else:
        parser = PlaintextParser.from_string(texto_processado, Tokenizer("english"))

    summarizer = SumBasicSummarizer()
    sumary = summarizer(parser.document, quantidade)

    resumo_texto = "\n ".join([str(sentence) for sentence in sumary])

    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, resumo_texto, ha="center", va="center", wrap=True)
    plt.axis("off")
    plt.title(
        " ☻ Resumo Textual ☻ ", fontsize=20, fontweight="bold", pad=20, color="blue"
    )
    plt.tight_layout(
        pad=4.0,  # Aumenta o espaço entre os elementos
        w_pad=1.0,  # Ajuste o espaçamento horizontal
        h_pad=2.0,  # Ajuste o espaçamento vertical
        rect=[0.05, 0.1, 0.95, 0.9],  # Ajusta os limites da área de plotagem
    )
    plt.show()

    # for sentence in sumary:
    #     print(sentence)


def buscar(texto_processado, dados):
    termo = input("Digite o termo que deseja buscar no texto: ").strip().lower()

    if dados == "pt":
        nlp = nlp_pt
    else:
        nlp = nlp_en

    doc = nlp(texto_processado)

    matcher = Matcher(nlp.vocab)
    padrao = [{"LOWER": termo}]  # Busca o termo ignorando maiúsculas e minúsculas
    matcher.add("TERMO_BUSCA", [padrao])

    matches = matcher(doc)
    resultados = ""
    if matches:
        print(f"\n🔍 Termo '{termo}' encontrado em:\n")
        for match_id, start, end in matches:
            contexto = doc[
                max(0, start - 5) : min(len(doc), end + 5)
            ]  # Pega 5 palavras antes e depois
            contexto_texto = " ".join([token.text for token in contexto])
            resultados += f"◄ {contexto_texto} ►\n"
            # print(f"... {' '.join([token.text for token in contexto])} ...\n")
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, resultados, fontsize=12, ha="center", va="center", wrap=True)
        plt.axis("off")
        plt.title(
            " ☻ Resultado da Busca ☻",
            fontsize=20,
            fontweight="bold",
            pad=20,
            color="blue",
        )
        plt.tight_layout()
        plt.show()
    else:
        print(f"\n❌ O termo '{termo}' não foi encontrado no texto.")
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, resultados, fontsize=14, ha="center", va="center", wrap=True)
        plt.axis("off")
        plt.title("Resultado da Busca", fontsize=18, pad=20)
        plt.tight_layout()
        plt.show()


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
    print(f"\nTema escolhido: {title}\n")

    opcao = menu()
    while opcao != 4:
        if opcao == 1:
            nuvemPalavras(texto_processado)

        elif opcao == 2:
            sumario(text, dados)
        elif opcao == 3:
            buscar(texto_processado, dados)
        else:
            print("Opção inválida, tente novamente")
        opcao = menu()

    print("Programa terminado!!")


if __name__ == "__main__":
    main()

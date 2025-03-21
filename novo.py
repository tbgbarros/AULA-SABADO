import spacy
import nltk
from goose3 import Goose
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Baixar o modelo de idioma do spaCy
nlp_en = spacy.load("en_core_web_sm")
nlp_pt = spacy.load("pt_core_news_lg")
nltk.download("punkt")

g = Goose()


def idioma(termo, lang=""):
    url = f"https://{lang}.wikipedia.org/wiki/{termo.replace(' ', '_')}"
    article = g.extract(url)
    return article.cleaned_text, article.title


def processar_texto(texto, lang):
    if lang == "pt":
        nlp = nlp_pt
    else:
        nlp = nlp_en

    doc = nlp(texto)
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


def nuvemPalavras(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras")
    plt.tight_layout()
    plt.show()


def menu():
    print("\n[1] - Apresentar nuvem de palavras")
    print("[2] - Resumo textual (não implementado)")
    print("[3] - Pesquisar por termo")
    print("[4] - Sair")

    try:
        return int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida! Digite um número entre 1 e 4.")
        return menu()


def main():
    dados = input("\nEscolha o idioma (en/pt): ").strip().lower()
    if dados not in ["en", "pt"]:
        print("Idioma inválido! Escolha 'en' ou 'pt'.")
        return

    termo = input(
        "Digite o verbete da Wikipedia ou a URL da página de interesse: "
    ).strip()
    text, title = idioma(termo, dados)
    texto_processado = processar_texto(text, dados)

    print(f"\nTema escolhido: {title}\n")

    while True:
        opcao = menu()
        if opcao == 1:
            nuvemPalavras(texto_processado)
        elif opcao == 2:
            print("Função de resumo ainda não implementada.")
        elif opcao == 3:
            termo = input("Digite um novo termo: ")
            text, title = idioma(termo, dados)
            texto_processado = processar_texto(text, dados)
            print(f"\nNovo tema escolhido: {title}\n")
        elif opcao == 4:
            print("Programa terminado!")
            break
        else:
            print("Opção inválida! Escolha entre 1 e 4.")


if __name__ == "__main__":
    main()

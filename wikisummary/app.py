from flask import Flask, render_template, request
import wikipedia
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

app = Flask(__name__)

def summarize_text(text, sentences_count):
    """sumyで文章を要約"""
    parser = PlaintextParser.from_string(text, Tokenizer("japanese"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(sentence) for sentence in summary)

@app.route("/", methods=["GET","POST"])
def index():
    summary3 = summary5 = one_line = " "
    lang = "ja"
    keyword = " "
    if request.method == "POST":
        keyword = request.form["keyword"]
        lang = request.form.get("lang", "ja")

        try:
            wikipedia.set_lang(lang)
            content = wikipedia.page(keyword).content

            summary3 = summarize_text(content, 3)
            summary5 = summarize_text(content, 5)

            parser = PlaintextParser.from_string(content, Tokenizer("japanese"))
            sentences = [str(s) for s in parser.document.sentences]
            one_line = sentences[0][:100] + "..." if sentences else "(本文が短すぎます)"

        except Exception as e:
            summary3 = summary5 = one_line = f"エラー: {e}"

    return render_template(
        "index.html", 
        summary3=summary3,
        summary5=summary5,
        one_line=one_line,
        keyword=keyword,
        lang=lang
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
                
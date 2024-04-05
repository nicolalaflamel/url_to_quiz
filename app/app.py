from flask import Flask, render_template, request
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import urllib.request
from creds import api_key

load_dotenv()


genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/index", methods=["post"])
def process():
    url = request.form["url"]
    html = fetch_html(url)
    text = process_html(html)
    print(text)
    prompt = "次の文章から理解度を図る問題とその回答を３つ作成してください。(例：**問題 1**どのようにFlaskでURLとバインドする関数を関連付けますか？)" + text
    response = model.generate_content(prompt)
    response_array = response.text.split("\n\n")
    question_array = [response_array[0],response_array[2],response_array[4]]
    answer_array = [response_array[1],response_array[3],response_array[5]]
    print(response.text)
    return render_template("index.html",questions = question_array,answers=answer_array)


def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        html = res.read().decode()
    return html

def process_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text


if __name__=="__main__":
    app.run(debug=True)

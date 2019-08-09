from flask import Flask
app = Flask(__name__)

@app.route('/chart/')
def chart():
    HtmlFile = open('chart.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    return source_code

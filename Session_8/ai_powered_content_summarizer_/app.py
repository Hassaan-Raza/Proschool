```python
from flask import Flask, request, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'

# Initialize summarizer model
summarizer = pipeline('summarization')

class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Summarize')

class TextForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Summarize')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            summary = summarizer(text, max_length=100, clean_up_tokenization_spaces=True)
            return render_template('summary.html', summary=summary)
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html', form=form)

@app.route('/text', methods=['GET', 'POST'])
def text_summary():
    form = TextForm()
    if form.validate_on_submit():
        text = form.text.data
        try:
            summary = summarizer(text, max_length=100, clean_up_tokenization_spaces=True)
            return render_template('summary.html', summary=summary)
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('text.html', form=form)

@app.route('/export', methods=['POST'])
def export_summary():
    summary = request.form['summary']
    filename = 'summary.txt'
    with open(filename, 'w') as f:
        f.write(summary)
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Content Summarizer</title>
  </head>
  <body>
    <h1>Content Summarizer</h1>
    <form method="POST">
      {{ form.hidden_tag() }}
      {{ form.url.label }} {{ form.url() }}
      {{ form.submit() }}
    </form>
  </body>
</html>

<!-- templates/text.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Content Summarizer</title>
  </head>
  <body>
    <h1>Content Summarizer</h1>
    <form method="POST">
      {{ form.hidden_tag() }}
      {{ form.text.label }} {{ form.text() }}
      {{ form.submit() }}
    </form>
  </body>
</html>

<!-- templates/summary.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Summary</title>
  </head>
  <body>
    <h1>Summary</h1>
    <p>{{ summary }}</p>
  </body>
</html>

<!-- templates/error.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Error</title>
  </head>
  <body>
    <h1>Error</h1>
    <p>{{ error }}</p>
  </body>
</html>
```
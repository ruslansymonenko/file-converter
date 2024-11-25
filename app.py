from flask import Flask, request, render_template, send_file
import os
import pypandoc

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    file = request.files['file']
    conversion_type = request.form['conversion_type']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    output_path = file_path.replace('.docx', '.pdf')

    if conversion_type == 'word-to-pdf':
        convert_word_to_pdf(file_path, output_path)
    
    return send_file(output_path, as_attachment=True)


def convert_word_to_pdf(input_path, output_path):
    try:
        output = pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
        assert output == ""
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        raise



if __name__ == '__main__':
    app.run(debug=True)
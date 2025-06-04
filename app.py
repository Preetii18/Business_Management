from flask import Flask, request, render_template
import os
from utils.parser import parse_bill_pdf, parse_bill_image

app = Flask(__name__)

# Uploads and config
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def homee():
    return render_template('upload.html')


# Home route — optional redirect to upload
@app.route('/')
def home():
    return render_template('upload.html')

# Upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_bill():
    if request.method == 'POST':
        file = request.files['file']
        bill_type = request.form.get('type')  # "sale" or "purchase"

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parse bill content
        if filename.lower().endswith('.pdf'):
            data = parse_bill_pdf(filepath)
        else:
            data = parse_bill_image(filepath)

        # Show extracted data on same page
        return render_template('upload.html', data=data, bill_type=bill_type)

    # GET method: show form
    return render_template('upload.html')

# Start the server
if __name__ == '__main__':
    app.run(debug=True)


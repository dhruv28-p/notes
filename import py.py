import os
from flask import Flask, request, render_template, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(_name_)

# -------------------- CONFIGURATION --------------------

# TODO: Update with your database connection details (for MySQL or PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<user>:<password>@<server>/<database>'
# Example: 'mysql+pymysql://root:password@localhost/pdf_database'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------- DATABASE MODEL --------------------
db = SQLAlchemy(app)

class PDFFile(db.Model):
    _tablename_ = 'pdf_files'  # TODO: Set your table name
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # TODO: Store PDF name
    data = db.Column(db.LargeBinary, nullable=False)  # TODO: Store PDF file content as binary

# Create the database tables
with app.app_context():
    db.create_all()

# -------------------- ROUTES --------------------

# Upload PDF Route
@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith('.pdf'):  # Ensure it's a PDF
            try:
                # Read file content as binary
                pdf_data = file.read()

                # Save file details in the database
                new_pdf = PDFFile(filename=file.filename, data=pdf_data)
                db.session.add(new_pdf)
                db.session.commit()

                return jsonify({"message": "File uploaded successfully", "filename": file.filename})

            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500

    return render_template('upload.html')

# List All Uploaded PDFs
@app.route('/pdfs', methods=['GET'])
def list_pdfs():
    pdfs = PDFFile.query.all()
    pdf_list = [{"id": pdf.id, "filename": pdf.filename} for pdf in pdfs]
    return jsonify(pdfs=pdf_list)

# Download PDF Route
@app.route('/download/<int:pdf_id>', methods=['GET'])
def download_pdf(pdf_id):
    pdf = PDFFile.query.get_or_404(pdf_id)
    
    # Send the PDF as a downloadable file
    return send_file(BytesIO(pdf.data), mimetype='application/pdf', as_attachment=True, download_name=pdf.filename)

if _name_ == '_main_':
    app.run(debug=True)
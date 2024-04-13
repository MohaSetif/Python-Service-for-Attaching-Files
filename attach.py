#insert two files: first is pdf and others are attachments
#verify the integrity of the sent files using checksums (each file has its own checksum) then return the checksum validity
#test your service
#send and return in json format
#cloud database: in-memory

#no pdf regeneration
#add token for auth
#dockerize it
#add a domain name
#add auto-deploy if possible

#install swagger
#create a log file for flask

#add requirements.txt for your service containing python libs



import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_checksum(file):
    sha256_hash = hashlib.sha256()
    for byte_block in iter(lambda: file.read(4096), b""):
        sha256_hash.update(byte_block)
    checksum = sha256_hash.hexdigest()
    return checksum

@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r') as f:
        html_content = f.read()
    return html_content

@app.route('/attach_files', methods=['GET'])
def attach_index():
    with open('attach_file.html', 'r') as f:
        attach_content = f.read()
    return attach_content

@app.route('/upload', methods=['POST'])
def upload_files():
    main_file = request.files['main_file']
    attachments = request.files.getlist('attachments')
    
    client_main_file_checksum = request.form['main_file_checksum']
    client_attachments_checksums = request.form['attachments_checksums'].split(',')
    
    server_main_file_checksum = calculate_checksum(main_file)
    server_attachments_checksums = [calculate_checksum(attachment) for attachment in attachments]
    
    main_file_checksum_match = client_main_file_checksum == server_main_file_checksum
    attachments_checksums_match = client_attachments_checksums == server_attachments_checksums

    main_file_result = {
        "filename": main_file.filename,
        "checksum": server_main_file_checksum,
        "verification_status": "valid" if main_file_checksum_match else "invalid"
    }

    attachments_results = []
    for attachment, server_checksum, client_checksum in zip(attachments, server_attachments_checksums, client_attachments_checksums):
        attachment_result = {
            "filename": attachment.filename,
            "checksum": server_checksum,
            "verification_status": "valid" if server_checksum == client_checksum else "invalid"
        }
        attachments_results.append(attachment_result)
    
    if main_file_checksum_match and attachments_checksums_match:
        return jsonify({
                        'Main File': main_file_result,
                        'Attachments': attachments_results
                       })
    else:
        return jsonify({'error': 'Checksum verification failed for main file or attachments!'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("3000"), debug=True)

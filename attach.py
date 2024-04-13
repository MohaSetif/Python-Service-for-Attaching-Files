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
    
    if main_file_checksum_match and attachments_checksums_match:
        return jsonify({'message': 'Checksum verification passed for main file and attachments!',
                        'Client Main check': client_main_file_checksum,
                        'Server Main check': server_main_file_checksum,
                        'Client Attachments check': client_attachments_checksums,
                        'Server Attachments: check': server_attachments_checksums,
                       })
    else:
        return jsonify({'error': 'Checksum verification failed for main file or attachments!',
                        'Client Main check': client_main_file_checksum,
                        'Server Main check': server_main_file_checksum,
                        'Client Attachments check': client_attachments_checksums,
                        'Server Attachments: check': server_attachments_checksums,
                       })

if __name__ == '__main__':
    app.run(debug=True)

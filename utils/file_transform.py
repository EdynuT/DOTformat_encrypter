import os

def combine_dotf_files(input_folder, output_file):
    index_file = os.path.join(os.path.dirname(output_file), 'index.txt')
    with open(index_file, 'w') as index:
        with open(output_file, 'wb') as outfile:
            for root, _, files in os.walk(input_folder):
                for file in files:
                    if file.endswith('.dotf'):
                        file_path = os.path.join(root, file)
                        if not os.path.commonprefix([os.path.realpath(file_path), os.path.realpath(input_folder)]) == os.path.realpath(input_folder):
                            continue
                        with open(file_path, 'rb') as infile:
                            data = infile.read()
                            outfile.write(len(data).to_bytes(4, 'big'))
                            outfile.write(file.encode('utf-8'))
                            outfile.write(b'\0')
                            outfile.write(data)
                        index.write(f"{file}\t{os.path.basename(file_path)}\n")

def split_dotf_file(input_file, output_folder):
    index_file = os.path.join(os.path.dirname(input_file), 'index.txt')
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"Index file not found: {index_file}")
    
    with open(index_file, 'r') as index:
        index_data = {line.split('\t')[0]: line.split('\t')[1].strip() for line in index.readlines()}
    
    with open(input_file, 'rb') as infile:
        while True:
            size_data = infile.read(4)
            if not size_data:
                break
            size = int.from_bytes(size_data, 'big')
            filename = b''
            while True:
                char = infile.read(1)
                if char == b'\0':
                    break
                filename += char
            filename = filename.decode('utf-8')
            data = infile.read(size)
            original_filename = index_data.get(filename, filename)
            output_path = os.path.join(output_folder, original_filename)
            if not os.path.commonprefix([os.path.realpath(output_path), os.path.realpath(output_folder)]) == os.path.realpath(output_folder):
                continue
            with open(output_path, 'wb') as outfile:
                outfile.write(data)
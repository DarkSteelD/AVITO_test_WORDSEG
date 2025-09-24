import pandas as pd
import os

def process_corpus(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sentences = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            sentence_with_spaces = line.strip()
            if sentence_with_spaces:
                sentence_without_spaces = sentence_with_spaces.replace(' ', '')
                sentences.append({
                    'id': i,
                    'sentence_with_spaces': sentence_with_spaces,
                    'sentence_without_spaces': sentence_without_spaces
                })

    if sentences:
        df = pd.DataFrame(sentences)
        output_file = os.path.join(output_dir, 'processed_corpus.parquet')
        df.to_parquet(output_file, index=False)
        print(f"Successfully created {output_file}")

if __name__ == '__main__':
    input_path = 'data/external_sentences_corpus.txt'
    output_path = 'data/proccesed_data'
    process_corpus(input_path, output_path) 

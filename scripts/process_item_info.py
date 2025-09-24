import pandas as pd
import os
import re
from tqdm import tqdm

def split_into_sentences(text):
    if not isinstance(text, str):
        return []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def process_item_info(input_csv_path, output_dir, output_filename):
    try:
        df = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    all_sentences = []
    sentence_id = 0

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing items"):
        title = row.get('title', '')
        description = row.get('description', '')

        title_sentences = split_into_sentences(title)
        desc_sentences = split_into_sentences(description)

        for sentence in title_sentences + desc_sentences:
            all_sentences.append({
                'id': sentence_id,
                'sentence_with_spaces': sentence,
                'sentence_without_spaces': sentence.replace(' ', '')
            })
            sentence_id += 1

    if all_sentences:
        output_df = pd.DataFrame(all_sentences)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, output_filename)
        output_df.to_parquet(output_file, index=False)
        print(f"Successfully created {output_file} with {len(output_df)} sentences.")
    else:
        print("No sentences were extracted from the item info file.")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process ItemInfo CSV and create a parquet file with sentences.')
    parser.add_argument('input_file', type=str, help='Path to the input ItemInfo CSV file.')
    args = parser.parse_args()

    output_path = 'data/proccesed_data'
    output_filename = os.path.splitext(os.path.basename(args.input_file))[0].replace('Info', '_info') + '.parquet'
    
    # Correcting the output filename generation
    if 'test' in args.input_file.lower():
        output_filename = 'item_info_test.parquet'
    elif 'train' in args.input_file.lower():
        output_filename = 'item_info_train.parquet'
    else:
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_filename = f"{base_name}_sentences.parquet"


    process_item_info(args.input_file, output_path, output_filename) 

import pandas as pd
import os
import re

def process_subtitles(metatable_path, subtitles_dir, output_dir):
    try:
        meta_df = pd.read_csv(metatable_path, sep='\t', on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading metatable: {e}")
        meta_df = pd.read_csv(metatable_path, sep=r'\s{2,}', engine='python', on_bad_lines='skip', names=['id', 'title', 'languages', 'filepath'])
    if 'id' not in meta_df.columns and meta_df.shape[1] == 4:
        meta_df.columns = ['id', 'title', 'languages', 'filepath']
    meta_df.dropna(subset=['languages', 'filepath'], inplace=True)

    ru_subtitles = meta_df[meta_df['languages'].str.strip() == 'ru']

    all_sentences = []
    sentence_id = 0

    for index, row in ru_subtitles.iterrows():
        try:
            series_name_match = re.match(r'^(.*?) - \d+x\d+', row['title'])
            if not series_name_match:
                series_name_match = re.match(r'^(.*?) - \d{4}', row['title']) # for movies with year
            if not series_name_match:
                 series_name_match = re.match(r'^(.*?) - [a-zA-Z]', row['title'])
            
            if series_name_match:
                series_name = series_name_match.group(1).strip()
            else:
                series_name = row['title'].split(' - ')[0].strip()

            filename = row['title'].replace('.srt', '.txt')
            
            filepath = os.path.join(subtitles_dir, 'texts', series_name, filename)

            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        if len(parts) >= 4:
                            sentence = " ".join(parts[3:])
                            if sentence:
                                all_sentences.append({
                                    'id': sentence_id,
                                    'sentence_with_spaces': sentence,
                                    'sentence_without_spaces': sentence.replace(' ', '')
                                })
                                sentence_id += 1
        except Exception as e:
            continue

    if all_sentences:
        df = pd.DataFrame(all_sentences)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, 'pesni.parquet')
        df.to_parquet(output_file, index=False)
        print(f"Successfully created {output_file} with {len(df)} sentences.")
    else:
        print("No Russian sentences found or processed.")


if __name__ == '__main__':
    metatable_path = 'data/Subtitles/metatable.csv'
    subtitles_base_dir = 'data/Subtitles'
    output_path = 'data/proccesed_data'
    process_subtitles(metatable_path, subtitles_base_dir, output_path) 

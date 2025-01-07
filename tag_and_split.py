import random

en_data = 'Final Project/Data/raw/en.txt'
hy_data = 'Final Project/Data/raw/hy.txt'
source_destination = 'Final Project/Data/source/'
target_destination = 'Final Project/Data/target/'

with open(en_data, 'r') as en, open(hy_data, 'r') as hy:
    en_lines = en.readlines()
    tagged_en_lines = ['<hy> '+line for line in en_lines]
    hy_lines = hy.readlines()
    tagged_hy_lines = ['<en> '+line for line in hy_lines]

source = list(zip(tagged_en_lines, ['<BOS> ' + hy_line.strip('\n') + '<EOS> \n' for hy_line in hy_lines]))
target = list(zip(tagged_hy_lines, ['<BOS> ' + en_line.strip('\n') + '<EOS> \n' for en_line in en_lines]))

# Create test sets by shuffling the source and target 
random.shuffle(source)
random.shuffle(target)
# Subset the source and target data to create non-shuffled test splits
source_subset, source = source[:500], source[500:]
target_subset, target = target[:500], target[500:]
en2hy, hy = zip(*source_subset)
hy2en, en = zip(*target_subset)

# Combine the source and target data to make the validation and training splits 
combo = source + target
random.shuffle(combo)
source_val, target_val = zip(*combo[:1000])
source_train, target_train = zip(*combo[1000:16000])

files_to_write = [
    # Training sets
    {"content": source_train,   "folder": source_destination,   "filename": "source_train.txt"},
    {"content": target_train,   "folder": target_destination,   "filename": "target_train.txt"},

    # Validation sets
    {"content": source_val,     "folder": source_destination,   "filename": "source_val.txt"},
    {"content": target_val,     "folder": target_destination,   "filename": "target_val.txt"},

    # Test sets
    {"content": en2hy,          "folder": source_destination,   "filename": "en2hy_test.txt"},
    {"content": hy,             "folder": target_destination,   "filename": "hy_test.txt"},

    {"content": hy2en,          "folder": source_destination,   "filename": "hy2en_test.txt"},
    {"content": en,             "folder": target_destination,   "filename": "en_test.txt"},
]

for file in files_to_write:
    with open(f"{file["folder"]}{file["filename"]}", 'w') as f:
        f.writelines(file["content"])
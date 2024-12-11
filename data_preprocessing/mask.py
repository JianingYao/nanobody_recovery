import pandas as pd
import random

# load the dataset
merged_dataset = pd.read_csv("merged_dataset.csv")

def mask_sequence(sequence, mask_token="[MASK]", mask_ratio=0.15):
    """
    Apply BERT-style masking to an amino acid sequence.
    
    Parameters:
    - sequence (str): The input amino acid sequence.
    - mask_token (str): Token used for masking (default: "[MASK]").
    - mask_ratio (float): Fraction of amino acids to mask (default: 0.15).
    
    Returns:
    - masked_sequence (str): The masked sequence.
    - label_sequence (str): The original sequence with non-masked positions as "-"
    """
    amino_acids = "ACDEFGHIKLMNPQRSTVWY"
    seq_length = len(sequence)
    num_to_mask = max(1, int(seq_length * mask_ratio))  # At least 1 position
    mask_positions = random.sample(range(seq_length), num_to_mask)
    
    masked_sequence = list(sequence)
    label_sequence = ["-"] * seq_length
    
    for pos in mask_positions:
        original_aa = sequence[pos]
        rand_prob = random.random()
        
        if rand_prob < 0.8:
            masked_sequence[pos] = mask_token
        elif rand_prob < 0.9:
            random_aa = random.choice([aa for aa in amino_acids if aa != original_aa])
            masked_sequence[pos] = random_aa
        else:
            masked_sequence[pos] = original_aa
        
        label_sequence[pos] = original_aa
    
    return "".join(masked_sequence), "".join(label_sequence)

# Create a list of store mask results
masked_data = []

# Mask through each sequence
for _, row in merged_dataset.iterrows():
    seq_id = row["SequenceID"]
    sequence = row["sequence"]
    dataset = row["Dataset"]  # train/val/test
    
    # Apply mask rules to sequences
    masked_seq, label_seq = mask_sequence(sequence)
    
    # Save
    masked_data.append({
        "Dataset": dataset,
        "SequenceID": seq_id,
        "OriginalSequence": sequence,
        "MaskedSequence": masked_seq,
        "LabelSequence": label_seq
    })

# Convert to DataFrame
masked_df = pd.DataFrame(masked_data)

# print(masked_df.head())

# Save by data label
for dataset_type in ["train", "val", "test"]:
    subset = masked_df[masked_df["Dataset"] == dataset_type]
    subset.to_csv(f"{dataset_type}_masked_dataset.csv", index=False)
    print(f"{dataset_type}_masked_dataset.csv saved with {len(subset)} sequences.")
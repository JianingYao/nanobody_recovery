import csv

input_csv = "all_sequences.csv"

output_fasta = "all_sequences.fasta"

with open(input_csv, "r") as csv_file, open(output_fasta, "w") as fasta_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:

        seq_id = row["ID"]
        sequence = row["sequence"]

        fasta_file.write(f">{seq_id}\n{sequence}\n")

print(f"FASTA file saved to {output_fasta}")
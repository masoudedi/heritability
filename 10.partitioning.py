import pandas as pd 
import sys

input_file = sys.argv[1]

df = pd.read_csv(input_file, skiprows=1, sep=' ', names=['SNP','chr', 'bp', 'freq', 'mean_rsq', 'snp_num', 'max_rsq', 'ldscore_SNP', 'ldscore_region'], usecols=['SNP', 'ldscore_SNP', 'ldscore_region'])

# Calculate mean
median_snp = df['ldscore_SNP'].median()

# Calculate median
median_region = df['ldscore_region'].median()
def select_high_ld(row, median_snp, median_region):
    if row['ldscore_SNP'] > median_snp:
        return True 
    elif row['ldscore_region'] > median_region:
        return True 
    return False 
df['is_high_ld'] = df.apply(select_high_ld, axis=1, args=(median_snp, median_region))

# Select rows where 'is_high_ld' is True
high_ld_df = df[df['is_high_ld'] == True]
high_ld_df.iloc[:, 0].to_csv(f"{input_file}.high_ld.txt", index=False, header=False)
#
low_ld_df = df[df['is_high_ld'] == False]
low_ld_df.iloc[:, 0].to_csv(f"{input_file}.low_ld.txt", index=False, header=False)

print("median_snp:", median_snp)
print("median_region:", median_region)
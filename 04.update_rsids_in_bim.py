import pysam

# Original chromosome mapping
chrom_mapping = {
    "NC_000001.10": "1",
    "NC_000002.11": "2",
    "NC_000003.11": "3",
    "NC_000004.11": "4",
    "NC_000005.9": "5",
    "NC_000006.11": "6",
    "NC_000007.13": "7",
    "NC_000008.10": "8",
    "NC_000009.11": "9",
    "NC_000010.10": "10",
    "NC_000011.9": "11",
    "NC_000012.11": "12",
    "NC_000013.10": "13",
    "NC_000014.8": "14",
    "NC_000015.9": "15",
    "NC_000016.9": "16",
    "NC_000017.10": "17",
    "NC_000018.9": "18",
    "NC_000019.9": "19",
    "NC_000020.10": "20",
    "NC_000021.8": "21",
    "NC_000022.10": "22",
    "NC_000023.10": "X",
    "NC_000024.9": "Y"
}

# Reverse the dictionary
reversed_chrom_mapping = {v: k for k, v in chrom_mapping.items()}

def convert_chromosome(chromosome):
    """
    Convert the chromosome from number/letter to NC notation.

    Parameters:
    chromosome (str): Chromosome number or letter (e.g., '1', 'X').

    Returns:
    str: Chromosome in NC notation (e.g., 'NC_000001.10').
    """
    return reversed_chrom_mapping.get(chromosome, chromosome)

def get_variant_info(vcf_file, chromosome, position, ref, alt):
    """
    Retrieve variant information from a VCF file for a specific genomic location.

    Parameters:
    vcf_file (str): Path to the VCF file.
    chromosome (str): Chromosome of interest.
    position (int): Position on the chromosome.

    Returns:
    list: A list of variant records at the specified location.
    """
    variants = []
    # Convert chromosome to NC notation if needed
    nc_chromosome = convert_chromosome(chromosome)

    # Open the VCF file
    vcf = pysam.VariantFile(vcf_file)
    
    # Fetch variants at the specific location
    for record in vcf.fetch(nc_chromosome, position-1, position):
        if record.pos == position:
            #IF the variant is indel, need to check the ref and alt to make sure that's realy variant
            if record.alts:
                if any(len(alt) > 1 for alt in record.alts) or len(record.ref) > 1:
                    if alt in record.alts and ref == record.ref:
                        variants.append(record.id)
                else:
                    variants.append(record.id)

    # Close the VCF file
    vcf.close()
    return variants[0] if variants else None

# Example usage:
vcf_file = '/home/edizadehm/03.resources/01.dbsnp/GCF_000001405.25.gz'
chrom = '22' 
bim_file = f"/home/edizadehm/02.tutorials/07.gcta/SCZ_CC_data/SCZ_CC_autosomes.{chrom}.bim"
output_bim = f"/home/edizadehm/02.tutorials/07.gcta/SCZ_CC_data/SCZ_CC_autosomes.converted.{chrom}.bim"

out = open(output_bim, 'w')
T = open(bim_file)

for line in T:
    line = line.strip().split()
    chromosome = line[0]
    position = line[3]
    ref, alt = line[4], line[5]
    variant_info = get_variant_info(vcf_file, str(chromosome), int(position), ref, alt)
    if variant_info:
        line[1] = variant_info
    out.write('\t'.join(line) + "\n")
out.close()
T.close()


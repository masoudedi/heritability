import pysam
import pybgen
from bgen import BgenWriter


def vcf_to_bgen(vcf_file, bgen_file):
    # Open the VCF file
    vcf = pysam.VariantFile(vcf_file, "r")
    
    # Prepare BGEN writer
    
    bgen = BgenWriter(bgen_file, n_samples=0)  # n_samples will be updated later
    
    # Collect sample information
    samples = vcf.header.samples
    n_samples = len(samples)
    bgen.n_samples = n_samples
    
    # Initialize BGEN file with sample and variant information
    for sample in samples:
        bgen.add_sample(sample)

    for rec in vcf.fetch():
        # Extract genotype probabilities (GP field assumed to be in the VCF file)
        genotypes_prob = rec.samples[samples[0]].get('GP', [])
        
        # Convert to genotype probabilities format
        # Assuming GP contains probabilities for 0/0, 0/1, 1/1
        probs = [0.0, 0.0, 0.0]  # Default probabilities
        
        if genotypes_prob:
            try:
                probs = [float(prob) for prob in genotypes_prob]
            except ValueError:
                # Handle any conversion errors
                print(f"Warning: Invalid genotype probabilities for variant {rec.chrom}:{rec.pos}")
                continue
        
        # Ensure the probabilities sum to 1
        prob_sum = sum(probs)
        if prob_sum > 0:
            probs = [p / prob_sum for p in probs]
        
        # Write to BGEN
        bgen.add_variant(rec.chrom, rec.pos, rec.id, probs)

    # Finalize BGEN file
    bgen.close()

# Usage example
vcf_file = "/home/edizadehm/03.resources/03.SCZ_CC/02.original_SCZ_CC_data/genos/chr22.dose.vcf"
bgen_file = "/home/edizadehm/03.resources/03.SCZ_CC/02.original_SCZ_CC_data/genos/chr22.dose.file.bgen"
vcf_to_bgen(vcf_file, bgen_file)

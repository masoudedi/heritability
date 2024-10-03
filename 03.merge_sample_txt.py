import pandas as pd 

def splitter(value):
    if '.' in value:
        value = value.split(".")[0]
    if "Affy" in value:
        value = value.split("_Affy")[0]
    if "Broad" in value:
        value = value.split("_Broad")[0]
    if "_VB_" in value:
        value = value.split("_VB_")[0]
    return value

for chrom in range(1,23):
    f = "/home/edizadehm/04.cases_information/01.updated_SCZ_CC_inforamtion.txt"
    f2 = f'/home/projects/IrishGWAS/SCZ_CC/Post_all_QC/HRC_version_r.1.1/genos/HRC.r.1.1.chr{chrom}.samples'
    out = f'/home/edizadehm/03.resources/03.SCZ_CC/02.original_SCZ_CC_data/genos/chr{chrom}.sample'
    df = pd.read_csv(f, sep='\t', names=['one', 'six1'], dtype=str)
    df = df.drop_duplicates(subset='one')

    df2 = pd.read_csv(f2, sep=' ', skiprows=1 ,names=['one', 'two', 'three'])
    df2['four'] = '0'
    df2['five'] = '0'

    df2['one'] = df2['one'].apply(splitter)
    df2['two'] = df2['two'].apply(splitter)

    final = pd.merge(df2, df, on='one', how='left')
    print(df2.shape)
    print(final.shape)

    ###geno sample format
    # .sample (Oxford sample information file)
    # Sample information file accompanying a .gen genotype dosage file. Loaded with --data/--sample, and produced by "--recode oxford".

    # The .sample space-delimited files emitted by --recode have two header lines, and then one line per sample with 3-5 relevant fields:

    # First header line	Second header line	Subsequent contents
    # ID_1	0	Family ID
    # ID_2	0	Within-family ID
    # missing	0	Missing call frequency
    # sex	D	Sex code ('1' = male, '2' = female, '0' = unknown)
    # phenotype	'B'/'P'	Binary ('0' = control, '1' = case) or continuous phenotype
    #B for binary variable and P for continous variable
    # A specification for this format is on the QCTOOL v2 website.

    #set category
    def set_pheno(value):
        if value in ['2', 2]:
            return 'case'
        elif value in ['1', 1]:
            return 'control'
        elif value in ['3', 3]:
            return 'NA'
        elif value in ['5', 5]:
            return 'NA'
        else:
            return 'NA'
    final['six1'] = final['six1'].apply(set_pheno)
    final.drop(['five'], axis=1, inplace=True)

    final.columns = ['ID_1', 'ID_2', 'missing', 'sex', 'phenotype']
    final.loc[0] = ['0', '0', '0', 'D', 'B']
    final.to_csv(out, index=False, header=True, sep=' ')





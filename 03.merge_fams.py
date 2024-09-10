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

f = "/home/edizadehm/04.cases_information/01.updated_SCZ_CC_inforamtion.txt"
f2 = "/home/edizadehm/03.resources/03.SCZ_CC/SCZ_CC_autosomes.fam"

df = pd.read_csv(f, sep='\t', names=['one', 'six1'], dtype=str)
df = df.drop_duplicates(subset='one')

df2 = pd.read_csv(f2, sep=' ', names=['one', 'two', 'three', 'four', 'five', 'six'])

df2['one'] = df2['one'].apply(splitter)
df2['two'] = df2['two'].apply(splitter)

final = pd.merge(df2, df, on='one', how='left')
print(df2.shape)
print(final.shape)

#set category
def set_pheno(value):
    if value in ['2', 2]:
        return '2'
    elif value in ['1', 1]:
        return '1'
    elif value in ['3', 3]:
        return '3'
    elif value in ['5', 5]:
        return '5'
    else:
        return '0'
final['six1'] = final['six1'].apply(set_pheno)
final.drop(['six'], axis=1, inplace=True)
final.to_csv("Final_SCZ_CC.fam", index=False, header=False, sep=' ')
print(final.head)



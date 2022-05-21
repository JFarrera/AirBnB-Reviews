import sys
import argparse
import pandas as pd 

attributes_list = ['@RELATION overallSatisfaction','',
'@ATTRIBUTE roomType {PrivateRoom,EntireHome,SharedRoom}',
'@ATTRIBUTE neighborhood {LesCorts,SantsMontjuic,CiutatVella,SantMarti,Gracia,Horta,Sarria,Eixample,SantAndreu,NouBarris}',
'@ATTRIBUTE reviews ','@ATTRIBUTE overallSatisfaction {1,2,3,4,5,6,7,8,9}',
'@ATTRIBUTE accommodates ','@ATTRIBUTE bedrooms ',
'@ATTRIBUTE price ','@ATTRIBUTE latitude ','@ATTRIBUTE longitude ','','@DATA']



def data_managment(filename):
    df_raw = pd.read_csv(filename)
    df1 = df_raw.replace(["Shared room","Entire home/apt","Private room","Les Corts","Sant Andreu","Nou Barris",
    "Sants-Montjuïc","Ciutat Vella","Sant Martí","Gràcia","Horta-Guinardó","Sarrià-Sant Gervasi"],
    ["SharedRoom","EntireHome","PrivateRoom","LesCorts","SantAndreu","NouBarris",
    "SantsMontjuic","CiutatVella","SantMarti","Gracia","Horta","Sarria"])

    df1 = convert_decimal_to_int(df1)
    df1 = convert_type_to_str(['reviews', 'accommodates'], df1)
    return df1

def convert_type_to_str(columns, dataframe):
    for column in columns:
        dataframe[column] = dataframe[column].astype(str)

    attributes_list[4]+='{'+','.join(x for x in list(map(str.strip,dataframe.reviews.unique())))+'}'
    attributes_list[6]+='{'+','.join(x for x in list(map(str.strip,dataframe.accommodates.unique())))+'}'
    return dataframe


def convert_decimal_to_int(dataframe):
    dataframe = dataframe.replace([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9])
    dataframe['overall_satisfaction'] = dataframe['overall_satisfaction'].astype(int)
    return dataframe



def main(argv=None):
    args = parse_command_line_arguments(argv)
    dataset = data_managment(args.dataset)
    return dataset.isna().sum()


def parse_command_line_arguments(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset', help='path to the dataset')
    parser.add_argument('train', help='file name for training')
    parser.add_argument('test', help='file name for testing')
    return parser.parse_args(args=argv)

if __name__ == "__main__":
    sys.exit(main())
    
import sys
import argparse
import pandas as pd

attributes_list = ['@RELATION overallSatisfaction','',
'@ATTRIBUTE roomType {PrivateRoom,EntireHome,SharedRoom}',
'@ATTRIBUTE neighborhood {LesCorts,SantsMontjuic,CiutatVella,SantMarti,Gracia,Horta,Sarria,Eixample,SantAndreu,NouBarris}',
'@ATTRIBUTE reviews ','@ATTRIBUTE overallSatisfaction {1,2,3,4,5,6,7,8,9}',
'@ATTRIBUTE accommodates ','@ATTRIBUTE bedrooms ',
'@ATTRIBUTE price ','@ATTRIBUTE latitude ','@ATTRIBUTE longitude ','','@DATA']



def write_headers(file):
    for atr in attributes_list:
        file.write(atr+'\n')

def write_to_file(arff_file,files):
    with open(files, 'w') as file:
        write_headers(file)
        for _,row in arff_file.iterrows():
            for pos,value_col in enumerate(row):
                file.write(str(value_col))
                if pos != len(row)-1:
                    file.write(',')
            file.write('\n')
    file.close()


def data_managment(filename):
    df_raw = pd.read_csv(filename)
    df1 = df_raw.replace(["Shared room","Entire home/apt","Private room","Les Corts","Sant Andreu","Nou Barris",
    "Sants-Montjuïc","Ciutat Vella","Sant Martí","Gràcia","Horta-Guinardó","Sarrià-Sant Gervasi"],
    ["SharedRoom","EntireHome","PrivateRoom","LesCorts","SantAndreu","NouBarris",
    "SantsMontjuic","CiutatVella","SantMarti","Gracia","Horta","Sarria"])

    df1 = convert_decimal_to_int('overall_satisfaction', df1)
    df1 = convert_type_to_str('reviews', 4, df1)
    df1 = convert_type_to_str('accommodates', 6, df1)
    df1 = convert_type_to_str('bedrooms', 7, df1)
    df1 = convert_type_to_str('price', 8, df1)

    df1 = convert_to_quantile('latitude', 9, df1)
    df1 = convert_to_quantile('longitude', 10, df1)

    return df1

def convert_to_quantile(column: str, n_col:int, dataframe):
    dataframe[column] = pd.qcut(dataframe[column], 5, labels=False)
    dataframe[column] = dataframe[column].astype(str)
    attributes_list[n_col]+='{'+','.join(x for x in list(map(str.strip,dataframe[column].unique())))+'}'
    return dataframe


def convert_type_to_str(column: str, n_col: int, dataframe):
    if not isinstance(dataframe[column], int):
        dataframe[column] = dataframe[column].astype(int)
    dataframe[column] = dataframe[column].astype(str)
    attributes_list[n_col]+='{'+','.join(x for x in list(map(str.strip,dataframe[column].unique())))+'}'
    return dataframe

def convert_decimal_to_int(column: str, dataframe):
    dataframe = dataframe.replace([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                                [1, 2, 3, 4, 5, 6, 7, 8, 9])
    dataframe[column] = dataframe[column].astype(int)
    return dataframe



def main(argv=None):
    args = parse_command_line_arguments(argv)
    dataset = data_managment(args.dataset)
    train_set = dataset.sample(frac=args.percentage, random_state=args.seed)
    test_set = dataset.drop(train_set.index)

    write_to_file(train_set,args.train)
    write_to_file(test_set,args.test)


def parse_command_line_arguments(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset', help='path to the dataset')
    parser.add_argument('train', help='file name for training')
    parser.add_argument('test', help='file name for testing')
    parser.add_argument("seed",nargs="?",default=80617,type=int,help="Seed for the random test-train split")
    parser.add_argument("percentage",nargs="?",default=0.75,type=float,help="Percentage of the training set range 0-1")
    return parser.parse_args(args=argv)

if __name__ == "__main__":
    sys.exit(main())
    
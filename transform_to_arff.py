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
    """
    Copy the attributes_list array to the train.arff and test.arff files

    :param file: the file location of train or test files
    :return:
    """
    for atr in attributes_list:
        file.write(atr+'\n')

def write_to_file(dataframe, files):
    """
    Copy the attributes_list array and the dataframe for the train or test files

    :param df: dataframe
    :param files: file location of train or test files
    :return:
    """
    with open(files, 'w') as file:
        write_headers(file)
        for _,row in dataframe.iterrows():
            for pos,value_col in enumerate(row):
                file.write(str(value_col))
                if pos != len(row)-1:
                    file.write(',')
            file.write('\n')
    file.close()

def data_preparation(filename):
    """
    Data preparation for the dataset

    :param filename: file location of the .csv file
    :return: returns dataframe
    """
    df_raw = pd.read_csv(filename)
    df1 = df_raw.replace(["Shared room","Entire home/apt","Private room","Les Corts","Sant Andreu","Nou Barris",
    "Sants-Montjuïc","Ciutat Vella","Sant Martí","Gràcia","Horta-Guinardó","Sarrià-Sant Gervasi"],
    ["SharedRoom","EntireHome","PrivateRoom","LesCorts","SantAndreu","NouBarris",
    "SantsMontjuic","CiutatVella","SantMarti","Gracia","Horta","Sarria"])

    df1 = mapping_objective_col('overall_satisfaction', df1)
    df1 = convert_type_to_str('accommodates', 6, df1)
    df1 = convert_type_to_str('bedrooms', 7, df1)    
    df1 = convert_to_discrete('reviews', 4, df1, 15)
    df1 = convert_to_discrete('price', 8, df1, 15)
    df1 = convert_to_discrete('latitude', 9, df1, 15)
    df1 = convert_to_discrete('longitude', 10, df1, 15)
    return df1

def convert_to_discrete(column: str, n_col: int, dataframe, divisions: int):
    """
    Convert the dataframe values to discrete

    :param column: column name
    :param n_col: column number
    :param dataframe: dataframe
    :param divisions: length of the set range of divisions
    :return: returns dataframe
    """
    dataframe[column] = pd.cut(dataframe[column], divisions, labels=False)
    dataframe[column] = dataframe[column].astype(str)
    attributes_list[n_col]+='{'+','.join(x for x in list(map(str.strip,dataframe[column].unique())))+'}'
    return dataframe

def convert_type_to_str(column: str, n_col: int, dataframe):
    """
    Convert the type of the dataframe values to string

    :param column: column name
    :param n_col: column number
    :param dataframe: dataframe
    :return: returns dataframe
    """
    if not isinstance(dataframe[column], int):
        dataframe[column] = dataframe[column].astype(int)
    dataframe[column] = dataframe[column].astype(str)
    attributes_list[n_col]+='{'+','.join(x for x in list(map(str.strip,dataframe[column].unique())))+'}'
    return dataframe

def mapping_objective_col(column: str, dataframe):
    """
    Convert the objective column values to discrete

    :param column: column name
    :param dataframe: dataframe
    :return: returns dataframe
    """
    dataframe = dataframe.replace([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                                [1, 2, 3, 4, 5, 6, 7, 8, 9])
    dataframe[column] = dataframe[column].astype(int)
    return dataframe

def parse_command_line_arguments(argv=None):
    """
    Read and parse command line arguments

    :param argv: command line arguments, default None
    :return: returns the parser
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dataset', help='path to the dataset')
    parser.add_argument('train', help='file name for training')
    parser.add_argument('test', help='file name for testing')
    parser.add_argument("seed",nargs="?",default=80617,type=int,help="Seed for the random test-train split")
    parser.add_argument("percentage",nargs="?",default=0.75,type=float,help="Percentage of the training set range 0-1")
    return parser.parse_args(args=argv)

def main(argv=None):
    """
    Main function of the program

    :param argv: command line arguments, default None
    :return:
    """
    args = parse_command_line_arguments(argv)
    dataset = data_preparation(args.dataset)
    train_set = dataset.sample(frac=args.percentage, random_state=args.seed)
    test_set = dataset.drop(train_set.index)

    write_to_file(train_set,args.train)
    write_to_file(test_set,args.test)

if __name__ == "__main__":
    sys.exit(main())
    
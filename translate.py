"""
Sci-Translator

This simple script in Python3 helps students to translate files with
.asc, .Spectrum extensions to CSV files

It will read all files with the above extensions, in the specified folder
and convert them to CSV files as output.<extension>.csv
"""

import glob, sys, csv, os

def read_spectrum(file):
    list = []
    list.append([os.path.splitext(os.path.basename(file))[0]])

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            data = line.rstrip().split('\t')
            if (len(data) < 2):
                continue
            list.append([data[1].strip()])
    return list

def read_asc(file):
    list = []
    list.append([os.path.splitext(os.path.basename(file))[0]])

    with open(file) as f:
        lines = f.readlines()
        can_append = False
        for line in lines:
            if ("#DATA" in line):
                can_append = True
                continue
            if (can_append):
                data = line.rstrip().split('\t')
                if (len(data) < 2):
                    continue
                list.append([data[1].strip()])
    return list

def get_asc_files(path):
    return glob.glob("{}/*.asc".format(path))

def get_spectrum_files(path):
    return glob.glob("{}/*.Spectrum".format(path))

def merge(data, file_data):
    for index, line in enumerate(file_data):
        data[index] = data[index] + line
    return data

def write_file(output, data):
    with open(output, mode='w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)

def process_spectrum(folder):
    output = "output.spectrum.csv"
    print("Reading .Spectrum files from '{}'\n".format(folder))
    files = get_spectrum_files(folder)
    files.sort()

    data = []
    for file in files:
        print("Processing file '{}'".format(file))
        file_data = read_spectrum(file)
        print("Found {} lines in file".format(len(file_data)))
        if (len(data) == 0):
            data = file_data
        else:
            data = merge(data, file_data)
        print()

    write_file(output, data)
    print("Done processing {} files to output.spectrum.csv".format(len(files)))

def process_asc(folder):
    output = "output.asc.csv"
    print("Reading .asc files from '{}'\n".format(folder))
    files = get_asc_files(folder)
    files.sort()

    data = []
    for file in files:
        print("Processing file '{}'".format(file))
        file_data = read_asc(file)
        print("Found {} lines in file".format(len(file_data)))
        if (len(data) == 0):
            data = file_data
        else:
            data = merge(data, file_data)
        print()

    write_file(output, data)
    print("Done processing {} files to output.asc.csv".format(len(files)))

if __name__ == "__main__":
    folder = sys.argv[1]

    process_spectrum(folder)
    print()
    process_asc(folder)

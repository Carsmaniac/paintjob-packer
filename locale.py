import csv, os

locale_dict = {}

for locale_file in os.listdir("locale"):
    if locale_file[-3:] == "csv":
        with open("locale/"+locale_file, "r", encoding="utf-8") as file:
            csv_file = csv.reader(file, delimiter=",", quotechar = "\"")
            for line in csv_file:
                if line[0] not in ["context", "source"]:
                    if line[0] not in locale_dict:
                        locale_dict[line[0]] = []
                    locale_dict[line[0]].append(line[1])

with open("locale.csv", "w", encoding="utf-8") as file:
    csv_file = csv.writer(file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
    for key in locale_dict:
        csv_file.writerow([key] + locale_dict[key])

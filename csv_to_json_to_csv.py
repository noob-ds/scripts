import pandas as pd
import json
import csv

def explode(record):
    result = []
    record = record.replace("\\", "").replace("\"{", "{").replace("}\"", "}")

    json_parsed = json.loads(record)
    for r in json_parsed['placements']:
        temp_res = [r['type'], r['percentage'], r['absoluteCost']]
        result.append(temp_res)
    return result


def write_to_file(file_path, rows):
    csv_file = open(file_path, 'w', newline='')
    obj = csv.writer(csv_file)
    for row in rows:
        obj.writerow(row)


if __name__ == '__main__':
    results = []
    col = []
    with open("/Users/sachit.sharma/Downloads/query_result.csv", "r") as infile:
        col = infile.readline().strip().split(",")
        content = [i.strip().split(",", 4) for i in infile.readlines()]
    col = list(map(lambda x:x.replace("\"",""), col))
    results.append(col)

    df = pd.DataFrame(content, columns=col)

    for index, row in df.iterrows():
        csv_row = list(map(lambda x: x.replace("\"", ""), row.tolist()))
        res_row = []

        if row[col[4]] == "NULL":
            res_row = csv_row[:3] + ["NULL", "NULL", "NULL"]
            results.append(res_row)
        else:
            rows = explode(row[4])
            exploded_rows = list(map(lambda x: csv_row[:3] + x, rows))
            results = results + exploded_rows

    write_to_file("/Users/sachit.sharma/Downloads/res_query_result.csv", results)

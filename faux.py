import csv
import json
import os

class Fauxlizer():
    # Define Fauxlizer class constructor.
    def __init__(self, filename): # Filename as unique input argument.
        self.filename = filename

    # Fauxlizer class methods.
    def validate_faux(self):
        try:
            with open(self.filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')

                # Check if file is empty.
                if os.stat(self.filename).st_size == 0:
                    raise SystemExit('File is empty.')

                # Check if first line of csv is header.
                fields = next(csvreader)
                if fields != ['experiment_name', 'sample_id', 'fauxness', 'category_guess']:
                    raise SystemExit('Invalid Header.')

                line_no = 1
                for row in csvreader:
                    line_no += 1

                    # Validate number of fields in each csv row.
                    if len(row) != 4:
                        raise SystemExit('Invalid row number of fields.')

                    # Iterate over fields of each row.
                    for field in row:
                        # Declare options for category guess:
                        category_guess = ['real', 'fake', 'ambiguous']

                        # Ensure experiment name is a string and not empty.
                        if row[0] in ("", None):
                            raise SystemExit('Experiment cannot be empty. Row: ' + str(line_no))

                        # Validate sample_id.
                        try:
                            value = int(row[1])
                            if value <= 0:
                                raise SystemExit('Sample ID must be a positive integer. Row: ' + str(line_no) + '. Value: ' + str(row[1]))
                        except ValueError:
                            print('Invalid datatype for sample_id. Row: ' + str(line_no) + '. Value: ' + str(row[1]))
                            break

                        # Validate fauxness.
                        try:
                            value = float(row[2])
                            if not(value >= 0 and value <= 1):
                                raise SystemExit("Fauxness not within range [0,1]. Row: " + str(line_no) + '. Value: ' + str(row[2]))
                        except ValueError:
                            print('Invalid datatype for sample_id. Row: ' + str(line_no) + '. Value: ' + str(row[2])) 
                            break              

                        # Validate category guess.
                        guess = str(row[3])
                        if guess not in category_guess:
                            raise SystemExit("Invalid guess. Row: " + str(line_no) + '. Value: ' + str(row[3]))

                if line_no == 1:
                        raise StopIteration                      

        except FileNotFoundError as fnf_error:
            print(fnf_error)

        except StopIteration:
            print("File has no content.")

        return True  

    """Method to provide a summary of the data in the file in JSON format."""
    def jsonify_data(self): 

        # Ensure csv is in valid format.
        is_valid_csv = self.validate_faux()

        if is_valid_csv:
            csvfile = open(self.filename, 'r')

            fieldnames = ("experiment_name","sample_id","fauxness","category_guess")
            reader = csv.DictReader( csvfile, fieldnames)
            next(csvfile)
            faux_list = list(reader)
            json_response = json.dumps(faux_list)

        return json_response

    """Method to return a particular row of data in several formats: python in-memory representation, json and fauxlizer's native csv format."""
    def return_row(self, line_no, response_format): 
        self.line_no = line_no
        self.response_format = response_format

        # Ensure csv is in valid format.
        is_valid_csv = self.validate_faux()

        if is_valid_csv:
            with open(self.filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                rows = [r for r in csvreader]
                selected_row = rows[line_no]

                # In memory.
                if response_format == 'in-memory':
                    response = selected_row

                # JSON.
                elif response_format == 'json':
                    for field in selected_row: 
                        json_dict = {"experiment_name": selected_row[0],
                                     "sample_id": selected_row[1],
                                     "fauxness": selected_row[2],
                                     "category_guess": selected_row[3]}

                    response = json.dumps(json_dict)

                # Native csv format.
                elif response_format == 'faux-csv':
                    response = ', '.join(selected_row)

        return response            


def main():
    instance = Fauxlizer('data/file_0.faux')
    method_1 = instance.validate_faux()
    print(method_1)                
    method_2 = instance.jsonify_data()
    print(method_2)
    method_3 = instance.return_row(1, 'faux-csv')
    print(method_3)
if __name__ == "__main__":
    main()

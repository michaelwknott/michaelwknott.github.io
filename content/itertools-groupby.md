Title: Grouping Data using Itertools groupby
Date: 2023-07-21 13:00
Category: Notes
Tags: Python, Itertools, Notes
Authors: Michael Knott
Summary: Grouping athlete data using Itertools groupby
Status: published

## Grouping Data

I've got a csv file containing athlete fitness assessment data. Each line contains a record related to a single assessment with the following fields:

+ athlete_name
+ sport
+ status
+ date
+ time_trial_name
+ time_trial_distance
+ time_trial_time

Currently there are multiple records for each athlete consisting of a 2km time trial or 5m flying sprint. I've included dummy data below:

    # fitness_results.csv

    athlete_name,sport,status,date,time_trial_name,time_trial_distance,time_trial_time
    John Doe,Boxing,True,2022/05/12,2km time trial,2000,510
    John Doe,Boxing,True,2023/06/18,5m flying sprint,5,0.67
    Jane Smith,Hockey,True,2022/07/03,2km time trial,2000,460
    Jane Smith,Hockey,True,2022/08/22,5m flying sprint,5,0.52
    Michael Johnson,Boxing,True,2022/09/09,2km time trial,2000,490
    Michael Johnson,Boxing,True,2022/10/17,5m flying sprint,5,0.72
    Sarah Thompson,Hockey,True,2022/11/25,2km time trial,2000,520
    Sarah Thompson,Hockey,True,2022/12/07,5m flying sprint,5,0.61
    ...

I need to ingest the csv file and group the records by athlete name.

### Itertools Groupby Function

One way to group data is to use the `groupby` function from the Itertools library. The `groupby` function accepts a positional argument and keyword argument (`key`). The positional argument expects an iterable and the keyword argument requires a function. The function passed to `key` should return a value that is used to identify groups. The `groupby` function returns an iterator of tuples. Each tuple contains a value (returned by the function passed to the keyword argument `key`) and an iterator (`itertools._grouper`) which contains the grouped data.

The code below opens the csv file, uses the `groupby` function to group the data by `athlete_name` and prints the `key_value` and `group` from the iterator returned by the `groupby` function:  

    :::python
    # script.py
    from pathlib import path

    def group_results_by_name(filepath: Path) -> None:
        with open(filepath) as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for key_value, group in groupby(reader, key=lambda row: row[0]):
                print(key_value, group)
    
    if __name__ == "__main__":
        FILEPATH = Path("fitness_results.csv")
        group_results_by_name(FILEPATH)
    
    # Terminal output
    John Doe, <itertools._grouper object at 0x7f6d9d1ec910>
    Jane Smith, <itertools._grouper object at 0x7f6d9d1ee770>
    Michael Johnson, <itertools._grouper object at 0x7f6d9d1ec910>
    Sarah Thompson, <itertools._grouper object at 0x7f6d9d1ee770>

### Unordered Data

One caveat is that the `groupby` function requires ordered data as it creates a new group every time the key function returns a new value. For example, changing the order to the csv data:
    
    # unordered_fitness_results.csv

    athlete_name,sport,status,date,time_trial_name,time_trial_distance,time_trial_time
    John Doe,Boxing,True,2022/05/12,2km time trial,2000,510
    Jane Smith,Hockey,True,2022/07/03,2km time trial,2000,460
    John Doe,Boxing,True,2023/06/18,5m flying sprint,5,0.67
    Jane Smith,Hockey,True,2022/08/22,5m flying sprint,5,0.52
    Michael Johnson,Boxing,True,2022/10/17,5m flying sprint,5,0.72
    Sarah Thompson,Hockey,True,2022/11/25,2km time trial,2000,520
    Michael Johnson,Boxing,True,2022/09/09,2km time trial,2000,490
    Sarah Thompson,Hockey,True,2022/12/07,5m flying sprint,5,0.61
    ...

results in the following output:

    :::python
    # script.py
    from pathlib import path

    def group_results_by_name(filepath: Path) -> None:
        with open(filepath) as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for key_value, group in groupby(reader, key=lambda row: row[0]):
                print(key_value, group)
    
    if __name__ == "__main__":
        FILEPATH = Path("unordered_fitness_results.csv")
        group_results_by_name(FILEPATH)
    

    # Terminal output
    John Doe, <itertools._grouper object at 0x7f4d618a0880>
    Jane Smith, <itertools._grouper object at 0x7f4d618a26e0>
    John Doe, <itertools._grouper object at 0x7f4d618a0880>
    Jane Smith, <itertools._grouper object at 0x7f4d618a26e0>
    Michael Johnson, <itertools._grouper object at 0x7f4d618a0880>
    Sarah Thompson, <itertools._grouper object at 0x7f4d618a26e0>
    Michael Johnson, <itertools._grouper object at 0x7f4d618a0880>
    Sarah Thompson, <itertools._grouper object at 0x7f4d618a26e0>
    
Due to the unordered data, the `groupby` function created multiple groups per `athlete_name`.

### Ordering csv Data

As the data from the csv file will be unordered I need to sort the data before using the `groupby` function. The following code opens the csv file and returns the data sorted by `athlete_name`.

    :::python
    # script.py
    from collections.abc import Iterator
    from pathlib import Path

    def sort_file_by_athlete_name(filepath: Path) -> list[list]
        with open(filepath) as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            sorted_records = sorted(reader, key=lambda record: record[0])
        return sorted_records

    if __name__ == "__main__":
            FILEPATH = Path("unordered_fitness_results.csv")
            sorted_records = sort_file_by_athlete_name(FILEPATH)
            print(sorted_records)
    
    # Terminal output
    [['Jane Smith', 'Hockey', 'True', '2022/07/03', '2km time trial', '2000', '460'], ['Jane Smith', 'Hockey', 'True', '2022/08/22', '5m flying sprint', '5', '0.52'], ['John Doe', 'Boxing', 'True', '2022/05/12', '2km time trial', '2000', '510'], ['John Doe', 'Boxing', 'True', '2023/06/18', '5m flying sprint', '5', '0.67'], ['Michael Johnson', 'Boxing', 'True', '2022/09/09', '2km time trial', '2000', '490'], ['Michael Johnson', 'Boxing', 'True', '2022/10/17', '5m flying sprint', '5', '0.72'], ['Sarah Thompson', 'Hockey', 'True', '2022/11/25', '2km time trial', '2000', '520'], ['Sarah Thompson', 'Hockey', 'True', '2022/12/07', '5m flying sprint', '5', '0.61']]

### Grouping Ordered Data

With the data sorted, I can update the `group_results_by_name` function to store the groups in a dictionary:

    :::python
    # script.py
    from collections.abc import Iterator
    from pathlib import Path

    def sort_file_by_athlete_name(filepath: Path) -> list[list]
        with open(filepath) as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            sorted_records = sorted(reader, key=lambda record: record[0])
        return sorted_records
    
    def group_results_by_name(sorted_records: list[list]) -> dict[str, Iterator]
        results = {
            key_value: list(group)
            for key_value, group in groupby(sorted_records, key=lambda row: row[0])
        }
        return results

    if __name__ == "__main__":
            FILEPATH = Path("unordered_fitness_results.csv")
            sorted_records = sort_file_by_athlete_name(FILEPATH)
            groups = group_results_by_name(sorted_records)
            print(groups)
    
    # Terminal output
    {'Jane Smith': [['Jane Smith', 'Hockey', 'True', '2022/07/03', '2km time trial', '2000', '460'], ['Jane Smith', 'Hockey', 'True', '2022/08/22', '5m flying sprint', '5', '0.52']], 'John Doe': [['John Doe', 'Boxing', 'True', '2022/05/12', '2km time trial', '2000', '510'], ['John Doe', 'Boxing', 'True', '2023/06/18', '5m flying sprint', '5', '0.67']], 'Michael Johnson': [['Michael Johnson', 'Boxing', 'True', '2022/09/09', '2km time trial', '2000', '490'], ['Michael Johnson', 'Boxing', 'True', '2022/10/17', '5m flying sprint', '5', '0.72']], 'Sarah Thompson': [['Sarah Thompson', 'Hockey', 'True', '2022/11/25', '2km time trial', '2000', '520'], ['Sarah Thompson', 'Hockey', 'True', '2022/12/07', '5m flying sprint', '5', '0.61']]}

I now have the data grouped by `athlete_name` which can be used for further analysis.
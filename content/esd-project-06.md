Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 6
Date: 2023-07-27 13:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing the CSV.........
Status: draft

### CsvRepository

I created two csv files with dummy fitness results and workouts. The first line of the csv files contains headers and is followed by athlete fitness or workout data.

    # fitness_assessments.csv

    athlete_name,sport,status,date,time_trial_name,time_trial_distance,time_trial_time
    John Doe,Boxing,True,2022/05/12,2km time trial,2000,510
    John Doe,Boxing,True,2023/06/18,5m flying sprint,5,0.67
    Jane Smith,Hockey,True,2022/07/03,2km time trial,2000,460
    Jane Smith,Hockey,True,2022/08/22,5m flying sprint,5,0.52

    # conditioning_workouts.csv

    workout_name,work_interval_time,work_interval_percentage_mas,work_interval_percentage_asr,rest_interval_time,rest_interval_percentage_mas,rest_interval_percentage_asr
    Passive Long Intervals - Normal,2,100,0,2,0,0
    Passive Long Intervals - Extensive,2,100,0,1,0,0
    Passive Long Intervals - Intensive,2,100,0,3,0,0

The fitness_assessments.csv file contains multiple records of 2km time trial and 5m flying sprint records for each athlete. I needed to ingest the data and group by athlete name. Then I needed to find the latest 2km time trial and 5m flying sprint records and use these to create a FitnessProfile object.

I'll often be prescribing conditioning sessions by sport. I need the ability to filter the records by sport. I believe I should do this when loading the data into memory. I can then create FitnessProfile objects and assign to an attribute in the CsvRepository class.
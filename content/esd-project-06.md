Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 6
Date: 2023-08-03 16:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing the Concrete Repositories for the Persistence Layer
Status: published

## Creating the CSV Repositories

In the previous [post](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-5.html) I outlined the implementation of `AbstractRepository`. With this in place I needed to create the concrete repositories to manage interactions with the csv files.

### Dummy Data

I started by creating two csv files with dummy fitness results and workouts. The first line of the csv files contains headers and is followed by athlete fitness or workout training variables.

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

### CsvFitnessProfileRepository

The fitness_assessments.csv file contains multiple records of 2km time trial and 5m flying sprint records for each athlete. I needed to ingest the data and group by athlete name. Then I needed to find the latest 2km time trial and 5m flying sprint records and use these to create a FitnessProfile object.

    :::python
    class CsvFitnessProfileRepository(AbstractRepository[FitnessProfile]):
    """CSV implementation of FitnessProfile repository."""

        def __init__(self, filepath: str):
            """Initialise CsvRepository with fitness profiles.

            Args:
                filepath: The filepath for the fitness assessment CSV files.
            """
            self._filepath = Path(filepath)
            self._fitness_profiles: dict[str, FitnessProfile] = {}
            self._load()

        def _load(self):
            with open(self._filepath) as f:
                reader = csv.reader(f)
                next(reader)  # skip header row

                # group reader by name
                athlete_records = defaultdict(list)
                for record in reader:
                    athlete_records[record[0]].append(record)

                # find latest 2km and 5m for each athlete
                for athlete_name, athlete_results in athlete_records.items():
                    latest_2km = max(
                        result
                        for result in athlete_results
                        if result[4] == "2km time trial"
                    )
                    latest_5m = max(
                        result
                        for result in athlete_results
                        if result[4] == "5m flying sprint"
                    )

                    # create FitnessProfile for each athlete
                    profile = FitnessProfile(
                        name=athlete_name,
                        time_trial_distance=int(latest_2km[5]),
                        sprint_distance=int(latest_5m[5]),
                        time_trial_time=int(latest_2km[6]),
                        sprint_time=float(latest_5m[6]),
                    )

                    self._fitness_profiles[athlete_name] = profile

        def get(self, id: str) -> FitnessProfile:
            """Get a single entity from the persistence layer."""
            return self._fitness_profiles[id]

        def get_all(self) -> Sequence[FitnessProfile]:
            """Get a sequence of entities from the persistence layer."""
            return list(self._fitness_profiles.values())

### A Quick Note on Keeping Things Simple...

I haven't implemented the `add` method as I removed it from the `AbstractRepository`. As I'm moving through the project I've realised that I'm trying to implement functionality that I don't currently need to create an MVP. This is slowing down the project and moving my attention away from learning the design patterns. My goal is to create an MVP implemented with the minimum required functionality and the design patterns I'd like to learn. Once I have a working application I can revisit the additional functionality. See [issue 8](https://github.com/michaelwknott/esd/issues/8) and [issue 9](https://github.com/michaelwknott/esd/issues/9) for previous examples of functionality that I have moved to the backlog.

### CsvWorkoutRepository

The conditioning_workouts.csv file contains the training variables for each conditioning workout. Again, I needed to ingest the csv data and create a `Workout` object. One nice addition to the class is the `_convert_types` method. This provides a cleaner way of converting the data types of each csv filed prior to instantiating each `Workout` instance. I was introduced to this approach through David Beazley's [Practical Programming](https://dabeaz-course.github.io/practical-python/Notes/Contents.html) course. Specifically, see [exercise 2.24](https://dabeaz-course.github.io/practical-python/Notes/02_Working_with_data/07_Objects.html).

    :::python
    class CsvWorkoutRepository(AbstractRepository[Workout]):
    """CSV implementation of Workout repository."""

        def __init__(self, filepath: str):
            """Initialise CsvRepository with workouts.

            Args:
                filepath: The filepath for the workouts CSV file.
            """
            self._file_path = Path(filepath)
            self._workouts: dict[str, Workout] = {}
            self._load()

        def _convert_types(self, record: list[str]) -> list:
            types = [str, int, float, float, int, float, float]
            return [func(val) for func, val in zip(types, record)]

        def _load(self):
            with open(self._file_path) as f:
                reader = csv.reader(f)
                next(reader)  # skip header row

                for record in reader:
                    converted = self._convert_types(record)
                    workout = Workout(*converted)
                    self._workouts[workout.name] = workout

        def get(self, id: str) -> Workout:
            """Get a single entity from the persistence layer."""
            return self._workouts[id]

        def get_all(self) -> Sequence[Workout]:
            """Get a sequence of entities from the persistence layer."""
            return list(self._workouts.values())

With the creation of the two repositories I now have the csv data stored in `FitnessProfile` and `Workout` objects and available in working memory. The next step is to create a service layer which outlines the use case for the data. For the MVP this will be calculating individual target distances for conditioning workouts.
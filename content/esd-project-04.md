Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 4
Date: 2023-07-18 10:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Domain Logic: Prescribing Individualised Conditioning Sessions using MAS
Status: published

[Part 1](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-1.html) covered project rationale, [Part 2](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-2.html) outlined my project set-up workflow and [Part 3](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-3.html) showed my use of GitHub Projects. This post outlines my implementation of the domain logic for prescribing individualised conditioning sessions.

## Creating the Domain Logic to Prescribe Individualised Conditioning Sessions

I decided to start the project by implementing the functionality to prescribe individualised conditioning sessions based upon assessment results. This involved calculating each athletes Maximum Aerobic Speed (MAS), Anaerobic Speed Reserve (ASR) and Maximum Sprinting Speed (MSS) from their fitness assessment data and using these metrics with workout training variables to calculate target work and rest interval distances.

### Assumptions

For this part of the project I assumed athlete fitness data and workout data had already been queried and loaded into memory. I could then ignore anything related to data input/output and persistance and concentrate on the logic required to calculate MAS, ASR, MSS and target distances for each athlete completing the workout.

When implemented, a fitness assessment record will have the following fields:

+ athlete name
+ sport
+ status
+ date
+ time trial name
+ time trial distance
+ time trial time

and the fields for a workout record will be:

+ workout name (the workout type including work and rest interval durations)
+ work interval time (the work interval duration)
+ work interval percentage Maximum Aerobic Speed (the percentage MAS for the work interval)
+ work interval percentage Anaerobic Speed Reserve (the percentage ASR for the work interval)
+ rest interval time (the rest interval duration)
+ rest interval percentage MAS (the percentage MAS for the rest interval)
+ rest interval percentage ASR the percentage ASR for the rest interval

2km time trial and 5m sprint fitness assessment records mapped to a Python object will have the following attributes (I won't map the 'sport' and 'status' fields to the Python object as these will only be required to filter queries):

        name = "John Smith"
        time_trial_distance = 2000
        time_trial_time = "07:01"
        sprint_distance = 5
        sprint_time = 0.56

and a workout record mapped to a Python object will have:

        workout_name = "Passive Long Intervals - Normal (3 mins work / 3 mins rest)"
        work_interval_time = 3
        work_interval_percentage_mas = 100
        work_interval_percentage_asr = 0
        rest_interval_time = 3
        rest_interval_percentage_mas = 0
        rest_interval_percentage_asr = 0

### MAS, ASR and MSS Calculations

The following formulas are used to calculate each fitness metric:

*MAS* = time trial distance (m) / time trial time (s)

*MSS* = sprint distance (m) / sprint time (s)

*ASR* = MSS (m/s) - ASR (m/s)

As the fitness record from the persistance layer doesn't contain these fields I will need to calculate these metrics when mapping the fitness record to a Python object. 

### Work and Rest Interval Target Distance Calculations

Calculating work and rest interval target distances involves multiplying an athlete's MAS (m/s) by the `Workout` `work_interval_percentage` and `rest_interval_percentage` to get the individualised target intensity for the session.

*individual_work_target_intensity* = athlete_mas * `work_interval_percentage`

*individual_rest_target_intensity* = athlete_mas * `rest_interval_percentage`

This value is multiplied by the workout `work_interval_time` (in seconds) and `rest_interval_time` (in seconds) to get the target distances.

*work_interval_target_distance* = individual_work_target_intensity * `work_interval_time`
*rest_interval_target_distance* = individual_rest_target_intensity * `rest_interval_time`

### Mapping Fitness and Workout Records to Python Objects

With the assumption that the database had been queried and I had the athlete and workout records in memory, I needed to create a Python object for each record to implement the domain logic.

I used a dataclass object for each athlete's fitness profile and created the ability to dynamically calculate MAS, ASR and MSS using properties.

    :::python
    # athlete.py

    @dataclass
    class FitnessProfile:
        """Represents an athlete's fitness profile.

        Attributes:
            name: A str of the athlete's name.
            time_trial_distance: An int of the time trial distance in meters.
            sprint_distance: An int of the sprint distance in meters.
            time_trial_time: An int of the time taken to complete the 2km time trial.
            sprint_time: A float of the time taken to complete the 5m sprint.

        Properties:
            max_aerobic_speed: A float representing MAS in meters per second.
            max_sprinting_speed: A float representing MSS in meters per second.
            anaerobic_speed_reserve: A float representing ASR in meters per second.
        """

        name: str
        time_trial_distance: int
        sprint_distance: int
        time_trial_time: int
        sprint_time: float

        @property
        def max_aerobic_speed(self) -> float:
            """Maximal Aerobic Speed in m/s (rounded to 2 decimal places)."""
            if self.time_trial_time != 0:
                return round(self.time_trial_distance / self.time_trial_time, 2)
            else:
                return 0

        @property
        def max_sprinting_speed(self) -> float:
            """Maximum Sprinting Speed in m/s (rounded to 2 decimal places)."""
            if self.sprint_time != 0:
                return round(self.sprint_distance / self.sprint_time, 2)
            else:
                return 0

        @property
        def anaerobic_speed_reserve(self) -> float:
            """Anaerobic Speed Reserve in m/s (rounded to 2 decimal places)."""
            if self.max_aerobic_speed == 0 or self.max_sprinting_speed == 0:
                return 0
            else:
                return round(self.max_sprinting_speed - self.max_aerobic_speed, 2)


I also used a dataclass to represent a workout and a property to dynamically calculate the workout name:

    :::python
    # session.py

    @dataclass
    class Workout:
        """Workout type and it's associated training variables."""

        workout_type: str
        work_interval_time: int
        work_interval_percentage_mas: float
        work_interval_percentage_asr: float | None
        rest_interval_time: int
        rest_interval_percentage_mas: float
        rest_interval_percentage_asr: float | None

        @property
        def name(self) -> str:
            """Name and description of workout.

            Returns:
                A string containing workout name and description.
            """
            return (
                f"{self.workout_type}: "
                f"{self.work_interval_time} mins work / "
                f"{self.rest_interval_time} mins rest"
            )

### Calculating Workout Target Distances for Each Athlete

With the `FitnessProfile` and `Workout` objects in place I created two functions to calculate work and rest interval distances. Each function returns a dictionary mapping the name of an athlete to the work or rest interval target distances. I believe I'll be able to pass the dictionaries as context to the jinja templates to create a downloadable sheet of each athlete's target distances to be used during conditioning session set-up.

 I had originally planned to also implement logic to calculate target distances using MAS and ASR, as well as provide the ability to calculate target pace as an extra option. However, implementing this logic was slowing down the project. I decided to leave this functionality for now and added [ASR calculations](https://github.com/michaelwknott/esd/issues/8) and [pace calculations](https://github.com/michaelwknott/esd/issues/9) issues to the ESD GitHub project for implementation at a later date.

I also created `_convert_minutes_to_seconds` as a helper function to convert work and rest interval time from minutes to seconds. This was required as time (in seconds) is multiplied by each athlete's work and rest interval MAS to calculate the target distance:

    :::python
    def calculate_work_interval_distances(
        workout: Workout, fitness_profiles: Collection[FitnessProfile]
    ) -> dict[str, float]:
        """Calculate work interval distances for each athlete.

        Args:
            workout: The training variables for the workout.
            fitness_profiles: The fitness profile for each athlete completing the workout.

        Returns:
            A dictionary of athlete names mapped to work interval distances.
        """
        work_distances = {}
        for profile in fitness_profiles:
            work_interval_mas = (
                profile.max_aerobic_speed * workout.work_interval_percentage_mas
            )
            work_interval_distance = round(
                work_interval_mas * _convert_minutes_to_seconds(workout.work_interval_time),
                0,
            )
            work_distances[profile.name] = work_interval_distance
        return work_distances


    def calculate_rest_interval_distances(
        workout: Workout, fitness_profiles: Collection[FitnessProfile]
    ) -> dict[str, float]:
        """Calculate rest interval distances for each athlete.

        Args:
            workout: The training variables for the workout.
            fitness_profiles: The fitness profile for each athlete completing the workout.

        Returns:
            A dictionary of athlete names mapped to rest interval distances.
        """
        rest_distances = {}
        for profile in fitness_profiles:
            rest_interval_mas = (
                profile.max_aerobic_speed * workout.rest_interval_percentage_mas
            )
            rest_interval_distance = round(
                rest_interval_mas * _convert_minutes_to_seconds(workout.rest_interval_time),
                0,
            )
            rest_distances[profile.name] = rest_interval_distance
        return rest_distances


    def _convert_minutes_to_seconds(work_interval_time: int) -> int:
        """Convert minutes to seconds.

        Args:
            work_interval_time: The work interval time in minutes.

        Returns:
            The work interval time in seconds.
        """
        return work_interval_time * 60

### Future Considerations

I'm not completely happy with the names I've chosen for the dataclass methods. I'm trying to give each method a descriptive name, however I feel they are currently too long. This could also be applied to variable names in the `calculate_rest_interval_distances`
and `calculate_work_interval_distances`.

The `calculate_rest_interval_distances` and `calculate_work_interval_distances` functions accept a `Workout` and `FitnessProfile` object as arguments. However, they don't require all of the information within the object. I believe I should consider re-writing the functions to accept only the information they require.

Similarly, the `calculate_rest_interval_distances` and `calculate_work_interval_distances` functions complete similar work and there is duplication of code. I think I could create a single function to calculate target distances and reduce duplication.

I assumed that 2km time trial times are already an integer data type. This assumption spreads to the tests I've written where I pass the required data types when instantiating AthleteProfile and Workout instances. In the future I will need to create the functionality to change the data types when coupling the logic to the persistence layer.

I'll also need to convert a number of database records (e.g. lines in a csv file or a SQLAlchemy Result object) into individual `FitnessProfile` instances. I believe this should be straight forward as Result objects and files are iterables that can be used in a for loop.

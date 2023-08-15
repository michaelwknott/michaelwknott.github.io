Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 7
Date: 2023-08-14 16:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing a Service Layer to Separate the Domain and presentation Layers
Status: published

With the ability to communicate with the [csv file persistence layer](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-6.html), the next step in the project was to implement a service layer to make it easier to swap out presentation layers. The service layer achieves this by acting as an abstraction between the domain logic and the presentation layer. This means the presentation layer will communicate with the service layer to initiate the required domain logic and the service layer will communicate with the persistence layer to retrieve the necessary data.

### Creating an In-memory Repository to Test the Service Layer

To make it easier to test the service layer I created concrete repositories for `FitnessProfile` and `Workout` domain entities. Although I currently only require read access to the persistence layer, using `FakeFitnessProfileRepository` and `FakeFitnessProfileRepository` avoids using data from the actual persistence layer (currently csv files). This would be more important if I was writing back to the persistence layer as using the production persistence layer for tests has the potential to affect the state of the application.

    :::python
    from esd.adapters.repository import AbstractRepository
    from esd.domain.athlete import FitnessProfile
    from esd.domain.session import Workout


    class FakeFitnessProfileRepository(AbstractRepository[FitnessProfile]):
        """Fake implementation of FitnessProfile repository."""

        def __init__(self, fitness_profiles: dict[str, FitnessProfile]):
            """Initialise FakeFitnessProfileRepository with fitness profiles."""
            self._fitness_profiles = fitness_profiles

        def get(self, id: str) -> FitnessProfile:
            """Get a single entity from the persistence layer."""
            return self._fitness_profiles[id]

        def get_all(self) -> list[FitnessProfile]:
            """Get all entities from the persistence layer."""
            return list(self._fitness_profiles.values())


    class FakeWorkoutRepository(AbstractRepository[Workout]):
        """Fake implementation of Workout repository."""

        def __init__(self, workouts: dict[str, Workout]):
            """Initialise FakeWorkoutRepository with workouts."""
            self._workouts = workouts

        def get(self, id: str) -> Workout:
            """Get a single entity from the persistence layer."""
            return self._workouts[id]

        def get_all(self) -> list[Workout]:
            """Get all entities from the persistence layer."""
            return list(self._workouts.values())

### My First Use Case

From my understanding the service layer contains all the functions or methods required to trigger the domain logic for a particular use case. As I mentioned in [part 1](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-1.html), my original plan was to create a PDF output of the individual work and rest interval distances for each athlete. However, to keep the project moving forward my first use case will provide output to the terminal using the [Rich](https://rich.readthedocs.io/en/stable/introduction.html) package. I made this decision as I haven't previously used packages for creating PDFs and I have familiarity with Rich which allowed me to maintain project momentum. The [PDF functionality](https://github.com/michaelwknott/esd/issues/32) will be added at a later date. 

So for now, my use case is as follows:

A coach wants to prescribe individual conditioning workouts for their athletes. They use a CLI tool to select a workout and receive work and rest interval distances for each individual athlete as output in the console. The coach can then use this information to set up the workout.

### Creating the Service Layer

To achieve the first use case requires a number of steps:

1. Get the required `Workout object`
1. Get the required `FitnessProfiles`
1. Calculate the individual work and rest interval distances using the `Workout` and `FitnessProfile` objects
1. Return an output in the terminal that shows work and rest interval distances for each athlete

For steps 1 and 2 I needed to be able to communicate with the persistance layer. To achieve this the  `WorkoutService` `__init__` method  initialises the `workout_repository` and `fitness_profile_repository` attributes with class instances that implements the `AbstractRepository` interface for `Workout` and `FitnessProfile` objects.

    :::python
    class WorkoutService:
    """Service class for workout related operations."""

        def __init__(
            self,
            workout_repository: AbstractRepository[Workout],
            fitness_profile_repository: AbstractRepository[FitnessProfile],
        ):
            """Initialise WorkoutService with repositories."""
            self.workout_repository = workout_repository
            self.fitness_profile_repository = fitness_profile_repository

To get the required workout I created a `get_workout` method that calls the `workout_repository` `get` method to return a single `Workout` entity. The `Workout` object contains the training variables which will be used along each athlete's `FitnessProfile` to calculate individual work and rest interval distances. The calculations multiply an athlete's Maximum Aerobic Speed (MAS) in meters per second by the work or rest interval time in seconds. As the `Workout` object contains work and rest interval times in minutes I also created a helper function to convert minutes to seconds. 

    :::python
    class WorkoutService:
    """Service class for workout related operations."""

        def __init__(
            self,
            workout_repository: AbstractRepository[Workout],
            fitness_profile_repository: AbstractRepository[FitnessProfile],
        ):
            """Initialise WorkoutService with repositories."""
            self.workout_repository = workout_repository
            self.fitness_profile_repository = fitness_profile_repository

        def get_workout(self, id: str) -> Workout:
            """Get a workout from the repository.

            Returns:
                A workout.
            """
            return self.workout_repository.get(id)
        
        def _convert_minutes_to_seconds(self, work_interval_time: int) -> int:
            """Convert minutes to seconds.

            Args:
                work_interval_time: The work interval time in minutes.

            Returns:
                The work interval time in seconds.
            """
            return work_interval_time * 60

To get the required `FitnessProfiles` I created a `get_fitness_profiles` method which calls the `get_all()` method from the `fitness_profile_repository`. This return a list of `FitnessProfiles` which will be used alongside the `Workout` object to calculate the individual work and rest interval distances.

    :::python
    class WorkoutService:
    """Service class for workout related operations."""
    
    ...
    
        def get_fitness_profiles(self) -> list[FitnessProfile]:
            """Get all fitness profiles from the repository.

            Returns:
                A list of fitness profiles.
            """
            return self.fitness_profile_repository.get_all()

The previous steps have collected the required data. Step 3 uses this data to calculate the individual work and rest interval distances. I've taken the `calculate_work_interval_distances` and `calculate_rest_interval_distances` functions that was previously in the domain model and moved them into the service layer.

    :::python
    class WorkoutService:
    """Service class for workout related operations."""

    ...

        def _calculate_work_interval_distances(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> dict[str, float]:
            """Calculate work interval distances for each athlete.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.

            Returns:
                A dictionary of athlete names mapped to work interval distances.
            """
            work_distances = {}
            for profile in fitness_profiles:
                work_interval_mas = (
                    profile.max_aerobic_speed * workout.work_interval_percentage_mas
                )
                work_interval_distance = round(
                    work_interval_mas
                    * self._convert_minutes_to_seconds(workout.work_interval_time),
                    0,
                )
                work_distances[profile.name] = work_interval_distance
            return work_distances

        def _calculate_rest_interval_distances(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> dict[str, float]:
            """Calculate rest interval distances for each athlete.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.

            Returns:
                A dictionary of athlete names mapped to rest interval distances.
            """
            rest_distances = {}
            for profile in fitness_profiles:
                rest_interval_mas = (
                    profile.max_aerobic_speed * workout.rest_interval_percentage_mas
                )
                rest_interval_distance = round(
                    rest_interval_mas
                    * self._convert_minutes_to_seconds(workout.rest_interval_time),
                    0,
                )
                rest_distances[profile.name] = rest_interval_distance
            return rest_distances

The methods have an underscore suffix as they will be called internally by `print_workout_table`. This method provides the functionality to print a table containing athlete's names, work interval distances and rest interval distances to the terminal.

    :::python
    class WorkoutService:
    """Service class for workout related operations."""

    ...

        def print_workout_table(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> Table:
            """Print a table of names, work interval and rest interval distances.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.
            """
            work_distances = self._calculate_work_interval_distances(
                workout, fitness_profiles
            )
            rest_distances = self._calculate_rest_interval_distances(
                workout, fitness_profiles
            )

            console = Console()
            date = datetime.now().strftime("%d/%m/%Y")
            table = Table(title=f"{workout.name} - {date}")
            table.add_column("Athlete Name", justify="left")
            table.add_column("Work Distance (m)", justify="center")
            table.add_column("Rest Distance (m)", justify="center")

            for athlete in work_distances:
                table.add_row(
                    athlete,
                    f"{work_distances[athlete]}m",
                    f"{rest_distances[athlete]}m",
                )

            console.print(table)
            return table

The service layer now has the required functionality to meet my first use case. The next step is to create a presentation layer that accepts user input and communicates with the service layer to create  the required output.

### The Complete `WorkoutService` Implementation

For completeness I've included the full implementation below.

    :::python
    from datetime import datetime

    from rich.console import Console
    from rich.table import Table

    from esd.adapters.repository import AbstractRepository
    from esd.domain.athlete import FitnessProfile
    from esd.domain.session import Workout


    class WorkoutService:
        """Service class for workout related operations."""

        def __init__(
            self,
            workout_repository: AbstractRepository[Workout],
            fitness_profile_repository: AbstractRepository[FitnessProfile],
        ):
            """Initialise WorkoutService with repositories."""
            self.workout_repository = workout_repository
            self.fitness_profile_repository = fitness_profile_repository

        def _convert_minutes_to_seconds(self, work_interval_time: int) -> int:
            """Convert minutes to seconds.

            Args:
                work_interval_time: The work interval time in minutes.

            Returns:
                The work interval time in seconds.
            """
            return work_interval_time * 60

        def get_workout(self, id: str) -> Workout:
            """Get a workout from the repository.

            Returns:
                A workout.
            """
            return self.workout_repository.get(id)

        def get_fitness_profiles(self) -> list[FitnessProfile]:
            """Get all fitness profiles from the repository.

            Returns:
                A list of fitness profiles.
            """
            return self.fitness_profile_repository.get_all()

        def _calculate_work_interval_distances(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> dict[str, float]:
            """Calculate work interval distances for each athlete.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.

            Returns:
                A dictionary of athlete names mapped to work interval distances.
            """
            work_distances = {}
            for profile in fitness_profiles:
                work_interval_mas = (
                    profile.max_aerobic_speed * workout.work_interval_percentage_mas
                )
                work_interval_distance = round(
                    work_interval_mas
                    * self._convert_minutes_to_seconds(workout.work_interval_time),
                    0,
                )
                work_distances[profile.name] = work_interval_distance
            return work_distances

        def _calculate_rest_interval_distances(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> dict[str, float]:
            """Calculate rest interval distances for each athlete.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.

            Returns:
                A dictionary of athlete names mapped to rest interval distances.
            """
            rest_distances = {}
            for profile in fitness_profiles:
                rest_interval_mas = (
                    profile.max_aerobic_speed * workout.rest_interval_percentage_mas
                )
                rest_interval_distance = round(
                    rest_interval_mas
                    * self._convert_minutes_to_seconds(workout.rest_interval_time),
                    0,
                )
                rest_distances[profile.name] = rest_interval_distance
            return rest_distances

        def print_workout_table(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> Table:
            """Print a table of names, work interval and rest interval distances.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.
            """
            work_distances = self._calculate_work_interval_distances(
                workout, fitness_profiles
            )
            rest_distances = self._calculate_rest_interval_distances(
                workout, fitness_profiles
            )

            console = Console()
            date = datetime.now().strftime("%d/%m/%Y")
            table = Table(title=f"{workout.name} - {date}")
            table.add_column("Athlete Name", justify="left")
            table.add_column("Work Distance (m)", justify="center")
            table.add_column("Rest Distance (m)", justify="center")

            for athlete in work_distances:
                table.add_row(
                    athlete,
                    f"{work_distances[athlete]}m",
                    f"{rest_distances[athlete]}m",
                )

            console.print(table)
            return table
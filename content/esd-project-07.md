Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 7
Date: 2023-08-14 16:00
Modified: 2023-08-17 15:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing a Service Layer to Separate the Domain and presentation Layers
Status: published

## Service Layer

The previous post outlined the implementation of the [csv file persistence layer](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions-part-6.html). With this in place, the next step in the project was to implement a service layer to make it easier to swap out presentation layers. The service layer achieves this by acting as an abstraction between the domain logic and the presentation layer. This means the presentation layer will communicate with the service layer to initiate the required domain logic and the service layer will communicate with the persistence layer to retrieve the necessary data.

### Creating an In-memory Repository to Test the Service Layer

To test the service layer I created in-memory concrete repositories for `FitnessProfile` and `Workout` domain entities. Using `FakeFitnessProfileRepository` and `FakeWorkoutRepository` whilst testing the service layer avoids using data from the production persistence layer (currently csv files). This reduces the chances of negatively affecting the persistence layer when performing read or write operations during tests. The fake in-memory repositories are implemented as follows:

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

*A coach wants to prescribe individual conditioning workouts for their athletes. They use a CLI tool to select a workout and receive work and rest interval distances for each individual athlete as output in the console. The coach can then use this information to set up the workout.*

### Creating the Service Layer

To achieve the first use case requires a number of steps each consisting of a single action:

1. Get all the workout names to display to the user
1. Get the required `Workout object`
1. Get the required `FitnessProfiles`
1. Calculate the individual work and rest interval distances using the `Workout` and `FitnessProfile` objects
1. Return an output in the terminal that shows work and rest interval distances for each athlete

The first 4 steps are general actions that will be required by all presentation layers. Step 5 is an action that is specific to the CLI presentation layer. To allow extensibility of the application without having to amend previously implemented code I have divided the actions into general and specific service classes. The general actions used across all presentation layers will be implemented in `WorkoutService` and the specific actions in`CLIService`.

### Creating `WorkoutService` for General Use Case Actions

For steps 1, 2 and 3 I needed to be able to communicate with the persistance layer. To achieve this the  `WorkoutService` `__init__` method  initialises the `workout_repository` and `fitness_profile_repository` attributes with class instances that implements the `AbstractRepository` interface for `Workout` and `FitnessProfile` objects.

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

To address step 1, I created the `get_workout_names` method to return a list of workout names. These names will be displayed to the user for selection of a single workout. For step 2, the selected workout name is passed to the `get_selected_workout` method to return a single `Workout` entity. The `Workout` object contains the training variables which are used along each athlete's `FitnessProfile` to calculate individual work and rest interval distances. The calculations multiply an athlete's Maximum Aerobic Speed (MAS) in meters per second by the work or rest interval time in seconds. As the `Workout` object contains work and rest interval times in minutes I also created a helper function to convert minutes to seconds. 

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

        def get_workout_names(self) -> list[str]:
            """Get all workout names from the repository.

            Workout names are displayed to the user to select the required workout.

            Returns:
                A list of workout names.
            """
            workouts = self.workout_repository.get_all()

            return [workout.name for workout in workouts]

        def get_selected_workout(self, selected_workout: str) -> Workout:
        """Get the selected workout from the repository.

        Args:
            selected_workout: The name of the selected workout.

        Returns:
            A workout.
        """
        return self.workout_repository.get(selected_workout)
        
        def _convert_minutes_to_seconds(self, work_interval_time: int) -> int:
            """Convert minutes to seconds.

            Args:
                work_interval_time: The work interval time in minutes.

            Returns:
                The work interval time in seconds.
            """
            return work_interval_time * 60

For step 3, the required `FitnessProfiles` are returned by `get_fitness_profiles`. This method calls `get_all()` from the `fitness_profile_repository`. The list of returned `FitnessProfiles` are used alongside the `Workout` object to calculate the individual work and rest interval distances.

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

The previous steps retrieve the required data. Step 4 uses the data to calculate the individual work and rest interval distances. I've taken the `calculate_work_interval_distances` and `calculate_rest_interval_distances` functions that were previously in the domain model and moved them into the service layer.

    :::python
    class WorkoutService:
    """Service class for workout related operations."""

    ...

        def calculate_work_interval_distances(
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

        def calculate_rest_interval_distances(
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

### Creating `CLIService` for Specific Use Case Actions

Step 5 requires work and rest interval distances to be printed in the terminal for each athlete. As this action is specific to the CLI presentation layer I created `CLIService` to encapsulate this behaviour. `CLIService` is initialised with an instance of `WorkoutService` and defines the `create_and_display_table` method. This provides `CLIService` with access to general use case actions and the action specific to the CLI presentation layer.

    :::python
    # cli_service.py

    from datetime import datetime

    from rich.console import Console
    from rich.table import Table

    from esd.domain.athlete import FitnessProfile
    from esd.domain.session import Workout
    from esd.service_layer.service import WorkoutService


    class CLIService:
        """Service class for CLI related operations."""

        def __init__(self, workout_service: WorkoutService):
            """Initialise CLIService with WorkoutService."""
            self.workout_service = workout_service

        def create_and_display_table(
            self, workout: Workout, fitness_profiles: list[FitnessProfile]
        ) -> Table:
            """Print a table of names, work interval and rest interval distances.

            Args:
                workout: The training variables for the workout.
                fitness_profiles: The fitness profile for each athlete completing the
                    workout.
            """
            work_distances = self.workout_service.calculate_work_interval_distances(
                workout, fitness_profiles
            )
            rest_distances = self.workout_service.calculate_rest_interval_distances(
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
    
### Extending the Service Layer

It is now straightforward to extend the service layer for additional presentation layers. For example, if I wanted to create API endpoints, I could create an `APIService` class that implements the required functionality for the API. The `APIService` class would be initialised with an instance of `WorkoutService` and would define the required methods for the API. The `WorkoutService` class would remain unchanged. 

### Next Steps

The service layer now has the required functionality to meet my first use case. The next step is to create a CLI presentation layer that accepts user input and communicates with `CLIService` to create the required output.

### The Complete `WorkoutService` Implementations

For completeness I've included the full implementation of `WorkoutService` below.

    :::python
    # service.py

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

        def get_selected_workout(self, selected_workout: str) -> Workout:
            """Get the selected workout from the repository.

            Args:
                selected_workout: The name of the selected workout.

            Returns:
                A workout.
            """
            return self.workout_repository.get(selected_workout)

        def get_workout_names(self) -> list[str]:
            """Get all workout names from the repository.

            Workout names are displayed to the user to select the required workout.

            Returns:
                A list of workout names.
            """
            workouts = self.workout_repository.get_all()

            return [workout.name for workout in workouts]

        def get_fitness_profiles(self) -> list[FitnessProfile]:
            """Get all fitness profiles from the repository.

            Returns:
                A list of fitness profiles.
            """
            return self.fitness_profile_repository.get_all()

        def calculate_work_interval_distances(
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

        def calculate_rest_interval_distances(
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

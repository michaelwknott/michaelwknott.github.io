Date: 2023-08-04 16:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing a Service Layer to Separate the Domain and presentation Layers
Status: draft

The next step in the project was to implement a service layer to make it easier to swap out the presentation layers. The service layer achieves this by acting as an abstraction between the domain logic and the presentation layer. This means the presentation layer will communicate with the service layer to initiate the required domain logic and the service layer will communicate with the persistence layer to retrieve the necessary data.

### Creating an In-memory Repository to Test the Service Layer

To make it easier to test the service layer I created concrete repositories for FitnessProfile and Workout domain entities. `FakeFitnessProfileRepository` and `FakeFitnessProfileRepository` can be passed test data which avoids using data from the actual persistence layer and affecting the state of the application.

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

### Creating the Service Layer

From my understanding the service layer contains all the functions or methods required to trigger the domain logic for a particular use case.

My use case was calculating individual work and rest interval distances for a particular conditioning workout. This involves the following steps:

Get the required `Workout object`
Get the required `FitnessProfiles`
Calculate the individual work and rest interval distances using the `Workout` and `FitnessProfile` objects
Return an output in the terminal that shows work and rest interval distances for each athlete
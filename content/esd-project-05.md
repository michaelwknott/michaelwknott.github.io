Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 5
Date: 2023-07-19 10:00
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing the Persistence Layer
Status: draft

## Implementing the Persistence Layer

With the basic domain logic in place I needed to load athlete fitness and workout data into memory. The first iteration of the project uses csv files as the persistence layer. Future iterations will require interacting with a database. To provide the ability to extend the functionality I used the Repository Pattern as an abstraction for the persistence layer.

### Abstract Repository

I decided to use an abstract base class (ABC) to create the abstraction layer. However, I'm aware that [pep 544](https://peps.python.org/pep-0544/) introduced Protocols and structural subtyping which could possibly be utilised in this case. This is an area I'll need to explore further to understand the specific use cases of Protocols.

The first challenge I faced related to the number of methods to create in the ABC. I have fitness assessment and workout records that I need to 'get', 'list' and 'add' from or to the persistence layer. I initially created the ABC with individual 'get', 'list' and 'add' methods for fitness assessment and workout records.

    :::python
    class AbstractRepository(ABC):
        """Interface for persistence layer."""

        @abstractmethod
        def get_profile(self, id: str) -> FitnessProfile:
            """Get a single FitnessProfile from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a get_profile method."
            )

        @abstractmethod
        def list_profiles(self) -> Sequence[FitnessProfile]:
            """Get a sequence of FitnessProfiles from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a list_profiles method."
            )

        @abstractmethod
        def add_profile(self, profile: FitnessProfile) -> None:
            """Add a single FitnessProfile record to persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a add_profile method"
            )

        @abstractmethod
        def add_profiles(self, profiles: Sequence[FitnessProfile]) -> None:
            """Add multiple FitnessProfiles to the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a add_profiles method"
            )

        @abstractmethod
        def get_workout(self, id: str) -> Workout:
            """Get a single Workout from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a get_workout method"
            )

        @abstractmethod
        def list_workouts(self, id: str) -> Sequence[Workout]:
            """Get multiple WOrkouts from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a list_workouts method"
            )

        @abstractmethod
        def add_workout(self, workout: Workout) -> None:
            """Add a single Workout to the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a add_workout method"
            )

        @abstractmethod
        def add_workouts(self, workouts: Sequence[Workout]) -> None:
            """Add multiple Workouts to the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a add_workouts method"
            )


However, I believe this created unnecessary duplication which could be removed through the addition of a parameter (`entity_type`) to the method signatures defining whether a fitness assessment or workout record was required. To ensure consistency of the arguments passed to the `entity_type` parameter I created a Enum.

    :::python
    class EntityType(Enum):
        """Represent the type of entity to be retrieved from persistence layer."""

        FITNESS_PROFILE = "fitness_profile"
        WORKOUT = "workout"


    class AbstractRepository(ABC):
        """Interface for persistence layer."""

        @abstractmethod
        def get(self, id: str, entity_type: EntityType) -> FitnessProfile | Workout:
            """Get a single entity from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a get method."
            )

        @abstractmethod
        def get_all(self, entity_type: EntityType) -> Sequence[FitnessProfile | Workout]:
            """Get a sequence of entities from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a list method."
            )

        @abstractmethod
        def add(self, entity_type: EntityType, entity: FitnessProfile | Workout) -> None:
            """Add a single entity record to persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement an add method."
            )

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

The groupby function from itertools may be useful here.
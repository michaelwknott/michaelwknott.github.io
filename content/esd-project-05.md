Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 5
Date: 2023-07-27 13:15
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Implementing the Repository Pattern for the Persistence Layer
Status: published

## Implementing the Repository Pattern

With the basic domain logic in place I needed to load athlete fitness and workout data into memory. The first iteration of the project uses csv files as the persistence layer. Future iterations will require interacting with a database. To provide the ability to extend the functionality I used the Repository Pattern as an abstraction for the persistence layer.

### Abstract Repository: Iteration 1

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


### Abstract Repository: Iteration 2

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

### Abstract Repository: Iteration 3

I felt uncomfortable with my implementation of the `AbstractRepository`. I wasn't sure whether I should create a generic abstraction or a separate abstraction for each of the domain objects (`FitnessProfile` and `Workout`). Further research revealed that I needed to create a generic AbstractRepository that could be used to create a concrete repository (a repository class that is instantiated) for each domain object. This resulted in the following implementation:


    :::python
    Entity = TypeVar("Entity", FitnessProfile, Workout)


    class AbstractRepository(ABC):
        """Interface for persistence layer."""

        @abstractmethod
        def get(self, id: str) -> Entity:
            """Get a single entity from the persistence layer."""
            raise NotImplementedError("Persistence layer needs to implement a get method.")

        @abstractmethod
        def get_all(self) -> Sequence[Entity]:
            """Get a sequence of entities from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a get_all method."
            )

        @abstractmethod
        def add(self, entity: Entity) -> None:
            """Add a single entity record to persistence layer."""
            raise NotImplementedError("Persistence layer needs to implement an add method")


### Abstract Repository: Iteration 4

In the third iteration of `AbstractRepository` I used `typing.TypeVar` to define a new type that would allow either a `FitnessProfile` or `Workout` type. Although `FitnessProfile` or `Workout` are the only domain objects that currently exist in the project, I wanted to ensure that `AbstractRepository` could accept additional types at a later date.

To achieve this I created a generic type `T` which I used in the `AbstractRepository` class definition. This means that any subclass of `AbstractRepository` will work with a specific type of entity defined by `T`.

    :::python
    T = TypeVar("T")


    class AbstractRepository(ABC, Generic[T]):
        """Interface for persistence layer."""

        @abstractmethod
        def get(self, id: str) -> T:
            """Get a single entity from the persistence layer."""
            raise NotImplementedError("Persistence layer needs to implement a get method.")

        @abstractmethod
        def get_all(self) -> Sequence[T]:
            """Get a sequence of entities from the persistence layer."""
            raise NotImplementedError(
                "Persistence layer needs to implement a get_all method."
            )

        @abstractmethod
        def add(self, entity: T) -> None:
            """Add a single entity record to persistence layer."""
            raise NotImplementedError("Persistence layer needs to implement an add method.")

As an example, if we have a `CSVFitnessProfileRepository` that implements the `AbstractRepository` interface I can define it as follows:


    :::python
    class CsvFitnessProfileRepository(AbstractRepository[FitnessProfile]):
        """CSV implementation of FitnessProfile repository."""

        def __init__(self, folder: str):
            """Initialise CsvRepository with fitness profiles.

            Args:
                folder: The directory path for the folder containing the CSV files.
            """
            self._filepath = Path(folder) / "fitness_assessments.csv"
            self._fitness_profiles: list[FitnessProfile] = []
            self._load()

        def _load(self):
            # logic to load csv data

        def get(self, id: str) -> FitnessProfile:
            """Get a single entity from the persistence layer."""
            pass

        def get_all(self) -> Sequence[FitnessProfile]:
            """Get a sequence of entities from the persistence layer."""
            pass

        def add(self, entity: FitnessProfile) -> None:
            """Add a single entity record to persistence layer."""
            pass


By passing `AbstractRepository[FitnessProfile]` in the class definition, the repository expects to work with objects of type `FitnessProfile`. The simple change from `Entity = TypeVar("Entity", FitnessProfile, Workout)` to `T = TypeVar("T")` provides the extensibility to create concrete repositories if new domain objects/entities are created without changing existing code.

The following GitHub [issue](https://github.com/michaelwknott/esd/issues/15) outlines the progression in my thought patterns and provides links to useful blog post that supported the above implementation of the Repository pattern.

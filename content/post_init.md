Title: TIL: Using `__post_init__` with Python Dataclasses 
Date: 2023-08-02 12:30
Category: Python
Tags: TIL, Python, dataclass
Authors: Michael Knott
Summary: Using `__post_init__` to initiate dependent fields
Status: Published

## dataclass `__post_init__`

Today I learnt that you can use `__post_init__` to initiate fields that depend upon other fields within a dataclass.

Within a project I'm currently working on I have the following dataclass:

    :::python
    from dataclasses import dataclass

    @dataclass
    class FitnessProfile:
        """Represents an athlete's fitness profile.

        Attributes:
            name: A str of the athlete's name.
            time_trial_distance: An int of the time trial distance in meters.
            time_trial_time: An int of the time taken to complete the 2km time trial.

        Properties:
            max_aerobic_speed: A float representing MAS in meters per second.
        """

        name: str
        time_trial_distance: int
        time_trial_time: int

        @property
        def max_aerobic_speed(self) -> float:
            """Maximal Aerobic Speed in m/s (rounded to 2 decimal places)."""
            if self.time_trial_time != 0:
                return round(self.time_trial_distance / self.time_trial_time, 2)
            else:
                return 0

Within the `FitnessProfile` I'm using a property to dynamically calculate `max_aerobic_speed` which depends upon the `time_trial_distance` and `time_trial_time` fields in the dataclass. 

    :::bash
    >>> from post_init import FitnessProfile
    >>> profile = FitnessProfile("John Smith", 2000, 480,)
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=480)
    >>> profile.max_aerobic_speed
    4.17

Using a property means that if either `time_trial_distance` or `time_trial_time` are updated after an instance is instantiated then `max_aerobic_speed` will use the updated values to provide an updated value.

    :::bash
    # current profile
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=480)
    
    # update time_trial_time
    >>> profile.time_trial_time = 450
    
    # updated profile with new time_trial_time
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=450)
    
    # max_aerobic_speed using updated time_trial_time
    >>> profile.max_aerobic_speed
    4.44

However, within the current project I'm not going to be updating fields within `FitnessProfile` once the dataclass instance has been instantiated. Therefore an alternative is to use the `__post_init__` to initialise the `max_aerobic_speed` field.

    :::python
    from dataclasses import dataclass, field

    @dataclass
    class FitnessProfile:
        """Represents an athlete's fitness profile.

        Attributes:
            name: A str of the athlete's name.
            time_trial_distance: An int of the time trial distance in meters.
            time_trial_time: An int of the time taken to complete the 2km time trial.
            max_aerobic_speed: A float representing MAS in meters per second.
        """

        name: str
        time_trial_distance: int
        time_trial_time: int
        max_aerobic_speed: float = field(init=False)

        def __post_init__(self):
            self.max_aerobic_speed = round(self.time_trial_distance / self.time_trial_time, 2)

Using the updated `FitnessProfile`:

    :::bash
    >>> from post_init import FitnessProfile
    >>> profile = FitnessProfile("John Smith", 2000, 480)
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=480, max_aerobic_speed=4.17)

This is fine for my use case but be aware that if I update either `time_trial_distance` or `time_trial_time` then `max_aerobic_speed` won't be updated using the new field values:

    :::bash
    # initial profile
    >>> profile = FitnessProfile("John Smith", 2000, 480)
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=480, max_aerobic_speed=4.17)
    
    # update time_trial_time
    >>> profile.time_trial_time = 450
    
    # updated profile with new time_trial_time
    >>> profile
    FitnessProfile(name='John Smith', time_trial_distance=2000, time_trial_time=450, max_aerobic_speed=4.17)
    
    # unchanged max_aerobic_speed field
    >>> profile.max_aerobic_speed
    4.17

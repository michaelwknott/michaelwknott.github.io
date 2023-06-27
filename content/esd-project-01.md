Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 1
Date: 2023-06-23 11:30
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Project Overview
Status: published

## Upskilling in Python
I've been using Python for approximately two years. I feel comfortable with the basics and creating projects for myself. To take the next step I believe I need to create projects which allow collaboration with other developers and involve users other than myself.

I've recently been reading [Practices of the Python Pro](https://thepythonpro.com/) by Dane Hillard and [Architecture Patterns with Python](https://www.cosmicpython.com/book/preface.html) by Harry Percival and Bob Gregory. Both books outline key principles, techniques and design patterns for developing Python applications. My plan is to utilise the ideas outlined in this book whilst developing my next project. I realise this may result in over-engineering of the project but I believe this is acceptable to further my knowledge and skills.  

### Project Overview
Within my current role I support several athletes that require the prescription of conditioning sessions as part of their training plan. To provide effective support involves three tasks:

1. Recording assessment data related to athlete's fitness qualities
2. Providing feedback to athletes and coaches on fitness progression
3. Prescribing individulised conditioning sessions based upon assessment results

Currently the process takes a number of steps involving multiple Excel workbooks and a lot of copy and paste.

The goal of this project is to streamline and automate the process to save me time, whilst also improving my knowledge of software design patterns and techniques. As a first iteration the application will need to provide the following functionality: 

+ Store athlete data for a variety of assessment results (1km, 2km, 3km and 5m times)
+ Calculate fitness metrics from assessment results such as Critical Speed, Maximal Aerobic Speed and Maximal Sprinting Speed
+ Provided a summary overview of fitness progression for athlete and coaches
+ Prescribe conditioning sessions and individualise target distances or target paces for each athlete
+ Create a downloadable sheet of each athlete's target distance/pace to be used during conditioning session set-up

However, I want ot ensure that I structure the project in an appropriate manner to extend it's functionality at a later date if additional functionality is required.

## Project Structure
I plan to use a three-layered architecture for the project. The three layers consist of a presentation layer to interface with the user, a business model layer containing the logic to implement the required workflows associated with monitoring and prescribing individualised conditioning sessions and a persistance layer to store the required data.

![Three layered architecture]({static}/images/three_layered_architecture.png "Three layered architecture"){style="display: block; margin: 0 auto"}

For the first version of the project I'm going to create an API for the presentation layer and utilise a relational database for the persistence layer. I'm aiming to create an interface between the business logic layer and the presentation and persistence layers to provide the ability to switch between components. For example, create a CLI for the presentation layer or utilise csv files for the persistence layer.

As a starting point I believe it will be best to develop the business logic. In [part 2](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions:-part-2.html) this is where i will start.
# NEAT_Mario_and_Luigi

This project implements a NEAT (NeuroEvolution of Augmenting Topologies) algorithm to play the game, Mario and Luigi: Partners In Time. Its task is specifically hard-coded to perfect the game's "copy flower" item where incoming Mario, Luigi, Baby Mario, or Baby Luigi (abbreviated to `MLBMBL` for the rest of the `README.md`) sprites run and jump on the enemy. The agent must press the corresponding button for each `MLBMBL` sprite at a precise window of time. The timing/difficulty window is made to increase for every successful button command. 

[A speedrun example.](https://www.youtube.com/watch?v=3LJ9qQpR4jI&ab_channel=Migu)

## Project Overview

NEAT is a genetic algorithm-based technique for evolving neural networks, similarly inspired by human evolution or natural selection. A NEAT algorithm starts with a population of very simple neural networks. Each neural network in the population is evaluated on a task, and the performance of each network is assessed based on some predefined criteria called the fitness. After one training iteration or generation of this population, the best networks or the "most fit" are chosen to crossover and mutate a new neural network for the next generation. This entire process iterates for X generations.

We will apply this theory to Mario and Luigi: Partners In Time where each neural network is an agent playing the copy flower item. The goal is to obtain the optimal agent that can top the speed run example above or destroy the boss in a single copy flower combo string!

## Implementation

The `main` project script is executed while a Mario and Luigi: Partners In Time game window is open. This project uses an emulator to play the game (which unfortunately means that the game is not running on its original source nor do we have access to in-game data).

Part of the training for the NEAT algorithm relies on input data, such as sprite positional data and game state data. Since we do not have access to this precise data, another portion of the project heavily relies on computer vision to track every frame on the game window to obtain in-game data for our neural networks.

To outline the requirements for this project, we need:
- A computer vision algorithm to track game states
- A NEAT algorithm where each neural network takes in-game data as an input to predict a controller button presses (ex. `A`, `B`, `X`, `Y`, or none).

### Computer Vision

### NEAT
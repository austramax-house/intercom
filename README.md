# Austramax Intercom

This repository houses the source code for the custom-built intercom for 
[Austramax House](https://austramax.house). 

> [!WARNING]
> This whole project is an active work in progress, very much including this readme. Over time I aim to expand both the documentation and functionality to make it even easier to try to build one for yourself.

## Hardware

The main hardware consists of:
- 1 x Raspberry Pi Pico 2 W
- 30 x momentary switches
- 14 x 1K Ohm resistors
- 3 x 100 Ohm resistors
- 1 x {part no} MOSFET
- 1 x piezo buzzer
- 1 x HxWmm prototyping board
- 1 x HxWmm prototyping board

...and various offsets, screws, printed, and laser cut parts.

## Software

The firmware for this device is written in MicroPython, with the help of the MicroPico extension for VSCode. 

With the exception of the `umqtt` library, all other code is implemented directly without the use of external libraries. 

## Architecture

In order to make the most of the development efforts of this project, I've set the long-term objective to be a consumer-ready user experience.

To not sweat the big stuff too early, I've focussed and reduced scope along the way, but the bones of a Finite State Machine-based architecture are in place.

These different states allow for transitioning between active components and keeping a clear and finite set of user pathways in focus.
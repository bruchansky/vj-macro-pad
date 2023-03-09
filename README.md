# Custom VJ Macro Pad (Raspberry Pi Pico)
These are instructions to build a macro pad for the Immersions VJ app on the iPad.

Get the app for free on the [App Store](https://apps.apple.com/app/immersions-vj/id6445908343).

Project homepage: [Immersions VJ](https://bruchansky.name/immersionsvj/)

## Hardware
- 1 Raspberry Pi Pico (about 5 euros)
- 1 Pico RGB Keypad Base (Pimoroni, about 20 euros)

## Installation
Instructions:
[pmk-circuitpython](https://github.com/pimoroni/pmk-circuitpython)

They are easy. Here are the libraries you should have installed on your Pico at the end of the process:
- adafruit_hid
- pmk

## Customization
Upload the code.py file to the root folder of your Pico.

The code:
- Assigns a function to each key (either when it is pressed once or continuously)
- Sets colors customised for the Immersions VJ app
- Animates key colors to reflect their function in the app (e.g. quick flashing light to increase bpm)

Future improvements:
- Update pad colors based on the theme and status of the app





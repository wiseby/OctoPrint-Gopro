# OctoPrint-Gopro

Do you have a GoPro Camera laying around? Tired of the low quality frames captured by your cheap webcam?
This plugin enables you to benefit from many of the good features the GoPro offers.
Its a simple plugin that will get a command to take a photo every time the timelapse evenmt is raised.
the best part is the wireless communications built in to the camera. The only connection necessary is the power (battery life will limit the length of the timelapse)

## Compatibility

- GoPro Hero 8

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/wiseby/OctoPrint-Gopro/archive/master.zip

## Configuration

Configure your raspberry by doing the steps in this [guide](https://github.com/KonradIT/goprowifihack/blob/master/Bluetooth/Platforms/RaspberryPi.md)-
You have to manually pair the GoPro the first time. Follow these steps:

- (Steps to pair with BlueZ)

- Initially you need to pair your GoPro
- set the presets for the photos captured

## Features for the future

- Automatic download on print-success and processing of timelapse (as the default functionality of OctoPrints timelapses)
- Support for more GoPro models (GoPro openapi only supports python >=3.8)

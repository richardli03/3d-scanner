# 3D Scanner

As part of our project for our Principles of Engineering class, we were tasked to build a 3D scanner with 2 servos, an IR-sensor and an Arduino R3.

The full report for this project can be read [here](https://drive.google.com/file/d/1EMQuUcNW2yjdMHRZvw1hTTl5di6LXwAG/view?usp=sharing)

This repository contains all of the software and Arduino firmware that this project needed to work. Running `main.py` will be able to reproduce our results with the existing datasets collected in "display.csv". The 3D mapping is accomplished using `matplotlib`'s heat mapping methods where darker colors correspond to closer points.
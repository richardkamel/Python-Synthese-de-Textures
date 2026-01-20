# Texture Synthesis – Python Image Processing Project

This project implements a texture synthesis algorithm in Python, allowing the generation of new textures from a small input sample.
The goal is to reproduce the visual appearance and statistical properties of an input texture while generating a larger synthetic image.

This project was developed as part of an academic image processing and computer vision course.

---

## Project Overview

Texture synthesis is a fundamental problem in image processing.
Given a small texture sample, the objective is to generate a new image that visually resembles the original texture without simply copying it.

The project focuses on:
- Neighborhood-based texture synthesis
- Pixel-by-pixel image generation
- Preservation of local spatial structures
- Visual coherence of synthesized textures

---

## Algorithm Description

The texture is synthesized by iteratively filling pixels in an output image based on similarity with neighborhoods from the source texture.

High-level steps:
1. Load a source texture image
2. Initialize an output image
3. For each pixel to synthesize:
   - Extract its local neighborhood
   - Search for similar neighborhoods in the source texture
   - Select the best matching candidate
   - Assign the corresponding pixel value
4. Repeat until the output image is fully generated

This approach preserves local patterns and texture consistency.

---

## Tech Stack

- Language: Python
- Libraries:
  - NumPy
  - OpenCV
  - Matplotlib
- Domain: Image processing, texture synthesis

---

## Input and Output

- Input: Small texture image (grayscale or color)
- Output: Larger synthesized texture image

The output preserves local visual patterns and the statistical distribution of the input texture.

---

## How to Run the Project

### Prerequisites
- Python 3.x
- pip

### Install dependencies
pip install -r requirements.txt

### Run the algorithm
python texture_synthesis.py

Input and output paths can be configured in the parameters file.

---

## Results

The algorithm generates visually coherent textures that resemble the input sample without exact repetition.
Results depend on neighborhood size, similarity thresholds, and output image dimensions.

---

## Limitations

- High computational cost for large images
- Sensitive to parameter tuning
- Performs best on stationary textures

---

## What I Learned

- Implementing texture synthesis algorithms from theory
- Working with neighborhoods and similarity metrics
- Manipulating images using NumPy and OpenCV
- Understanding the trade-off between quality and performance
- Debugging and optimizing numerical algorithms
- Evaluating visual results in image processing tasks

---

## Possible Improvements

- Patch-based synthesis instead of pixel-based
- Multi-resolution or pyramid-based synthesis
- Performance optimization and vectorization
- GPU acceleration
- Interactive parameter tuning

---

## Purpose

This project was developed to apply theoretical image processing concepts in a practical implementation and to gain hands-on experience with texture synthesis techniques.

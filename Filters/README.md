# Filters

This is an augmented reality project that generates an interactive portal within the camera feed using real-time hand tracking. Through a natural gesture, the user can toggle between 8 distinct visual filters rendered live inside the portal.

---

## Features

- Real-time hand tracking using MediaPipe Hands.
- Dynamically constructed perspective portal based on the index finger and thumb tips of both hands.
- Eight visual filters applied exclusively within the portal area.
- Gesture-based filter switching: bringing hands closer together triggers a transition to the next filter in the sequence.
- Hysteresis system to prevent accidental changes caused by hand tremors or tracking inaccuracies.

## Included Filters

| Filter | Description |
|--------|-------------|
| `filter_grid` | Grid overlay on the original image |
| `filter_duotone` | Duotone segmented by luminosity thresholds |
| `filter_halftone` | Black and white halftone pattern |
| `filter_chromatic_aberration` | Chromatic aberration with RGB channel separation |
| `filter_thermal` | Thermal camera simulation using a colormap |
| `filter_sepia` | Vintage sepia style with vignetting and grain |
| `filter_frosted_glass` | Frosted glass effect over the image |
| `filter_pink_halftone` | Pink-magenta duotone halftone | ## Installation

Clone the repository:

```bash
git clone 
cd Filters
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

With the camera active, raise both hands with your index fingers and thumbs extended; the portal is automatically generated between them. Bring your hands closer together to "close" the portal and advance to the next filter in the list. Press **`esc`** while the window is active to stop the program.

## Project Structure

```
Filters/
├── main.py            Entry point: capture loop and filter cycle
├── hand_tracking.py    Detection of extended fingers based on landmarks
├── geometry.py          Portal geometry and closing gesture detection
├── filters.py            Definitions for the eight available filters
├── requirements.txt
└── README.md
```

## Extending the Project

To add a new filter, simply define a function in `filters.py` that accepts a crop in BGR format (`numpy.ndarray`) and returns a crop of the same size:

```python
def filter_new(roi: np.ndarray) -> np.ndarray:
    return roi
```

Then, add it to the `FILTERS` list at the end of the file. The filter cycle automatically adjusts to the number of elements in that list.

## Tech Stack

- Python 3.10
- OpenCV
- MediaPipe
- NumPy

## License

This project is distributed under the MIT License.
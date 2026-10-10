# Phonocardiogram (PCG) Signal Processing

A Python application for basic processing of phonocardiogram (PCG) recordings. It loads a WAV audio file, applies a Butterworth band-pass filter, displays the original and filtered signals, and saves the processed audio and a comparison plot.

**This project is for educational purposes only and is not a medical diagnostic tool.**

## Features

- Select a WAV recording using a file dialog.
- Remove the signal's DC offset.
- Apply a fourth-order Butterworth band-pass filter (20–400 Hz).
- Visualize the original and filtered signals.
- Save the filtered WAV file and comparison plot automatically.

## Requirements

- Python 3.13 or a compatible Python version
- The dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Install the required packages:

   **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

## Downloading PCG recordings

The repository does not include audio recordings. You can download publicly available phonocardiogram recordings from the **CirCor DigiScope Phonocardiogram Dataset** on PhysioNet:

https://physionet.org/content/circor-heart-sound/1.0.3/

Download the dataset or an example WAV recording and place the WAV file in the `wavs/` folder.

Please follow the dataset's access and licensing terms and cite the dataset if you use it in academic work.

## Running the application

From the project directory, run:

```powershell
.\.venv\Scripts\python.exe pcg_filter.py
```

Select a WAV file in the file dialog. The application will display the original and filtered signals and save the output files after processing.

## Output

Generated files are saved in the `results/` folder:

- `*_filtered.wav` — filtered audio recording
- `*_comparison.png` — plot comparing the original and filtered signals

The `results/` folder is created automatically if it does not exist.

## Project structure

```text
pcg/
├── pcg_filter.py
├── requirements.txt
├── README.md
├── .gitignore
├── wavs/
│   └── README.md
└── results/
    └── README.md
```

## Disclaimer

This application demonstrates basic digital signal processing techniques. The output should not be used to diagnose or assess medical conditions.
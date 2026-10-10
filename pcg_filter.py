from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt


LOWCUT_HZ = 20.0
HIGHCUT_HZ = 400.0
FILTER_ORDER = 4


def process_pcg(input_path: str) -> tuple[Path, Path, dict]:
    """Read a WAV file, filter it, and save output WAV and comparison plot."""
    input_path = Path(input_path)
    signal, sample_rate = sf.read(input_path, always_2d=True)

    if signal.size == 0 or signal.shape[0] < 32:
        raise ValueError("Файлът е празен или съдържа твърде малко проби.")
    if sample_rate <= 2 * HIGHCUT_HZ:
        raise ValueError(
            f"Честотата на дискретизация ({sample_rate} Hz) трябва да е "
            f"по-висока от {2 * HIGHCUT_HZ} Hz за избраната горна гранична честота."
        )

    mono = np.mean(signal, axis=1)
    mono = mono - np.mean(mono) 


    sos = butter(
        FILTER_ORDER,
        [LOWCUT_HZ, HIGHCUT_HZ],
        btype="bandpass",
        fs=sample_rate,
        output="sos",
    )
    filtered = sosfiltfilt(sos, mono)

    project_dir = Path(__file__).resolve().parent
    results_dir = project_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    output_wav = results_dir / f"{input_path.stem}_filtered.wav"
    output_plot = results_dir / f"{input_path.stem}_comparison.png"
    
    sf.write(output_wav, filtered, sample_rate, subtype="PCM_16")

    duration = len(mono) / sample_rate
    time = np.arange(len(mono)) / sample_rate
    
    shown = min(len(time), int(10 * sample_rate))
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].plot(time[:shown], mono[:shown], linewidth=0.65)
    axes[0].set_title("Оригинален фонокардиографски сигнал")
    axes[0].set_ylabel("Амплитуда")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(time[:shown], filtered[:shown], linewidth=0.65)
    axes[1].set_title(f"Филтриран сигнал ({LOWCUT_HZ:.0f}–{HIGHCUT_HZ:.0f} Hz)")
    axes[1].set_xlabel("Време (s)")
    axes[1].set_ylabel("Амплитуда")
    axes[1].grid(True, alpha=0.3)
    fig.suptitle(f"Обработка на фонокардиограма — {input_path.name}")
    fig.tight_layout()
    fig.savefig(output_plot, dpi=160, bbox_inches="tight")
    plt.show()

    stats = {
        "sample_rate_hz": int(sample_rate),
        "duration_s": float(duration),
        "samples": int(len(mono)),
        "channels_in": int(signal.shape[1]),
        "rms_before": float(np.sqrt(np.mean(mono ** 2))),
        "rms_after": float(np.sqrt(np.mean(filtered ** 2))),
        "output_wav": str(output_wav),
        "output_plot": str(output_plot),
    }
    return output_wav, output_plot, stats


def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    project_dir = Path(__file__).resolve().parent
    wavs_dir = project_dir / "wavs"

    input_path = filedialog.askopenfilename(
        title="Изберете WAV файл със сърдечни тонове",
        initialdir=str(wavs_dir),
        filetypes=[("WAV аудио", "*.wav"), ("Всички файлове", "*.*")]
    )
    root.destroy()

    if not input_path:
        return
    try:
        output_wav, output_plot, stats = process_pcg(input_path)
        summary = (
            "Обработката приключи успешно.\n\n"
            f"Честота на дискретизация: {stats['sample_rate_hz']} Hz\n"
            f"Продължителност: {stats['duration_s']:.2f} s\n"
            f"Брой проби: {stats['samples']}\n"
            f"Входни канали: {stats['channels_in']}\n"
            f"RMS преди: {stats['rms_before']:.6f}\n"
            f"RMS след: {stats['rms_after']:.6f}\n\n"
            f"Записан сигнал:\n{output_wav}\n\n"
            f"Графика:\n{output_plot}\n\n"
            "Резултатите са за учебна демонстрация, не за медицинска диагноза."
        )
        messagebox.showinfo("Резултат", summary)
    except Exception as exc:
        messagebox.showerror("Грешка при обработката", str(exc))


if __name__ == "__main__":
    main()

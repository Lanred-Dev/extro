# The order of these imports DOES matter. Loading extro can cause a big hang betwen the first and second frame.
import time
import matplotlib.pyplot as pyplot
import psutil
import platform
import wmi
import extro

TIME_BETWEEN_CAPTURES: float = 0.1
X_TICKS: range = range(40)

started_capturing_at: float = 0
last_capture_at: float = 0
captures: dict[float, dict[str, float]] = {}
fps_captures: dict[float, float] = {}
post_render_connection: str | None = None


def take_capture():
    global last_capture_at, captures, fps_captures

    now: float = time.perf_counter()

    if now - last_capture_at < TIME_BETWEEN_CAPTURES:
        return

    last_capture_at = now

    captures[last_capture_at] = extro.Profiler.get_stats()
    fps_captures[last_capture_at] = extro.Profiler.get_fps()


def start_tracking(output_path: str, duration: float):
    print("Benchmarking started...")

    global post_render_connection, captures, started_capturing_at

    started_capturing_at = time.perf_counter()

    captures = {}
    post_render_connection = extro.Services.TimingService.on_post_render.connect(
        lambda: take_capture()
    )

    timeout = extro.Utils.Timeout(duration)
    timeout.on_finish.connect(lambda: stop_tracking(output_path))
    timeout.start()


def stop_tracking(output_path: str):
    print("Benchmarking complete. Cleaning up...")

    global post_render_connection

    if post_render_connection is not None:
        extro.Services.TimingService.on_post_render.disconnect(post_render_connection)
        post_render_connection = None

    print(f"Generating report at '{output_path}'...")

    formatted: dict[str, tuple[list[float], list[float]]] = {}

    for time, stats in captures.items():
        for system, response_time in stats.items():
            if system not in formatted:
                formatted[system] = ([], [])

            formatted[system][0].append(time - started_capturing_at)
            formatted[system][1].append(response_time)

    pyplot.figure(1, (14, 8))

    for system, (times, values) in formatted.items():
        pyplot.plot(times, values, label=system)

    pyplot.title("System Response Times")
    pyplot.xlabel("Time (s)")
    pyplot.ylabel("Response Time (ms)")
    pyplot.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    pyplot.tight_layout()
    pyplot.grid(True)
    pyplot.xticks(
        [
            i * (max(captures.keys()) - started_capturing_at) / len(X_TICKS)
            for i in X_TICKS
        ],
        [
            f"{i * (max(captures.keys()) - started_capturing_at) / len(X_TICKS):.1f}"
            for i in X_TICKS
        ],
    )
    pyplot.savefig(f"{output_path}/system_response_times.png", dpi=400)

    pyplot.figure(2, (14, 8))
    pyplot.title("FPS Over Time")
    pyplot.xlabel("Time (s)")
    pyplot.ylabel("Frames Per Second (FPS)")
    pyplot.plot(
        [time - started_capturing_at for time in fps_captures.keys()],
        list(fps_captures.values()),
        label="FPS",
        color="red",
    )
    pyplot.xticks(
        [
            index * (max(fps_captures.keys()) - started_capturing_at) / len(X_TICKS)
            for index in X_TICKS
        ],
        [
            f"{index * (max(fps_captures.keys()) - started_capturing_at) / len(X_TICKS):.1f}"
            for index in X_TICKS
        ],
    )
    pyplot.tight_layout()
    pyplot.grid(True)
    pyplot.savefig(f"{output_path}/fps.png", dpi=400)

    with open(f"{output_path}/report.md", "w") as report_file:
        report_file.write("# Benchmark Report\n\n")

        report_file.write(
            f"This benchmark ran for {max(captures.keys()) - started_capturing_at:.2f} seconds and captured {len(captures)} data points.\n\n"
        )

        report_file.write("### Average System Response Times\n\n")

        for system, (times, values) in formatted.items():
            average_time = sum(values) / len(values)
            report_file.write(f"- {system}: {average_time:.4f} ms\n")

        average_fps = sum(fps_captures.values()) / len(fps_captures)
        report_file.write(f"\nAverage FPS: {average_fps:.2f}\n\n")

        report_file.write("### System Specifications\n\n")

        report_file.write(f"- Platform: {platform.platform()}\n")
        report_file.write(f"- Processor: {platform.processor()}\n")
        report_file.write(f"- GPU: {wmi.WMI().Win32_VideoController()[0].Name}\n")
        report_file.write(
            f"- RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        )

    print("Done generating report.")
    print("Quitting...")

    extro.Engine.quit()

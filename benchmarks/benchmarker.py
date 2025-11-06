# The order of these imports DOES matter. Loading extro first can cause a big hang betwen the first and second frame.
import time
import matplotlib.pyplot as pyplot
import psutil
import platform
import wmi
import extro

TIME_BETWEEN_CAPTURES: float = 0.02
X_TICKS: range = range(40)
Y_TICKS: range = range(25)

started_capturing_at: float = 0
last_capture_at: float = 0
system_response_time_captures: dict[float, dict[str, float]] = {}
fps_captures: dict[float, float] = {}
hardware_usage_captures: dict[float, dict[str, float]] = {}
post_render_connection: str | None = None


def take_capture():
    global last_capture_at, system_response_time_captures, fps_captures, hardware_usage_captures

    now: float = time.perf_counter()

    if now - last_capture_at < TIME_BETWEEN_CAPTURES:
        return

    last_capture_at = now

    system_response_time_captures[last_capture_at] = extro.Profiler.get_averages()
    fps_captures[last_capture_at] = extro.Profiler.get_fps()
    hardware_usage_captures[last_capture_at] = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
    }


def generate_chart(
    title: str,
    xlabel: str,
    ylabel: str,
    data: dict[float, dict[str, float]],
    output_file: str,
    multiplier: float = 1.0,
):
    pyplot.figure(figsize=(14, 8))

    formatted_data = format_capture_data(data, multiplier)

    for system, values in formatted_data.items():
        times = list(values.keys())
        values = list(values.values())
        pyplot.plot(times, values, label=system, linewidth=2)

    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    pyplot.tight_layout()
    pyplot.grid(True)
    pyplot.xticks(
        [
            index * (max(data.keys()) - started_capturing_at) / len(X_TICKS)
            for index in X_TICKS
        ],
        [
            f"{index * (max(data.keys()) - started_capturing_at) / len(X_TICKS):.1f}"
            for index in X_TICKS
        ],
        rotation=45,
    )
    pyplot.yticks(
        [
            index
            * max(
                value for system in formatted_data.values() for value in system.values()
            )
            / len(Y_TICKS)
            for index in Y_TICKS
        ],
        [
            f"{index * max(value for system in formatted_data.values() for value in system.values()) / len(Y_TICKS):.1f}"
            for index in Y_TICKS
        ],
    )
    pyplot.margins(x=0, y=0.01)
    pyplot.savefig(output_file, dpi=400)


def format_capture_data(
    data: dict[float, dict[str, float]],
    multiplier: float = 1.0,
) -> dict[str, dict[float, float]]:
    formatted_data: dict[str, dict[float, float]] = {}

    for time, values in data.items():
        for key, value in values.items():
            if key not in formatted_data:
                formatted_data[key] = {}

            formatted_data[key][time - started_capturing_at] = value * multiplier

    return formatted_data


def start_tracking(
    output_path: str = "",
    duration: float | None = None,
    benchmark_info: dict[str, str] = {},
):
    print("Benchmarking started...")

    global post_render_connection, captures, started_capturing_at

    captures = {}
    started_capturing_at = time.perf_counter()
    post_render_connection = extro.Services.TimingService.on_post_render.connect(
        lambda: take_capture()
    )

    if duration is not None:
        timeout = extro.Utils.Timeout(duration)
        timeout.on_finish.connect(lambda: stop_tracking(output_path, benchmark_info))
        timeout.start()


def stop_tracking(output_path: str, benchmark_info: dict[str, str]):
    print("Benchmarking complete. Cleaning up...")

    global post_render_connection

    if post_render_connection is not None:
        extro.Services.TimingService.on_post_render.disconnect(post_render_connection)
        post_render_connection = None

    print(f"Generating report at '{output_path}'...")

    generate_chart(
        "System Response Times Over Time",
        "Time (s)",
        "Response Time (ms)",
        {
            time: {
                system: value for system, value in values.items() if system != "total"
            }
            for time, values in system_response_time_captures.items()
        },
        f"{output_path}/system_response_times.png",
        1000.0,
    )

    generate_chart(
        "FPS Over Time",
        "Time (s)",
        "Frames Per Second (FPS)",
        {time: {"FPS": fps} for time, fps in fps_captures.items()},
        f"{output_path}/fps.png",
    )

    generate_chart(
        "Hardware Usage Over Time",
        "Time (s)",
        "Usage (%)",
        hardware_usage_captures,
        f"{output_path}/hardware_usage.png",
    )

    with open(f"{output_path}/report.md", "w") as report_file:
        benchmark_name: str = benchmark_info.get("name", "Benchmark")
        benchmark_info.pop("name", None)

        report_file.write(f"# {benchmark_name} Report\n\n")

        report_file.write(
            f"This benchmark ran for {max(system_response_time_captures.keys()) - started_capturing_at:.2f} seconds and captured {len(system_response_time_captures)} data points.\n\n"
        )

        if len(benchmark_info) > 0:
            report_file.write("### Benchmark Information\n\n")

            for key, value in benchmark_info.items():
                report_file.write(f"- {key}: {value}\n")

            report_file.write("\n")

        report_file.write("### Average System Response Times\n\n")

        average_fps = sum(fps_captures.values()) / len(fps_captures)
        report_file.write(f"Average FPS: {average_fps:.2f}\n\n")

        for system, values in format_capture_data(
            system_response_time_captures,
            1000.0,
        ).items():
            average_time = sum(values.values()) / len(values)
            report_file.write(f"- {system}: {average_time:.2f} ms\n")

        report_file.write("\n")

        report_file.write("### System Specifications\n\n")

        report_file.write(f"- Platform: {platform.platform()}\n")
        report_file.write(f"- Processor: {platform.processor()}\n")
        report_file.write(f"- GPU: {wmi.WMI().Win32_VideoController()[0].Name}\n")
        report_file.write(
            f"- RAM: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB\n"
        )

        report_file.write("\n")

        report_file.write("### Charts\n\n")
        report_file.write("![System Response Times](system_response_times.png)\n\n")
        report_file.write("![FPS](fps.png)\n\n")
        report_file.write("![Hardware Usage](hardware_usage.png)\n\n")

    print("Done generating report.")
    print("Quitting...")

    extro.Engine.quit()


from collections import Counter
import csv

LOG_FILE = "sample.log"
REPORT_FILE = "report.csv"

def suggest_next_step(message):
    message = message.lower()

    if "database connection failed" in message:
        return (
            "Check database availability, hostname, port, "
            "and network connectivity."
        )

    elif "request timed out" in message:
        return (
            "Check service availability, network latency, "
            "and firewall rules."
        )

    elif "memory" in message:
        return (
            "Check memory usage, running processes, "
            "and recent workload changes."
        )

    elif "disk space" in message:
        return (
            "Check disk usage and identify large log or "
            "temporary files before taking action."
        )

    else:
        return (
            "Review surrounding log entries and recent "
            "system changes."
        )
def analyze_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{LOG_FILE}' was not found.")
        return
    except OSError as error:
        print(f"Could not read the input file: {error}")
        return

    log_levels = Counter()
    error_messages = Counter()
    total_lines = 0
    invalid_lines = 0


    for line in lines:
            line = line.strip()

            if not line:
                continue

            parts = line.split(" ", 3)

            if len(parts) < 4:
                invalid_lines += 1
                continue

            timestamp = parts[0] + " " + parts[1]
            level = parts[2]
            message = parts[3]

            if level not in {"INFO", "WARNING", "ERROR"}:
                invalid_lines += 1
                continue

            total_lines += 1
            log_levels[level] += 1

            if level == "ERROR":
                error_messages[message] += 1

    print("\n===== SERVER LOG ANALYSIS =====")
    print(f"Valid log entries: {total_lines}")
    print(f"Invalid entries: {invalid_lines}")

    print("\nLog level summary:")
    for level, count in sorted(log_levels.items()):
        print(f"{level}: {count}")

    print("\nMost frequent errors:")
    if error_messages:
        for message, count in error_messages.most_common():
            print(f"{message}: {count} time(s)")
    else:
        print("No errors found.")

        
    if error_messages:
        top_error, count = error_messages.most_common(1)[0]

        print("\n===== TROUBLESHOOTING INSIGHT =====")
        print(f"Most frequent error: {top_error}")
        print(f"Occurrences: {count}")
        print(f"Suggested next check: {suggest_next_step(top_error)}")

    
    try:
        with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Log Level", "Count"])

            for level, count in sorted(log_levels.items()):
                writer.writerow([level, count])

            writer.writerow([])
            writer.writerow(["Error Message", "Occurrences"])

            for message, count in error_messages.most_common():
                writer.writerow([message, count])

        print(f"\nReport saved to {REPORT_FILE}")

    except OSError as error:
        print(f"Could not save the report: {error}")

if __name__ == "__main__":
    analyze_logs()

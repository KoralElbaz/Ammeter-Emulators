def print_chart(measurements, title):
    print(f"\n--- Visualization for {title} ---")

    max_val = max(measurements)

    for i, val in enumerate(measurements):
        bar_length = int((val / max_val) * 50) if max_val != 0 else 0
        bar = "#" * bar_length
        print(f"{i:02d}: {bar} ({round(val, 4)})")
import matplotlib.pyplot as plt
import csv

prompts = []
times = []

with open("concurrency_results.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        prompts.append(row['prompt'])
        times.append(float(row['elapsed_time']))

plt.figure(figsize=(10, 6))
plt.bar(prompts, times, color='teal')
plt.xlabel("Prompt")
plt.ylabel("Time Taken (seconds)")
plt.title("Response Time per Concurrent Request")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.savefig("performance_plot.png")
plt.show()

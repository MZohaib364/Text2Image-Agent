# import requests
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time
# import csv

# URL = "http://localhost:8000/generate"

# def send_request(prompt):
#     payload = {
#         "context": "fantasy art",
#         "text": "a wizard casting fire in the sky"
#     }
#     start = time.time()
#     response = requests.post(URL, json=payload)
#     elapsed = time.time() - start
#     return {
#         "prompt": prompt,
#         "status": response.status_code,
#         "elapsed_time": elapsed
#     }

# def main():
#     prompts = [f"Prompt number {i}" for i in range(10)]

#     results = []
#     start_time = time.time()

#     with ThreadPoolExecutor(max_workers=10) as executor:
#         futures = [executor.submit(send_request, prompt) for prompt in prompts]
#         for future in as_completed(futures):
#             result = future.result()
#             print(f"Prompt: {result['prompt']} | Status: {result['status']} | Time Taken: {result['elapsed_time']:.2f}s")
#             results.append(result)

#     total_time = time.time() - start_time
#     print(f"\nTotal time for all concurrent requests: {total_time:.2f} seconds")

#     # Write to CSV
#     with open("concurrency_results.csv", mode="w", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=["prompt", "status", "elapsed_time"])
#         writer.writeheader()
#         writer.writerows(results)

#     print("Results saved to concurrency_results.csv")

# if __name__ == "__main__":
#     main()

import requests
import time
import threading
import csv
import matplotlib.pyplot as plt
import json

# Configuration for the REST API and number of concurrent requests
url = "http://localhost:8000/generate"
num_requests = 10  # Number of requests to simulate
concurrent_requests = 5  # Number of concurrent requests

# CSV file to log performance results
csv_file = "performance_log.csv"

# A list to store response times for visualization
response_times = []

# Function to send requests
def send_request(request_id):
    # Prepare the JSON payload for the request
    payload = {
        "context": "fantasy art",
        "text": "a wizard casting fire in the sky"
    }

    try:
        start_time = time.time()  # Record the start time
        response = requests.post(url, json=payload)
        response_time = time.time() - start_time  # Calculate the response time
        
        # Log response time and status to the CSV file
        log_to_csv(request_id, response_time, response.status_code)
        response_times.append(response_time)  # Store the response time for visualization

    except requests.exceptions.RequestException as e:
        print(f"Error occurred in request {request_id}: {e}")
        log_to_csv(request_id, 0, 500)  # Log error with a 500 status code (server error)

# Function to log performance data to a CSV file
def log_to_csv(request_id, response_time, status_code):
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([request_id, response_time, status_code])

# Function to run multiple requests concurrently
def run_concurrent_requests():
    threads = []
    for i in range(num_requests):
        thread = threading.Thread(target=send_request, args=(i+1,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Generate performance report after all requests are completed
    generate_performance_report()

# Function to generate a performance report with Matplotlib
def generate_performance_report():
    print("Generating performance report...")

    # Plot the response times
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(response_times) + 1), response_times, marker='o', linestyle='-', color='b', label='Response Time (seconds)')
    plt.xlabel('Request ID')
    plt.ylabel('Response Time (seconds)')
    plt.title('API Performance: Response Time per Request')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Create CSV file and add headers if it doesn't exist
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Request ID", "Response Time (seconds)", "Status Code"])

    # Run the concurrent requests
    run_concurrent_requests()

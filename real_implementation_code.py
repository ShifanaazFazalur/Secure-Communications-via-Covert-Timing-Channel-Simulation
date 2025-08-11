import numpy as np
from scipy.stats import uniform

def simulate_buffer(Ipd_distribution, B=20, m_len=[16, 32], i_size=[2, 6, 10, 14, 18], experiments=1000):
   results = []  # Store results for underflow, overflow, success
  
   for m in m_len:  # Iterate over message sizes
       for i in i_size:  # Iterate over initial buffer sizes
           underflow = 0
           overflow = 0
           success = 0

           for _ in range(experiments):
               buffer = i  # Initialize buffer
               message = np.random.randint(0, 2, size=m)  # Generate a random message


               # Generate inter-packet delays based on the chosen distribution
               if Ipd_distribution.lower() == "exponential":
                   ipd = np.random.exponential(scale=1, size=m)  # Exp(1) distribution
                   ipd = np.clip(ipd, 0, 5)  # Limit range
                   min_delay, max_delay, median_delay = 0, np.max(ipd), np.log(2)  # Exp(1) median
               elif Ipd_distribution.lower() == "uniform":
                   ipd = uniform.rvs(0, 2, size=m)  # Uniform(0,2) distribution
                   min_delay, max_delay, median_delay = np.min(ipd), np.max(ipd), np.median(ipd)
               else:
                   print(f"Invalid distribution: {Ipd_distribution}. Using default 'Exponential'.")
                   ipd = np.random.exponential(scale=1, size=m)  # Default to exponential
                   ipd = np.clip(ipd, 0, 5)
                   min_delay, max_delay, median_delay = 0, np.max(ipd), np.log(2)


               for bit in message:
                   # Encode the bit using inter-packet delay modulation
                   if bit == 0:
                       delay = uniform.rvs(min_delay, median_delay - min_delay)  # Sample from [min, median]
                   else:
                       delay = uniform.rvs(median_delay, max_delay - median_delay)  # Sample from [median, max]


                   # Fix arrivals calculation using Poisson process
                   arrivals = np.random.poisson(delay)  # Arrivals should be an integer count
                   buffer += arrivals  # Add arriving packets
                   buffer -= 1  # Send a packet


                   # Check for underflow and overflow
                   if buffer < 0:
                       underflow += 1
                       break
                   elif buffer > B:
                       overflow += 1
                       break
               else:
                   success += 1  # Successful transmission


           # Store probabilities
           results.append([m, i, underflow / experiments, overflow / experiments, success / experiments])


   return results

# Function to print results
def print_results(results, distribution):
   print(f"\nSource Distribution = {distribution.capitalize()}")
   print("M Size      i             Underflow         Overflow      Success")
   for row in results:
       print(f"{row[0]:<12}{row[1]:<12}{row[2]:<18.3f}{row[3]:<16.3f}{row[4]:<10.3f}")
   print()


# Get user input for distribution type
distribution_choice = input("Enter the source distribution ('Exponential' or 'Uniform'): ").strip()


# Get user input for i values (initial buffer sizes)
i_values = input("Enter initial buffer sizes (comma-separated, e.g., 2,6,10,14,18): ").strip()
i_values = list(map(int, i_values.split(',')))


# Get user input for m sizes (message sizes)
m_values = input("Enter message sizes (comma-separated, e.g., 16,32): ").strip()
m_values = list(map(int, m_values.split(',')))

# Run simulation based on user input
results = simulate_buffer(distribution_choice, i_size=i_values, m_len=m_values)

# Print results
print_results(results, distribution_choice)


#Resources: 
# 1. Map function: https://www.geeksforgeeks.org/python-map-function/
# 2. Strip function: https://www.geeksforgeeks.org/numpy-string-operations-strip-function/
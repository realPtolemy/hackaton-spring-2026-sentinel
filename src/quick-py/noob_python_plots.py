import matplotlib.pyplot as plt
import random
import math

x_values = []
y_values = []
y_values_2 = []
y_values_3 = []
moving_avg = []

count = 0
limit = 100

while count < limit:
    x_values.append(count)
    
    val1 = math.sin(count * 0.1) * 10
    rand_factor = random.random() * 5
    final_val1 = val1 + rand_factor
    y_values.append(final_val1)
    
    val2 = count * 0.5
    val2 = val2 * val2
    val2 = val2 / 100
    y_values_2.append(val2)
    
    val3 = math.cos(count * 0.2) * 20
    if val3 < 0:
        val3 = val3 * -1
    y_values_3.append(val3)
    
    count = count + 1

print("generated data lists")

i = 0
while i < len(y_values):
    current_sum = 0
    num_items = 0
    j = i - 5
    while j < i + 5:
        if j >= 0:
            if j < len(y_values):
                current_sum = current_sum + y_values[j]
                num_items = num_items + 1
        j = j + 1
    
    if num_items > 0:
        average = current_sum / num_items
        moving_avg.append(average)
    else:
        moving_avg.append(0)
    
    i = i + 1

print("calculated averages")

max_val = 0
max_idx = 0
k = 0
for item in y_values:
    if item > max_val:
        max_val = item
        max_idx = k
    k = k + 1

print("found the max value")
print(max_val)

plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
plt.plot(x_values, y_values, "go--")
plt.title("Noisy Sine Wave")
plt.xlabel("time")
plt.ylabel("amplitude")

plt.subplot(2, 2, 2)
plt.plot(x_values, y_values_2, color="red", linewidth=3)
plt.plot(x_values, moving_avg, color="blue")
plt.legend(["Parabola thing", "The Average"])
plt.title("Math Stuff")

plt.subplot(2, 2, 3)
plt.bar(x_values[0:20], y_values_3[0:20])
plt.title("Absolute Cosine (First 20)")

plt.subplot(2, 2, 4)
plt.scatter(y_values, y_values_3, alpha=0.5, c="purple")
plt.text(5, 15, "scatter plot area")
plt.grid(True)
plt.title("Correlation check")

plt.suptitle("MY COMPLEX DATA ANALYSIS PROJECT")

plt.tight_layout()
plt.show()


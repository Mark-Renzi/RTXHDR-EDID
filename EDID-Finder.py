import numpy as np
import matplotlib.pyplot as plt

x_data = np.array([97, 98, 100, 110, 120, 130, 140, 160, 180, 200, 220, 240, 255])
y_data = np.array([408, 417, 436, 541, 672, 835, 1037, 1600, 2467, 3805, 5869, 9051, 12526])

# Polynomial fit
poly_coeffs = np.polyfit(x_data, y_data, deg=5)
poly_func = np.poly1d(poly_coeffs)

# Save to file (choose either .npy or .txt)
np.save("polynomial_coeffs.npy", poly_coeffs)
np.savetxt("polynomial_coeffs.txt", poly_coeffs)

# Optional: print the equation
print("Polynomial coefficients saved:")
print(poly_func)

print(f"Predicted at EDID 97: {poly_func(97):.2f} nits (expected: 408)")


# (Optional) visualize
x_fit = np.linspace(97, 255, 300)
plt.figure(figsize=(8, 5))
plt.scatter(x_data, y_data, color='red', label='Measured Data')
plt.plot(x_fit, poly_func(x_fit), color='blue', label='Polynomial Fit')
plt.title('Polynomial Fit of NVIDIA HDR Brightness')
plt.xlabel('EDID Max Luminance')
plt.ylabel('NVIDIA Reported Brightness (nits)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

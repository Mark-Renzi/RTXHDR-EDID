import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

x_data = np.array([97, 98, 100, 110, 120, 130, 140, 160, 180, 200, 220, 240, 255])
y_data = np.array([408, 417, 436, 541, 672, 835, 1037, 1600, 2467, 3805, 5869, 9051, 12526])

# Power function model with vertical offset: y = a * x^b + c
def power_func_offset(x, a, b, c):
    return a * np.power(x, b) + c

# Polynomial model: y = a*x^4 + b*x^3 + c*x^2 + d*x + e
poly_coeffs = np.polyfit(x_data, y_data, deg=5)
poly_func = np.poly1d(poly_coeffs)

# Power fit with offset
params_power_offset, _ = curve_fit(power_func_offset, x_data, y_data, maxfev=10000)
y_fit_power_offset = power_func_offset(x_data, *params_power_offset)
r2_power_offset = r2_score(y_data, y_fit_power_offset)

# Polynomial fit
y_fit_poly = poly_func(x_data)
r2_poly = r2_score(y_data, y_fit_poly)

x_fit = np.linspace(97, 255, 500)
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, color='red', label='Measured Data')
plt.plot(x_fit, poly_func(x_fit), label=f'Polynomial Fit (deg=3), R²={r2_poly:.4f}', color='blue')
plt.plot(x_fit, power_func_offset(x_fit, *params_power_offset), 
         label=f'Power Fit with Offset, R²={r2_power_offset:.4f}', color='green', linestyle='dashed')

plt.xlabel('EDID Max Luminance')
plt.ylabel('NVIDIA Reported Peak Brightness (nits)')
plt.title('Curve Fitting: EDID Max Luminance → NVIDIA HDR Brightness')
plt.legend()
plt.grid(True)
plt.ylim(0, max(y_data)*1.1)
plt.tight_layout()
plt.show()

print("\nEstimated Brightness (Polynomial Fit):")
for val in range(60, 150, 10):
    est = poly_func(val)
    print(f"  EDID {val:>3} → {est:7.1f} nits")

print("\nEstimated Brightness (Power Fit with Offset):")
for val in range(60, 150, 10):
    est = power_func_offset(val, *params_power_offset)
    print(f"  EDID {val:>3} → {est:7.1f} nits")

print(f"\nPower fit parameters: a={params_power_offset[0]:.4e}, b={params_power_offset[1]:.4f}, c={params_power_offset[2]:.4f}")

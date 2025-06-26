import numpy as np
from scipy.optimize import root_scalar

coeffs = np.load("polynomial_coeffs.npy")
poly = np.poly1d(coeffs)

x_min, x_max = 64, 255

target_brightness = float(input("Enter desired NVIDIA peak brightness in nits (e.g. 700): "))

full_range = np.arange(x_min, x_max + 1)
brightness_values = poly(full_range)
min_output = brightness_values.min()
max_output = brightness_values.max()

if not (min_output <= target_brightness <= max_output):
    print(f"\n❌ The target brightness {target_brightness:.1f} nits is out of range.")
    print(f"   Valid brightness range: {min_output:.1f} – {max_output:.1f} nits")
else:
    def func(x):
        return poly(x) - target_brightness

    bracket_found = False
    for i in range(x_min, x_max):
        x0, x1 = i, i + 1
        f0, f1 = func(x0), func(x1)
        if f0 * f1 < 0:  # Sign change: valid bracket
            bracket = [x0, x1]
            bracket_found = True
            break

    if not bracket_found:
        print("⚠️  Could not find a valid EDID value — no sign change detected in polynomial.")
    else:
        # Solve within bracket
        result = root_scalar(func, bracket=bracket, method='brentq')

        if result.converged:
            edid_float = result.root
            print(f"\n✅ Exact EDID Max Luminance for {target_brightness:.1f} nits: {edid_float:.2f}")

            # Closest integer EDIDs
            edid_lower = int(np.floor(edid_float))
            edid_upper = int(np.ceil(edid_float))

            # Clamp within valid range
            edid_lower = max(x_min, min(edid_lower, x_max))
            edid_upper = max(x_min, min(edid_upper, x_max))

            # Compute and sort by closeness
            candidates = [(edid_lower, abs(edid_float - edid_lower)), (edid_upper, abs(edid_float - edid_upper))]
            candidates.sort(key=lambda x: x[1])

            lowest_edid = 255
            for edid_val, dist in candidates:
                brightness = poly(edid_val)
                print(f"Closest EDID integer: {edid_val} → Estimated brightness: {brightness:.1f} nits (distance {dist:.2f})")
                if edid_val < lowest_edid:
                    lowest_edid = edid_val
            if lowest_edid < 97:
                print("⚠️  The NVIDIA App will not show you brightness controls when EDID Max Luminance is < 97.")
        else:
            print("⚠️  Root solver failed to converge within the valid bracket.")

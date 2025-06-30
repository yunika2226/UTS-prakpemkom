import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from mpl_toolkits.mplot3d import Axes3D

# Fungsi posisi vektor r(t)
def r(t):
    return np.array([t, np.sin(t), np.cos(t)])

# Fungsi kecepatan vektor v(t)
def v(t):
    return np.array([1, np.cos(t), -np.sin(t)])

# Fungsi percepatan vektor a(t)
def a(t):
    return np.array([0, -np.sin(t), -np.cos(t)])

# Fungsi magnitude kecepatan untuk panjang lintasan
def v_magnitude(t):
    v_vec = v(t)
    return np.linalg.norm(v_vec)  # √(1 + cos²(t) + sin²(t)) = √2

# Interval waktu
a_val, b_val = 0, 2*np.pi

# Hitung panjang lintasan
s, _ = quad(v_magnitude, a_val, b_val)
print(f"Panjang lintasan dari t = {a_val:.2f} hingga t = {b_val:.2f} adalah {s:.3f}")

# Buat array t untuk plotting
t_vals = np.linspace(a_val, b_val, 500)
r_vals = np.array([r(t) for t in t_vals])

# Ambil komponen x, y, z
x_vals, y_vals, z_vals = r_vals[:,0], r_vals[:,1], r_vals[:,2]

# Plot lintasan 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_vals, y_vals, z_vals, label='Lintasan r(t)', color='blue')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Grafik Lintasan Vektor r(t)')
ax.legend()
plt.tight_layout()
plt.show()

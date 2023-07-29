import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats

# Function to calculate the power of the hypothesis test
def calculate_power(sample_size, significance_level, effect_size):
    null_hypothesis_value = 0.5
    alt_hypothesis_value = null_hypothesis_value + effect_size
    z_critical = stats.norm.ppf(1 - significance_level / 2)

    standard_error = np.sqrt((null_hypothesis_value * (1 - null_hypothesis_value)) / sample_size)
    difference = np.abs(null_hypothesis_value - alt_hypothesis_value)
    z_effect = difference / standard_error

    power = 1 - stats.norm.cdf(z_effect - z_critical) + stats.norm.cdf(-z_effect - z_critical)
    return power

# Generate a range of sample sizes, significance levels, and effect sizes
sample_sizes = np.arange(10, 201, 10)
significance_levels = np.linspace(0.001, 0.05, 20)
effect_sizes = np.linspace(0.1, 1.0, 20)

# Calculate the power for each combination of sample size, significance level, and effect size
power_values = np.zeros((len(sample_sizes), len(significance_levels), len(effect_sizes)))
for i, sample_size in enumerate(sample_sizes):
    for j, significance_level in enumerate(significance_levels):
        for k, effect_size in enumerate(effect_sizes):
            power_values[i, j, k] = calculate_power(sample_size, significance_level, effect_size)

# Create meshgrid for heatmap plotting
significance_grid, sample_size_grid, effect_size_grid = np.meshgrid(significance_levels, sample_sizes, effect_sizes, indexing='ij')

# Flatten the grids for plotting
significance_flat = significance_grid.flatten()
sample_size_flat = sample_size_grid.flatten()
effect_size_flat = effect_size_grid.flatten()
power_flat = power_values.flatten()

# Create the heatmap plot
fig = px.scatter_3d(x=significance_flat, y=sample_size_flat, z=effect_size_flat, color=power_flat,
                    color_continuous_scale='Viridis', opacity=0.8)

# Layout customization
fig.update_layout(
    scene=dict(
        xaxis_title='Significance Level',
        yaxis_title='Sample Size',
        zaxis_title='Effect Size',
        xaxis=dict(tickformat='.3f'),
        yaxis=dict(tickvals=sample_sizes, ticktext=[f'Size {size}' for size in sample_sizes]),
        zaxis=dict(tickformat='.2f'),
        xaxis_ticksuffix='',
        zaxis_ticksuffix='',
        camera=dict(eye=dict(x=1.2, y=-1.2, z=0.8)),  # Camera angle
    ),
    title={
        'text': 'Statistical Power as a Function of Significance Level, Sample Size, and Effect Size',
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=18)
    },
    font=dict(family='Arial', size=12, color='black'),
    margin=dict(l=70, r=40, t=80, b=70),  # Margins to adjust the plot position
)

# Show the interactive 3D scatter plot
fig.show()


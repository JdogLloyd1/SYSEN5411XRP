# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 27, 2025

# Goal:
# Task C1 - Export plots of raw vs filtered data to assess noise reduction vs lag for different alpha values

import time
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def _resolve_path(fname: str):
	"""Resolve a filename to an existing path.

	Tries (in order):
	- If fname is absolute and exists, return it.
	- If fname exists in the current working directory, return its abs path.
	- If fname exists in the same directory as this script, return that path.
	Otherwise raise FileNotFoundError.

	This makes the loader robust when run from different CWDs or by tools.
	"""
	# Try given path, then script directory
	if os.path.isabs(fname) and os.path.exists(fname):
		return fname
	if os.path.exists(fname):
		return os.path.abspath(fname)
	script_dir = os.path.dirname(__file__)
	alt = os.path.join(script_dir, fname)
	if os.path.exists(alt):
		return alt
	raise FileNotFoundError(f"Could not find {fname} in CWD or script dir")


def load_imu_csv(fname: str):
	"""Load an IMU CSV into a pandas DataFrame and normalize types.

	Parameters
	----------
	fname : str
		Path or filename of CSV. Resolved using _resolve_path.

	Returns
	-------
	pd.DataFrame
		DataFrame with numeric columns coerced, a t_s column (seconds), and any
		missing expected columns filled with NaN.

	Notes
	-----
	This function accepts files that may be missing some expected columns; in
	that case the missing columns are created with NaN values so downstream code
	can operate without KeyErrors.
	"""

	path = _resolve_path(fname)
	df = pd.read_csv(path)

	# Expected columns for B1/B2 datasets — coerce types and create missing cols
	expected = ['t_ms','ax_g','ax_lpf_g']
	for c in expected:
		if c in df.columns:
			df[c] = pd.to_numeric(df[c], errors='coerce')
		else:
			# missing column -> fill with NaN so code that references columns won't fail
			df[c] = np.nan

	# Ensure we have a valid time column and create t_s (seconds)
	df = df.dropna(subset=['t_ms']).reset_index(drop=True)
	df['t_s'] = df['t_ms'] / 1000.0

	return df

def analyze_and_plot(save_figs=False):
	"""Load the three C1 CSVs and produce plots comparing raw vs filtered data.

	Behaviour
	---------
	- Loads the three files: `C1_axis_alpha_0.1.csv`, `C1_axis_alpha_0.5.csv`,
	  `C1_axis_alpha_0.9.csv` from the script directory or CWD.
	- For each alpha file, plots raw (`ax_g`) and filtered (`ax_lpf_g`) on a
	  dedicated figure to inspect noise reduction and smoothing.
	- Creates a combined figure overlaying the filtered signals for the three
	  alphas plus the raw signal (light gray) for comparison.
	- Computes simple metrics printed to stdout: standard deviation of raw vs
	  filtered (noise reduction), and an approximate lag estimate (seconds)
	  computed from the cross-correlation peak between raw and filtered.
	- If `save_figs=True`, writes PNG files to a `figures/` directory next to
	  the script. Otherwise calls `plt.show()` once after creating figures so
	  interactive windows open together.

	Parameters
	----------
	save_figs : bool
		If True, save figures to `./figures` instead of calling ``plt.show()``.
	"""

	# Files for the three alpha values. Resolved by _resolve_path inside loader.
	script_dir = os.path.dirname(__file__)
	files = {
		0.1: os.path.join(script_dir, 'C1_axis_alpha_0.1.csv'),
		0.5: os.path.join(script_dir, 'C1_axis_alpha_0.5.csv'),
		0.9: os.path.join(script_dir, 'C1_axis_alpha_0.9.csv'),
	}

	# Helper: estimate lag (seconds) between raw and filtered using cross-correlation
	def estimate_lag_seconds(x_raw, x_filt, t_s):
		"""Return lag (secs) where filtered best matches raw (peak of cross-correlation).

		This is a simple estimate. For noisy signals the estimate can be noisy.
		"""
		# make sure inputs are numpy arrays and zero-mean for correlation
		xr = np.asarray(x_raw) - np.nanmean(x_raw)
		xf = np.asarray(x_filt) - np.nanmean(x_filt)
		# drop NaNs by simple masking (same-length arrays assumed)
		mask = np.isfinite(xr) & np.isfinite(xf)
		if mask.sum() < 3:
			return np.nan
		xr = xr[mask]
		xf = xf[mask]
		# compute correlation
		corr = np.correlate(xr, xf, mode='full')
		lag_idx = corr.argmax() - (len(xr) - 1)
		# estimate sample spacing from t_s (may be non-uniform; use median diff)
		if len(t_s[mask]) >= 2:
			dt = np.median(np.diff(t_s[mask]))
		else:
			dt = np.nan
		return float(lag_idx) * float(dt) if not np.isnan(dt) else np.nan

	dfs = {}
	for alpha, path in files.items():
		try:
			dfs[alpha] = load_imu_csv(path)
		except FileNotFoundError:
			# Try resolving using _resolve_path directly and re-raise if missing
			alt = _resolve_path(os.path.basename(path))
			dfs[alpha] = load_imu_csv(alt)

	# Create per-alpha figures (raw vs filtered)
	figs = []
	for alpha, df in dfs.items():
		# Column names expected in these C1 files: 't_ms', 'ax_g', 'ax_lpf_g'
		if 't_s' not in df.columns:
			df['t_s'] = df['t_ms'] / 1000.0
		t = df['t_s'].to_numpy()
		ax_raw = df.get('ax_g')
		ax_filt = df.get('ax_lpf_g')
		# If columns are missing, warn and continue
		if ax_raw is None or ax_filt is None:
			print(f"Warning: expected columns missing for alpha={alpha}: ax_g or ax_lpf_g")
			continue

		fig, ax = plt.subplots(figsize=(10, 4))
		ax.plot(t, ax_raw, label='raw ax (g)', color='tab:gray', linewidth=0.6, alpha=0.9)
		ax.plot(t, ax_filt, label=f'LPF ax (alpha={alpha})', linewidth=1.0)
		ax.set_xlabel('time (s)')
		ax.set_ylabel('ax (g)')
		ax.set_title(f'Raw vs Low-pass filtered ax (alpha={alpha})')
		ax.grid(True, linestyle='--', alpha=0.3)
		ax.legend()
		figs.append((f'raw_vs_lpf_alpha_{alpha}'.replace('.', '_'), fig))

		# Compute simple metrics and print summary
		std_raw = np.nanstd(ax_raw)
		std_filt = np.nanstd(ax_filt)
		reduction = (std_raw - std_filt) / std_raw * 100.0 if std_raw != 0 else np.nan
		lag_s = estimate_lag_seconds(ax_raw.to_numpy(), ax_filt.to_numpy(), t)
		print(f'alpha={alpha}: std raw={std_raw:.4f} g, std filt={std_filt:.4f} g, reduction={reduction:.1f}%, lag~{lag_s:.4f} s')

	# Combined figure: raw (light) + all filtered overlays for direct comparison
	fig_comb, axc = plt.subplots(figsize=(11, 4))
	# choose one of the dataframes with longest time as reference for raw plotting
	ref_alpha = sorted(dfs.keys())[0]
	ref_df = dfs[ref_alpha]
	if 't_s' not in ref_df.columns:
		ref_df['t_s'] = ref_df['t_ms'] / 1000.0
	t_ref = ref_df['t_s'].to_numpy()
	# Plot raw from reference alpha (should be same raw for all files)
	if 'ax_g' in ref_df.columns:
		axc.plot(t_ref, ref_df['ax_g'], color='0.85', linewidth=0.6, label='raw (ref)', zorder=0)

	colors = ['C0', 'C1', 'C2']
	for (alpha, df), c in zip(dfs.items(), colors):
		if 't_s' not in df.columns:
			df['t_s'] = df['t_ms'] / 1000.0
		if 'ax_lpf_g' not in df.columns:
			continue
		axc.plot(df['t_s'], df['ax_lpf_g'], label=f'LPF alpha={alpha}', color=c, linewidth=0.9)

	axc.set_xlabel('time (s)')
	axc.set_ylabel('ax (g)')
	axc.set_title('Comparison of LPF outputs (different alpha)')
	axc.grid(True, linestyle='--', alpha=0.25)
	axc.legend()
	figs.append(('C1_combined_lpf_comparison', fig_comb))

	# Save or show figures
	out_dir = os.path.join(script_dir, 'C1figures')
	if save_figs==True:
		os.makedirs(out_dir, exist_ok=True)
		for name, fig in figs:
			out_path = os.path.join(out_dir, f'{name}.png')
			fig.tight_layout()
			fig.savefig(out_path, dpi=150)
			print(f'Saved {out_path}')
		plt.close('all')
	else:
		# Create all figures and then show once so GUI opens windows together
		plt.show()


if __name__ == '__main__':
	# When run interactively, do not save by default. Pass save_figs=True in CI.
	analyze_and_plot(save_figs=False)

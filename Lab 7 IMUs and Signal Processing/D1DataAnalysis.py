# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 27, 2025

# Goal:
# Task D1 - Export plots of raw vs filtered data to assess noise reduction vs lag for different alpha values

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
	expected = ['t_ms','roll_acc','roll_comp','pitch_acc','pitch_comp']
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
	# Load D1 dataset files for each alpha value
	alphas = [0.9, 0.98, 0.995]
	dfs = {}
	script_dir = os.path.dirname(__file__)
	for alpha in alphas:
		fname = f"D1_complementary_{alpha}.csv"
		try:
			dfs[alpha] = load_imu_csv(os.path.join(script_dir, fname))
		except FileNotFoundError:
			try:
				# try basename resolve
				dfs[alpha] = load_imu_csv(fname)
			except FileNotFoundError:
				print(f"File not found for alpha={alpha}: {fname}")
				continue

	if len(dfs) == 0:
		print("No D1 files found — aborting analysis.")
		return

	# Prepare containers for figures
	figs = []

	# Metrics summary accumulator
	metrics = {}

	# Helper: RMS and simple steady-state metrics
	def rms(x):
		x = np.asarray(x)
		return np.sqrt(np.nanmean(np.square(x)))

	# Analyze per-alpha: plot roll & pitch comparisons (accel vs comp)
	for alpha, df in dfs.items():
		# ensure time in seconds
		if 't_s' not in df.columns:
			df['t_s'] = df['t_ms'] / 1000.0
		t = df['t_s'].to_numpy()

		# read columns (may contain NaNs if missing)
		roll_acc = df.get('roll_acc')
		roll_comp = df.get('roll_comp')
		pitch_acc = df.get('pitch_acc')
		pitch_comp = df.get('pitch_comp')

		# Basic sanity checks
		if roll_acc is None or roll_comp is None:
			print(f"alpha={alpha}: missing roll columns — skipping")
			continue

		# Compute errors (comp - accel)
		err_roll = roll_comp.to_numpy() - roll_acc.to_numpy()
		err_pitch = pitch_comp.to_numpy() - pitch_acc.to_numpy() if pitch_comp is not None and pitch_acc is not None else None

		# Steady-state window: use last 5% of samples as an estimate
		n = len(t)
		tail_n = max(3, int(n * 0.05))
		tail_slice = slice(max(0, n - tail_n), n)

		steady_roll_mean = np.nanmean(err_roll[tail_slice])
		steady_roll_rms = rms(err_roll[tail_slice])

		# Motion detection: use median absolute derivative to flag motion periods
		roll_deriv = np.abs(np.gradient(roll_acc.to_numpy(), t))
		med_deriv = np.nanmedian(roll_deriv)
		motion_mask = roll_deriv > (med_deriv * 5.0 + 1e-12)
		if motion_mask.sum() == 0:
			# fallback: mark as motion where derivative > small absolute threshold
			motion_mask = roll_deriv > 0.1

		# Metrics for quiet vs motion
		quiet_mask = ~motion_mask
		metrics[alpha] = {}
		metrics[alpha]['std_roll_acc'] = np.nanstd(roll_acc)
		metrics[alpha]['std_roll_comp'] = np.nanstd(roll_comp)
		metrics[alpha]['reduction_pct'] = ((metrics[alpha]['std_roll_acc'] - metrics[alpha]['std_roll_comp']) / metrics[alpha]['std_roll_acc'] * 100.0) if metrics[alpha]['std_roll_acc'] != 0 else np.nan
		metrics[alpha]['err_roll_rms_all'] = rms(err_roll)
		metrics[alpha]['err_roll_mean_all'] = np.nanmean(err_roll)
		metrics[alpha]['err_roll_steady_mean'] = steady_roll_mean
		metrics[alpha]['err_roll_steady_rms'] = steady_roll_rms
		metrics[alpha]['err_roll_rms_motion'] = rms(err_roll[motion_mask]) if motion_mask.sum() > 0 else np.nan
		metrics[alpha]['err_roll_rms_quiet'] = rms(err_roll[quiet_mask]) if quiet_mask.sum() > 0 else np.nan

		if err_pitch is not None:
			metrics[alpha]['err_pitch_rms_all'] = rms(err_pitch)
			metrics[alpha]['err_pitch_mean_all'] = np.nanmean(err_pitch)
			metrics[alpha]['err_pitch_steady_mean'] = np.nanmean(err_pitch[tail_slice])
			metrics[alpha]['err_pitch_steady_rms'] = rms(err_pitch[tail_slice])

		# Plot roll comparison
		fig_r, axr = plt.subplots(figsize=(10, 4))
		axr.plot(t, roll_acc, label='accel roll (deg)', color='tab:gray', linewidth=0.6)
		axr.plot(t, roll_comp, label=f'comp roll (alpha={alpha})', linewidth=1.0)
		axr.set_xlabel('time (s)')
		axr.set_ylabel('roll (deg)')
		axr.set_title(f'Roll: accel vs complementary (alpha={alpha})')
		axr.grid(True, linestyle='--', alpha=0.3)
		axr.legend()
		figs.append((f'roll_acc_vs_comp_alpha_{str(alpha).replace(".","_")}', fig_r))

		# Plot roll error (comp - accel)
		fig_er, axer = plt.subplots(figsize=(10, 3))
		axer.plot(t, err_roll, label='comp - accel (deg)', color='C3', linewidth=0.7)
		axer.axhline(metrics[alpha]['err_roll_steady_mean'], color='k', linestyle='--', linewidth=0.8, label='steady mean (tail)')
		axer.set_xlabel('time (s)')
		axer.set_ylabel('error (deg)')
		axer.set_title(f'Roll error (comp - accel) alpha={alpha}: RMS={metrics[alpha]["err_roll_rms_all"]:.4f} deg')
		axer.grid(True, linestyle='--', alpha=0.25)
		axer.legend()
		figs.append((f'roll_error_alpha_{str(alpha).replace(".","_")}', fig_er))

		# Plot pitch comparison if available
		if pitch_comp is not None and pitch_acc is not None:
			fig_p, axp = plt.subplots(figsize=(10, 4))
			axp.plot(t, pitch_acc, label='accel pitch (deg)', color='tab:gray', linewidth=0.6)
			axp.plot(t, pitch_comp, label=f'comp pitch (alpha={alpha})', linewidth=1.0)
			axp.set_xlabel('time (s)')
			axp.set_ylabel('pitch (deg)')
			axp.set_title(f'Pitch: accel vs complementary (alpha={alpha})')
			axp.grid(True, linestyle='--', alpha=0.3)
			axp.legend()
			figs.append((f'pitch_acc_vs_comp_alpha_{str(alpha).replace(".","_")}', fig_p))

	# Combined comparison across alphas: overlay complementary outputs
	fig_comb_roll, axc = plt.subplots(figsize=(11, 4))
	# plot accel from first available df as reference
	first_alpha = sorted(dfs.keys())[0]
	ref_df = dfs[first_alpha]
	if 't_s' not in ref_df.columns:
		ref_df['t_s'] = ref_df['t_ms'] / 1000.0
	axc.plot(ref_df['t_s'], ref_df['roll_acc'], color='0.85', linewidth=0.6, label='accel roll (ref)')
	colors = ['C0', 'C1', 'C2']
	for (alpha, df), c in zip(dfs.items(), colors):
		axc.plot(df['t_s'], df['roll_comp'], label=f'comp alpha={alpha}', color=c, linewidth=0.9)
	axc.set_xlabel('time (s)')
	axc.set_ylabel('roll (deg)')
	axc.set_title('Complementary filter outputs (roll) — different alphas')
	axc.grid(True, linestyle='--', alpha=0.25)
	axc.legend()
	figs.append(('D1_combined_comp_roll', fig_comb_roll))

	# Print a compact metrics table to stdout
	print('\nD1 complementary filter metrics summary (per-alpha):')
	for alpha in sorted(metrics.keys()):
		m = metrics[alpha]
		print(f"alpha={alpha}: std_acc={m['std_roll_acc']:.4f} deg, std_comp={m['std_roll_comp']:.4f} deg, reduction={m['reduction_pct']:.1f}%, err_rms_all={m['err_roll_rms_all']:.4f} deg, err_rms_quiet={m['err_roll_rms_quiet']:.4f} deg, err_rms_motion={m['err_roll_rms_motion']:.4f} deg, steady_mean={m['err_roll_steady_mean']:.4f} deg")

	# Optional saving
	out_dir = os.path.join(script_dir, 'D1figures')
	if save_figs==True:
		os.makedirs(out_dir, exist_ok=True)
		for name, fig in figs:
			out_path = os.path.join(out_dir, f'{name}.png')
			fig.tight_layout()
			fig.savefig(out_path, dpi=150)
			print(f'Saved {out_path}')
		plt.close('all')
	else:
		plt.show()


if __name__ == '__main__':
	analyze_and_plot(save_figs=False)
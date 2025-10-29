# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 27, 2025

# Goal:
# Task B1 - Compare accelerometer pitch/roll vs gyroscope pitch/roll
# Task B2 - Plot accelerometer data vs calibrated gyroscope data, quantify drift

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
	expected = ['t_ms','ax_mg','ay_mg','az_mg','roll_acc_deg','pitch_acc_deg','gyro_int_roll','gyro_int_pitch']
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


def analyze_and_plot(b1_csv='B1_gyro_log.csv', b2_csv='B2_gyro_drift_with_cal.csv', save_figs=False):
	# Load the B1 and B2 datasets into DataFrames
	b1 = load_imu_csv(b1_csv)
	b2 = load_imu_csv(b2_csv)

	# --- Compute error signals (gyro integrated minus accel-derived) ---
	# These are in degrees and represent the instantaneous difference between
	# the angle obtained by integrating gyro output and the angle computed
	# from the accelerometer.
	for df in (b1, b2):
		df['err_roll_deg'] = df['gyro_int_roll'] - df['roll_acc_deg']
		df['err_pitch_deg'] = df['gyro_int_pitch'] - df['pitch_acc_deg']

	# --- Cumulative RMS: expanding mean of squared error, then sqrt ---
	# This gives a running measure of how the error accumulates (useful to
	# visualize gyro drift over time). We compute separately for roll and pitch.
	b1['rms_roll_deg'] = np.sqrt((b1['err_roll_deg']**2).expanding().mean())
	b1['rms_pitch_deg'] = np.sqrt((b1['err_pitch_deg']**2).expanding().mean())
	b2['rms_roll_deg'] = np.sqrt((b2['err_roll_deg']**2).expanding().mean())
	b2['rms_pitch_deg'] = np.sqrt((b2['err_pitch_deg']**2).expanding().mean())

	# Print concise overall RMS summary for quick numeric comparison
	def _summ(df, name):
		roll_rms = np.sqrt(np.nanmean(df['err_roll_deg']**2))
		pitch_rms = np.sqrt(np.nanmean(df['err_pitch_deg']**2))
		print(f"{name}: overall RMS roll={roll_rms:.4f} deg, pitch={pitch_rms:.4f} deg, samples={len(df)}")

	_summ(b1, 'B1 (gyro vs accel)')
	_summ(b2, 'B2 (calibrated gyro vs accel)')

	# --- Plot comparisons: Accel vs Gyro for B1 and B2 ---
	# Create figures for roll/pitch comparisons for each dataset. Figures are
	# constructed before calling plt.show() so interactive environments open
	# all windows at once.

	# B1 roll: accel vs gyro integrated
	fig_b1_roll = plt.figure(figsize=(8,3))
	plt.plot(b1['t_s'], b1['roll_acc_deg'], label='accel roll (deg)')
	plt.plot(b1['t_s'], b1['gyro_int_roll'], label='gyro integrated roll (deg)', alpha=0.8)
	plt.xlabel('t (s)')
	plt.ylabel('Roll (deg)')
	plt.title('B1: Accel vs Gyro Integrated - Roll')
	plt.legend()

	# B1 pitch: accel vs gyro integrated
	fig_b1_pitch = plt.figure(figsize=(8,3))
	plt.plot(b1['t_s'], b1['pitch_acc_deg'], label='accel pitch (deg)')
	plt.plot(b1['t_s'], b1['gyro_int_pitch'], label='gyro integrated pitch (deg)', alpha=0.8)
	plt.xlabel('t (s)')
	plt.ylabel('Pitch (deg)')
	plt.title('B1: Accel vs Gyro Integrated - Pitch')
	plt.legend()

	# B2 roll: accel vs calibrated gyro
	fig_b2_roll = plt.figure(figsize=(8,3))
	plt.plot(b2['t_s'], b2['roll_acc_deg'], label='accel roll (deg)')
	plt.plot(b2['t_s'], b2['gyro_int_roll'], label='calibrated gyro roll (deg)', alpha=0.8)
	plt.xlabel('t (s)')
	plt.ylabel('Roll (deg)')
	plt.title('B2: Accel vs Calibrated Gyro - Roll')
	plt.legend()

	# B2 pitch: accel vs calibrated gyro
	fig_b2_pitch = plt.figure(figsize=(8,3))
	plt.plot(b2['t_s'], b2['pitch_acc_deg'], label='accel pitch (deg)')
	plt.plot(b2['t_s'], b2['gyro_int_pitch'], label='calibrated gyro pitch (deg)', alpha=0.8)
	plt.xlabel('t (s)')
	plt.ylabel('Pitch (deg)')
	plt.title('B2: Accel vs Calibrated Gyro - Pitch')
	plt.legend()

	# --- Drift / RMS plots: split into separate figures for roll and pitch ---
	# Roll RMS: compare cumulative RMS for roll between B1 and B2
	fig_rms_roll = plt.figure(figsize=(8,3))
	plt.plot(b1['t_s'], b1['rms_roll_deg'], label='B1 rms roll (deg)')
	plt.plot(b2['t_s'], b2['rms_roll_deg'], '--', label='B2 rms roll (deg)')
	plt.xlabel('t (s)')
	plt.ylabel('Cumulative RMS error (deg)')
	plt.title('Cumulative RMS drift - Roll')
	plt.legend()

	# Pitch RMS: compare cumulative RMS for pitch between B1 and B2
	fig_rms_pitch = plt.figure(figsize=(8,3))
	plt.plot(b1['t_s'], b1['rms_pitch_deg'], label='B1 rms pitch (deg)')
	plt.plot(b2['t_s'], b2['rms_pitch_deg'], '--', label='B2 rms pitch (deg)')
	plt.xlabel('t (s)')
	plt.ylabel('Cumulative RMS error (deg)')
	plt.title('Cumulative RMS drift - Pitch')
	plt.legend()

	# Optionally save the created figures to ./figures
	if save_figs == True:
		outdir = os.path.join(os.path.dirname(__file__), 'B1B2figures')
		os.makedirs(outdir, exist_ok=True)
		fig_b1_roll.savefig(os.path.join(outdir, 'B1_roll.png'))
		fig_b1_pitch.savefig(os.path.join(outdir, 'B1_pitch.png'))
		fig_b2_roll.savefig(os.path.join(outdir, 'B2_roll.png'))
		fig_b2_pitch.savefig(os.path.join(outdir, 'B2_pitch.png'))
		fig_rms_roll.savefig(os.path.join(outdir, 'RMS_roll.png'))
		fig_rms_pitch.savefig(os.path.join(outdir, 'RMS_pitch.png'))
		print(f'Saved figures to {outdir}')

	# Show all figures (interactive env will open them all)
	plt.show()


if __name__ == '__main__':
	# Default run: create plots and print RMS summaries. If running in CI/headless,
	# set MATPLOTLIB_BACKEND=Agg or call with save_figs=True to write PNGs instead of showing.
	analyze_and_plot(save_figs=False)
from __future__ import print_function, division, unicode_literals

import os

import numpy as np

from scipy import interpolate

import math

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.core.structure import Structure

import warnings


def plot_gamma_surface(fmt='pdf'):
    """
    Collect the energies from a grid of static energy
    calculations to plot the Gamma surface between two layers of the 2D
    material.

    Args:
        fmt (str): matplotlib format style. Check the matplotlib
            docs for options.
    """

    os.chdir('friction/lateral')

    static_dirs = [
        d.split('x') for d in os.listdir(os.getcwd()) if 'x' in d and
        len(d) == 3
    ]

    n_divs_x = max([int(d[0]) for d in static_dirs])
    n_divs_y = max([int(d[1]) for d in static_dirs])

    lattice = Structure.from_file('POSCAR').lattice
    area = np.cross(lattice._matrix[0], lattice._matrix[1])[2]

    ax = plt.figure(figsize=(n_divs_x * 1.2, n_divs_y * 1.2)).gca()

    ax.set_xlim(0, n_divs_x + 1)
    ax.set_ylim(0, n_divs_y + 1)

    ENERGY_ARRAY = []

    X_VALUES = range(n_divs_x)
    Y_VALUES = range(n_divs_y)

    not_converged = []
    for x in X_VALUES:
        ENERGY_ARRAY.append([])
        for y in Y_VALUES:
            dir = '{}x{}'.format(x, y)
            os.chdir(dir)
            try:
                energy = Vasprun('vasprun.xml').final_energy / area
                ENERGY_ARRAY[x].append(energy)
            except:
                not_converged.append('{}x{}'.format(x, y))
                ENERGY_ARRAY[x].append(0)
            os.chdir('../')
        ENERGY_ARRAY[x].append(ENERGY_ARRAY[x][0])

    ENERGY_ARRAY.append([])
    ENERGY_ARRAY[n_divs_x] = ENERGY_ARRAY[0]

    if not_converged:
        warnings.warn('{} did not converge.'.format(not_converged))
        for coords in not_converged:
            ENERGY_ARRAY[
                int(coords.split('x')[0])][int(coords.split('x')[1])] = energy

    minima = []
    maxima = []
    for x in X_VALUES:
        minima.append(min(ENERGY_ARRAY[x]))
        maxima.append(max(ENERGY_ARRAY[x]))

    abs_minimum = min(minima)
    abs_maximum = max(maxima)

    for x in range(n_divs_x + 1):
        for y in range(n_divs_y + 1):

            # Plot all energies relative to the global minimum.
            scaled_energy = ENERGY_ARRAY[x][y] - abs_minimum
            if '{}x{}'.format(x, y) in not_converged:
                color_code = 'w'
            else:
                color_code = plt.cm.jet(
                    scaled_energy / (abs_maximum - abs_minimum)
                    )

            ax.add_patch(plt.Rectangle((x, y), width=1, height=1,
                                       facecolor=color_code,
                                       linewidth=0))

    # Get rid of annoying ticks.
    ax.axes.get_yaxis().set_ticks([])
    ax.axes.get_xaxis().set_ticks([])

    os.chdir('../../')

    plt.savefig('gamma_surface.{}'.format(fmt), transparent=True)


def get_basin_and_peak_locations():
    """
    Find which directories inside 'friction/lateral' represent
    the minimum (basin) and maximum (peak) energy stacking
    configurations.

    Returns:
        tuple. Of the form (basin, peak).
    """

    os.chdir('friction/lateral')

    static_dirs = [
        d.split('x') for d in os.listdir(os.getcwd()) if 'x' in d and
        len(d) == 3
    ]

    n_divs_x = max([int(d[0]) for d in static_dirs])
    n_divs_y = max([int(d[1]) for d in static_dirs])

    X_VALUES = range(n_divs_x)
    Y_VALUES = range(n_divs_y)

    abs_maximum = -10000
    abs_minimum = 0
    for x in X_VALUES:
        for y in Y_VALUES:
            dir = '{}x{}'.format(x, y)
            os.chdir(dir)
            try:
                energy = Vasprun('vasprun.xml').final_energy
                if energy < abs_minimum:
                    basin = dir
                    abs_minimum = energy
                if energy > abs_maximum:
                    peak = dir
                    abs_maximum = energy
            except:
                pass
            os.chdir('../')
    os.chdir('../../')

    return(basin, peak)


def plot_friction_force(fmt='pdf'):
    """
    Plot the sinusoidal curve of delta E between basin and saddle
    points for each normal spacing dz.

    Args:
        fmt (str): matplotlib format style. Check the matplotlib
            docs for options.
    """

    os.chdir('friction/normal')

    f, (ax1, ax2) = plt.subplots(2, figsize=(16, 16))

    spacings = sorted([float(spc) for spc in os.listdir(os.getcwd()) if
                       os.path.isdir(spc)])

    spc_range = spacings[-1] - spacings[0] + 0.1

    for spacing in spacings:
        os.chdir(str(spacing))
        subdirectories = os.listdir(os.getcwd())

        amplitude = abs(
            Vasprun('{}/vasprun.xml'.format(subdirectories[0])).final_energy
            - Vasprun('{}/vasprun.xml'.format(subdirectories[1])).final_energy
            ) / 2

        start_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[0])
            ).sites[-1].coords
        end_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[1])
            ).sites[-1].coords
        dist = np.sqrt(
            (start_coords[0] - end_coords[0])**2
            + (start_coords[1] - end_coords[1])**2)

        b = (2 * np.pi) / (dist * 2)

        x = np.arange(0, 4, 0.01)
        sinx = [amplitude * np.sin(b * val) + amplitude for val in x]
        cosx = [b * amplitude * np.cos(b * val)
                if np.cos(b * val) > 0 else 0 for val in x]

        ax1.plot(x, sinx, linewidth=8,
                 color=plt.cm.jet(-(spacing - 4) / spc_range), label=spacing)
        ax1.set_xticklabels(ax1.get_xticks(), family='serif', fontsize=18)
        ax1.set_yticklabels(ax1.get_yticks(), family='serif', fontsize=18)
        ax1.set_xlabel(r'$\mathrm{\Delta d\/(\AA)}$', family='serif',
            fontsize=24)
        ax1.set_ylabel(r'$\mathrm{E(z)\/(eV)}$', family='serif', fontsize=24)
        ax2.plot(x, cosx, linewidth=8,
                 color=plt.cm.jet(-(spacing - 4) / spc_range), label=spacing)
        ax2.set_xticklabels(ax2.get_xticks(), family='serif', fontsize=18)
        ax2.set_yticklabels(ax2.get_yticks(), family='serif', fontsize=18)
        ax2.set_xlabel(r'$\mathrm{\Delta d\/(\AA)}$', family='serif',
            fontsize=24)
        ax2.set_ylabel(r'$\mathrm{F_f\/(eV/\AA)}$', family='serif', fontsize=24)
        os.chdir('../')

    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')

    os.chdir('../../')

    plt.savefig('F_f.{}'.format(fmt))


def plot_normal_force(basin_dir, fmt='pdf'):
    """
    Plot the LJ-like curve of the energy at the basin point
    as a function of normal spacing dz.

    Args:
        basin_dir (str): directory corresponding to the minimum
            energy on the gamma surface. Generally obtained by the
            get_basin_and_peak_locations() function.
        fmt (str): matplotlib format style. Check the matplotlib
            docs for options.
    """

    os.chdir('friction/normal')
    spacings = [float(dir) for dir in os.listdir(os.getcwd()) if
                os.path.isdir(dir)]
    spacings.sort()

    fig = plt.figure(figsize=(16, 10))
    ax = fig.gca()
    ax2 = ax.twinx()

    abs_E = [
        Vasprun('{}/{}/vasprun.xml'.format(spacing, basin_dir)).final_energy
        for spacing in spacings
        ]
    E = [energy - abs_E[-1] for energy in abs_E]

    spline = interpolate.splrep(spacings, E, s=0)
    xnew = np.arange(spacings[0], spacings[-1], 0.001)
    ynew = interpolate.splev(xnew, spline, der=0)
    ynew_slope = interpolate.splev(spacings, spline, der=1)

    ax.set_xlim(spacings[0], spacings[-1])

    ax.plot([spacings[0], spacings[-1]], [0, 0], '--', color=plt.cm.jet(0))
    ax2.plot([spacings[0], spacings[-1]], [0, 0], '--', color=plt.cm.jet(0.9))
    E_z = ax.plot(xnew, ynew, color=plt.cm.jet(0),
                  linewidth=4, label=r'$\mathrm{E(z)}$')
    F_N = ax2.plot(spacings, [-y for y in ynew_slope], color=plt.cm.jet(0.9),
                   linewidth=4, label=r'$\mathrm{F_N}$')

    ax.set_ylim(ax.get_ylim())

    ax.set_xticklabels(ax.get_xticks(), family='serif', fontsize=18)
    ax.set_yticklabels(ax.get_yticks(), family='serif', fontsize=18)
    ax2.set_yticklabels(ax2.get_yticks(), family='serif', fontsize=18)

    ax.set_xlabel(r'$\mathrm{z\/(\AA)}$', fontsize=24)
    ax.set_ylabel(r'$\mathrm{E(z)\/(eV)}$', fontsize=24)
    ax2.set_ylabel(r'$\mathrm{F_N\/(eV/\AA)}$', fontsize=24)

    data = E_z + F_N
    labs = [l.get_label() for l in data]

    ax.legend(data, labs, loc='upper right', fontsize=24)

    ax.plot(spacings, E, linewidth=0, marker='o', color=plt.cm.jet(0),
            markersize=10, markeredgecolor='none')

    os.chdir('../../')

    plt.savefig('F_N.{}'.format(fmt))


def plot_mu_vs_F_N(basin_dir, fmt='pdf'):
    """
    Plot friction coefficient 'mu' vs. F_Normal.
    mu = F_friction / F_Normal.

    Args:
        basin_dir (str): directory corresponding to the minimum
            energy on the gamma surface. Generally obtained by the
            get_basin_and_peak_locations() function.
        fmt (str): matplotlib format style. Check the matplotlib
            docs for options.
    """

    fig = plt.figure(figsize=(16, 10))
    ax = fig.gca()
    ax2 = ax.twinx()

    os.chdir('friction/normal')
    spacings = [float(dir) for dir in os.listdir(os.getcwd()) if
                os.path.isdir(dir)]
    spacings.sort()

    abs_E = [
        Vasprun('{}/{}/vasprun.xml'.format(spacing, basin_dir)).final_energy
        for spacing in spacings
        ]
    E = [energy - abs_E[-1] for energy in abs_E]

    spline = interpolate.splrep(spacings, E, s=0)
    xnew = np.arange(spacings[0], spacings[-1], 0.001)
    ynew = interpolate.splev(xnew, spline, der=0)
    ynew_slope = interpolate.splev(spacings, spline, der=1)
    F_N = [-y * 1.602 for y in ynew_slope]
    F_f = []

    for spacing in sorted([float(spc) for spc in os.listdir(os.getcwd()) if
            os.path.isdir(spc)]):
        os.chdir(str(spacing))
        subdirectories = os.listdir(os.getcwd())

        amplitude = abs(
            Vasprun('{}/vasprun.xml'.format(subdirectories[0])).final_energy
            - Vasprun('{}/vasprun.xml'.format(subdirectories[1])).final_energy
            ) / 2

        start_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[0])
            ).sites[-1].coords
        end_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[1])
            ).sites[-1].coords
        dist = np.sqrt(
            (start_coords[0] - end_coords[0])**2
            + (start_coords[1] - end_coords[1])**2)

        b = (2 * np.pi) / (dist * 2)

        x = np.arange(0, 4, 0.01)
        sinx = [amplitude * np.sin(b * val) + amplitude for val in x]
        cosx = [b * amplitude * np.cos(b * val)
                if np.cos(b * val) > 0 else 0 for val in x]
        F_f.append(max(cosx) * 1.602)
        os.chdir('../')

    os.chdir('../../')

    mu = [f / N for f, N in zip(F_f, F_N)]

    ax = plt.figure().gca()
    ax.plot(F_N, mu, linewidth=2, marker='o', markeredgecolor='none',
            markersize=3, color=plt.cm.jet(0))
    plt.savefig('mu_vs_F_N.{}'.format(fmt))


def get_mu_vs_F_N(basin_dir):
    """
    Essentially the same function as plotting, but without the plot.

    Args:
        basin_dir (str): directory corresponding to the minimum
            energy on the gamma surface. Generally obtained by the
            get_basin_and_peak_locations() function.

    Returns:
        dict. Of the form {'F_N': F_N, 'mu': mu, 'F_f': F_f}, where
            forces are in nN.
    """

    os.chdir('friction/normal')
    spacings = [float(dir) for dir in os.listdir(os.getcwd()) if
                os.path.isdir(dir)]
    spacings.sort()

    abs_E = [
        Vasprun('{}/{}/vasprun.xml'.format(spacing, basin_dir)).final_energy
        for spacing in spacings
        ]
    E = [energy - abs_E[-1] for energy in abs_E]

    spline = interpolate.splrep(spacings, E, s=0)
    xnew = np.arange(spacings[0], spacings[-1], 0.001)
    ynew = interpolate.splev(xnew, spline, der=0)
    ynew_slope = interpolate.splev(spacings, spline, der=1)
    # Convert eV.A to nN
    F_N = [-y * 1.602 for y in ynew_slope]
    F_f = []

    for spacing in sorted([float(spc) for spc in os.listdir(os.getcwd()) if
            os.path.isdir(spc)]):
        os.chdir(str(spacing))
        subdirectories = os.listdir(os.getcwd())

        try:
            amplitude = abs(
                Vasprun('{}/vasprun.xml'.format(subdirectories[0])).final_energy
                -
                Vasprun('{}/vasprun.xml'.format(subdirectories[1])).final_energy
                ) / 2
        except:
            print('One or more jobs in {}/ have not converged.'.format(spacing))

        start_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[0])
            ).sites[-1].coords
        end_coords = Structure.from_file(
            '{}/POSCAR'.format(subdirectories[1])
            ).sites[-1].coords
        dist = np.sqrt(
            (start_coords[0] - end_coords[0])**2
            + (start_coords[1] - end_coords[1])**2)

        b = (2 * np.pi) / (dist * 2)

        x = np.arange(0, 4, 0.01)
        sinx = [amplitude * np.sin(b * val) + amplitude for val in x]
        cosx = [b * amplitude * np.cos(b * val)
                if np.cos(b * val) > 0 else 0 for val in x]
        F_f.append(max(cosx) * 1.602)
        os.chdir('../')

    os.chdir('../../')

    mu = [f / N for f, N in zip(F_f, F_N)]

    return({'F_N': F_N, 'mu': mu, 'F_f': F_f})

r"""
===============================================================================
Submodule -- thermal_conductance
===============================================================================

"""

import scipy as _sp


def series_resistors(target,
                     pore_thermal_conductivity='pore.thermal_conductivity',
                     throat_thermal_conductivity='throat.thermal_conductivity',
                     throat_diffusivity='throat.diffusivity',
                     throat_equivalent_area='throat.equivalent_area',
                     throat_conduit_lengths='throat.conduit_lengths'):
    r"""
    Calculate the thermal conductance of void conduits in network ( 1/2 pore - full
    throat - 1/2 pore ) based on size (assuming cylindrical geometry)

    Parameters
    ----------
    target : OpenPNM Object
        The object which this model is associated with. This controls the
        length of the calculated array, and also provides access to other
        necessary properties.

    pore_thermal_conductivity : string
        Dictionary key of the pore thermal conductivity values

    throat_thermal_conductivity : string
        Dictionary key of the throat thermal conductivity values

    throat_equivalent_area : string
        Dictionary key of the throat equivalent area values

    throat_conduit_lengths : string
        Dictionary key of the throat conduit lengths

    Notes
    -----
    (1) This function requires that all the necessary phase properties already
    be calculated.

    (2) This function calculates the specified property for the *entire*
    network then extracts the values for the appropriate throats at the end.

    """
    network = target.project.network
    throats = network.map_throats(target['throat._id'])
    phase = target.project.find_phase(target)
    geom = target.project.find_geometry(target)
    cn = network['throat.conns'][throats]
    # Getting equivalent areas
    A1 = geom[throat_equivalent_area+'.pore1'][throats]     # Equivalent area pore 1
    At = geom[throat_equivalent_area+'.throat'][throats]    # Equivalent area throat
    A2 = geom[throat_equivalent_area+'.pore2'][throats]     # Equivalent area pore 2
    # Getting conduit lengths
    L1 = geom[throat_conduit_lengths+'.pore1'][throats]     # Equivalent length pore 1
    Lt = geom[throat_conduit_lengths+'.throat'][throats]    # Equivalent length throat
    L2 = geom[throat_conduit_lengths+'.pore2'][throats]     # Equivalent length pore 2
    # Interpolate pore phase property values to throats
    try:
        kt = phase[throat_thermal_conductivity]
    except KeyError:
        kt = phase.interpolate_data(propname=pore_thermal_conductivity)
    try:
        kp = phase[pore_thermal_conductivity]
    except KeyError:
        kp = phase.interpolate_data(propname=throat_thermal_conductivity)
    # Remove any non-positive lengths
    L1[L1 <= 0] = 1e-12
    L2[L2 <= 0] = 1e-12
    Lt[Lt <= 0] = 1e-12
    # Find g for half of pore 1
    gp1 = kp[cn[:, 0]] * A1 / L1
    gp1[_sp.isnan(gp1)] = _sp.inf
    gp1[gp1<=0] = _sp.inf  # Set 0 conductance pores (boundaries) to inf
    # Find g for half of pore 2
    gp2 = kp[cn[:, 1]] * A2 / L2
    gp2[_sp.isnan(gp2)] = _sp.inf
    gp2[gp2<=0] = _sp.inf  # Set 0 conductance pores (boundaries) to inf
    # Find g for full throat
    gt = kt[throats] * At / Lt
    gt[gt<=0] = _sp.inf
    return (1/gt + 1/gp1 + 1/gp2)**(-1)

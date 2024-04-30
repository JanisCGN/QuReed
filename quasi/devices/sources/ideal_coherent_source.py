"""
Ideal Coherent Source Implementation
"""
import numpy as np
from math import factorial

from quasi.devices import (GenericDevice,
                           wait_input_compute,
                           coordinate_gui,
                           ensure_output_compute)
from quasi.devices.port import Port
from quasi.signals import (GenericSignal,
                           GenericFloatSignal,
                           GenericBoolSignal,
                           GenericQuantumSignal)

from quasi.gui.icons import icon_list
from quasi.simulation import Simulation, SimulationType, ModeManager

from quasi._math.fock.ops import adagger, a, coherent_state



class IdealCoherentSource(GenericDevice):
    """
    COHERENT
    """
    ports = {
        "control": Port(
            label="control",
            direction="input",
            signal=None,
            signal_type=GenericBoolSignal,
            device=None),
        "alpha": Port(
            label="alpha",
            direction="input",
            signal=None,
            signal_type=GenericFloatSignal,
            device=None),
        "phi": Port(
            label="phi",
            direction="input",
            signal=None,
            signal_type=GenericFloatSignal,
            device=None),
        "output": Port(
            label="output",
            direction="output",
            signal=None,
            signal_type=GenericQuantumSignal,
            device=None),
    }

    # Gui Configuration
    gui_icon = icon_list.LASER
    gui_tags = ["ideal"]
    gui_name = "Ideal Coherent Photon Source"
    gui_documentation = "ideal_coherent_photon_source.md"

    power_peak = 0
    power_average = 0

    reference = None

    def set_displacement(self, alpha: float, phi: float):
        """
        Sets the signals so that the source correctly displaces the vacuum
        """
        alpha_sig = GenericFloatSignal()
        alpha_sig.set_float(alpha)
        phi_sig = GenericFloatSignal()
        phi_sig.set_float(phi)
        self.register_signal(signal=alpha_sig, port_label="alpha")
        self.register_signal(signal=phi_sig, port_label="phi")
        phi_sig.set_computed()
        alpha_sig.set_computed()

    @ensure_output_compute
    @coordinate_gui
    @wait_input_compute
    def compute_outputs(self, *args, **kwargs):
        simulation = Simulation.get_instance()
        if simulation.simulation_type is SimulationType.FOCK:
            self.simulate_fock()

    def simulate_fock(self):
        """
        Fock Simulation
        """
        simulation = Simulation.get_instance()
        backend = simulation.get_backend()

        # Get the mode manager
        mm = ModeManager()
        # Generate new mode
        mode = mm.create_new_mode()
        # Displacement parameters
        alpha = self.ports["alpha"].signal.contents
        phi = self.ports["phi"].signal.contents
        
        # Initialize photon number state in the mode
        operator = backend.displace(alpha, phi, mm.get_mode_index(mode))
        backend.apply_operator(operator, [mm.get_mode_index(mode)])

        self.ports["output"].signal.set_contents(
            timestamp=0,
            mode_id=mode)
        self.ports["output"].signal.set_computed()

"""
This module implements helpers for visualization of states during simulation
"""
from photon_weave.state.composite_envelope import CompositeEnvelope


def viz_hook(event):
  """
  this function takes an event. If the event contains a state, it displays the energy of the state.
  """
  if "signal" in event.kwargs:
    if "envelope" in event.signal:
      env = event.signal.envelope
      meas = env.measure()
      print(meas)    
  return 0


  

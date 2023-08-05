# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A MIDI interface to the sequence generators.

Captures monophonic input MIDI sequences and plays back responses from the
sequence generator.
"""

import time

# internal imports
import tensorflow as tf
import magenta

from magenta.interfaces.midi import midi_hub
from magenta.interfaces.midi import midi_interaction
from magenta.models.melody_rnn import melody_rnn_sequence_generator

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_bool(
    'list_ports',
    False,
    'Only list available MIDI ports.')
tf.app.flags.DEFINE_string(
    'input_port',
    'magenta_in',
    'The name of the input MIDI port.')
tf.app.flags.DEFINE_string(
    'output_port',
    'magenta_out',
    'The name of the output MIDI port.')
tf.app.flags.DEFINE_integer(
    'phrase_bars',
    None,
    'The number of bars of duration to use for the call and response phrases. '
    'If none, `end_call_control_number` must be specified.')
tf.app.flags.DEFINE_integer(
    'start_call_control_number',
    None,
    'The control change number to use as a signal to start the call phrase. If '
    'None, call will start immediately after response.')
tf.app.flags.DEFINE_integer(
    'end_call_control_number',
    None,
    'The control change number to use as a signal to end the call phrase. If '
    'None, `phrase_bars` must be specified.')
# TODO(adarob): Make the qpm adjustable by a control change signal.
tf.app.flags.DEFINE_integer(
    'qpm',
    90,
    'The quarters per minute to use for the metronome and generated sequence.')
tf.app.flags.DEFINE_string(
    'bundle_file',
    None,
    'The location of the bundle file to use.')

# A map from a string generator name to its class.
_GENERATOR_MAP = melody_rnn_sequence_generator.get_generator_map()


def main(unused_argv):
  if FLAGS.list_ports:
    print "Input ports: '%s'" % (
        "', '".join(midi_hub.get_available_input_ports()))
    print "Ouput ports: '%s'" % (
        "', '".join(midi_hub.get_available_output_ports()))
    return

  if FLAGS.bundle_file is None:
    print '--bundle_file must be specified.'
    return

  if (FLAGS.end_call_control_number, FLAGS.phrase_bars).count(None) != 1:
    print('Exactly one of --end_call_control_number or --phrase_bars should be '
          'specified.')
    return

  try:
    bundle = magenta.music.sequence_generator_bundle.read_bundle_file(
        FLAGS.bundle_file)
  except magenta.music.sequence_generator_bundle.GeneratorBundleParseException:
    print 'Failed to parse bundle file: %s' % FLAGS.bundle_file
    return

  generator_id = bundle.generator_details.id
  if generator_id not in _GENERATOR_MAP:
    print "Unrecognized SequenceGenerator ID '%s' in bundle file: %s" % (
        generator_id, FLAGS.bundle_file)
    return
  generator = _GENERATOR_MAP[generator_id](checkpoint=None, bundle=bundle)
  generator.initialize()
  print "Loaded '%s' generator bundle from file '%s'." % (
      bundle.generator_details.id, FLAGS.bundle_file)

  if FLAGS.input_port not in midi_hub.get_available_input_ports():
    print "Opening '%s' as a virtual MIDI port for input." % FLAGS.input_port
  if FLAGS.output_port not in midi_hub.get_available_output_ports():
    print "Opening '%s' as a virtual MIDI port for output." % FLAGS.output_port
  hub = midi_hub.MidiHub(FLAGS.input_port, FLAGS.output_port,
                         midi_hub.TextureType.MONOPHONIC)

  start_call_signal = (
      None if FLAGS.start_call_control_number is None else
      midi_hub.MidiSignal(control=FLAGS.start_call_control_number, value=0))
  end_call_signal = (
      None if FLAGS.end_call_control_number is None else
      midi_hub.MidiSignal(control=FLAGS.end_call_control_number, value=0))
  interaction = midi_interaction.CallAndResponseMidiInteraction(
      hub,
      FLAGS.qpm,
      generator,
      phrase_bars=FLAGS.phrase_bars,
      start_call_signal=start_call_signal,
      end_call_signal=end_call_signal)

  print ''
  print 'Instructions:'
  if FLAGS.start_call_control_number is not None:
    print ('When you want to begin the call phrase, signal control number %d '
           'with value 0.' % FLAGS.start_call_control_number)
  print 'Play when you hear the metronome ticking.'
  if FLAGS.phrase_bars is not None:
    print ('After %d bars (4 beats), Magenta will play its response.' %
           FLAGS.phrase_bars)
  else:
    print ('When you want to end the call phrase, signal control number %d '
           'with value 0' % FLAGS.end_call_control_number)
    print ('At the end of the current bar (4 beats), Magenta will play its '
           'response.')
  if FLAGS.start_call_control_number is not None:
    print ('Once the response completes, the interface will wait for you to '
           'signal a new call phrase using control number %d.' %
           FLAGS.start_call_control_number)
  else:
    print ('Once the response completes, the metronome will tick and you can '
           'play again.')

  print ''
  print 'To end the interaction, press CTRL-C.'

  interaction.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    interaction.stop()

  print 'Interaction stopped.'


def console_entry_point():
  tf.app.run(main)


if __name__ == '__main__':
  console_entry_point()

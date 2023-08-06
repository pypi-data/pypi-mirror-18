PyKyu
=====

Process queueing; declarative, configurable.

`readthedocs.org <http://pykyu.readthedocs.io/en/latest/>`_

Example
-------

This is how you do it.

.. code-block:: python

  # -*- coding: utf-8 -*-
  import json

  from pykyu import Kyu, KyuState


  def setup(s: KyuState):
      s.data['log'] = list()
      s.data['log'].append('setup')
      s.data['type'] = 'application/json'


  def fetch_a(s: KyuState):
      s.data['log'].append('fetch_a')


  def fetch_b(s: KyuState):
      s.data['log'].append('fetch_b')


  def display_choice(s: KyuState):
      if 'json' in s.data['type']:
          s.cursor.kyu.group('display').hook(display_json)
      else:
          s.cursor.kyu.group('display').hook(display_html)


  def display_json(s: KyuState):
      s.data['result'] = json.dumps(s.data)


  def display_html(s: KyuState):
      lines = ['<li>%s</li>' % x for x in s.data['log']]
      s.data['result'] = '<ul>%s</ul>' % ''.join(lines)


  kyu = Kyu('test')

  with kyu.group('setup') as g:
      g.hook(setup)
  with kyu.group('fetch') as g:
      g.hook(fetch_b)
      g.hook(fetch_a, priority=10)
  with kyu.group('display') as g:
      g.hook(display_choice)

  state = kyu.run(KyuState())
  print(state.data['result'])
  # {"type": "application/json", "log": ["setup", "fetch_a", "fetch_b"]}


There is some more voodoo you can play with! You can view the documentation on
`readthedocs.org <http://pykyu.readthedocs.io/en/latest/>`_.

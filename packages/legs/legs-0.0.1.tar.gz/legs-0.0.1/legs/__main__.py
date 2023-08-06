#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import re

from argparse import ArgumentParser
from collections import defaultdict
from itertools import chain, count

from pithy.collection import freeze
from pithy.dict_utils import dict_put
from pithy.fs import path_ext, path_name_stem
from pithy.immutable import Immutable
from pithy.io import errF, errFL, errL, errSL, errLL, failF, failS, outFL
from pithy.iterable import fan_by_key_fn, group_by_heads, OnHeadless
from pithy.string_utils import pluralize

from unico import codes_for_ranges, ranges_for_codes
from unico.charsets import unicode_charsets

from legs.automata import NFA, DFA, empty_symbol, genDFA, minimizeDFA
from legs.rules import *
from legs.swift import output_swift


def main():
  parser = ArgumentParser(prog='legs')
  parser.add_argument('rules_path', nargs='?')
  parser.add_argument('-patterns', nargs='+')
  parser.add_argument('-dbg', action='store_true')
  parser.add_argument('-match', nargs='+')
  parser.add_argument('-mode', default=None)
  parser.add_argument('-output')
  parser.add_argument('-stats', action='store_true')
  parser.add_argument('-test', action='store_true')
  parser.add_argument('-type-prefix', default='')
  parser.add_argument('-license', default='NO LICENSE SPECIFIED')
  args = parser.parse_args()
  dbg = args.dbg

  is_match_specified = args.match is not None
  is_mode_specified = args.mode is not None
  target_mode = args.mode or 'main'
  if not is_match_specified and is_mode_specified:
    failF('`-mode` option only valid with `-match`.')

  if (args.rules_path is None) and args.patterns:
    path = '<patterns>'
    lines = args.patterns
  elif (args.rules_path is not None) and not args.patterns:
    path = args.rules_path
    try: lines = open(path)
    except FileNotFoundError:
      failF('legs error: no such rule file: {!r}', path)
  else:
    failF('`must specify either `rules_path` or `-pattern`.')
  mode_named_rules, mode_transitions = parse_legs(path, lines)

  mode_dfa_pairs = []
  for mode, named_rules in sorted(mode_named_rules.items()):
    if is_match_specified and mode != target_mode:
      continue
    if dbg:
      errSL('\nmode:', mode)
      for name, rule in named_rules:
        rule.describe(name=name)
      errL()
    nfa = genNFA(mode, named_rules)
    if dbg: nfa.describe()
    if dbg or args.stats: nfa.describe_stats('NFA Stats')

    msgs = nfa.validate()
    if msgs:
      errLL(*msgs)
      exit(1)

    fat_dfa = genDFA(nfa)
    if dbg: fat_dfa.describe('Fat DFA')
    if dbg or args.stats: fat_dfa.describe_stats('Fat DFA Stats')

    min_dfa = minimizeDFA(fat_dfa)
    if dbg: min_dfa.describe('Min DFA')
    if dbg or args.stats: min_dfa.describe_stats('Min DFA Stats')
    mode_dfa_pairs.append((mode, min_dfa))

    if is_match_specified and mode == target_mode:
      for string in args.match:
        match_string(nfa, fat_dfa, min_dfa, string)
      exit()

    if dbg: errL('----')

    post_matches = len(min_dfa.postMatchNodes)
    if post_matches:
      errFL('note: `{}`: minimized DFA contains {}', mode, pluralize(post_matches, 'post-match node'))

  if is_match_specified: failF('bad mode: {!r}', target_mode)

  if dbg and mode_transitions:
    errSL('\nmode transitions:')
    for a, b in mode_transitions:
      errSL('  %', a, b)

  dfa, modes, node_modes = combine_dfas(mode_dfa_pairs)
  if args.output is not None:
    output(dfa=dfa, modes=modes, node_modes=node_modes, mode_transitions=mode_transitions,
      rules_path=args.rules_path, path=args.output, test=args.test, type_prefix=args.type_prefix, license=args.license)


def match_string(nfa, fat_dfa, min_dfa, string):
  'Test `nfa`, `fat_dfa`, and `min_dfa` against each other by attempting to match `string`.'
  nfa_matches = nfa.match(string)
  if len(nfa_matches) > 1:
    failF('match: {!r}: NFA matched multiple rules: {}.', string, ', '.join(sorted(nfa_matches)))
  nfa_match = list(nfa_matches)[0] if nfa_matches else None
  fat_dfa_match = fat_dfa.match(string)
  if fat_dfa_match != nfa_match:
    failF('match: {!r} inconsistent match: NFA: {}; fat DFA: {}.', string, nfa_match, fat_dfa_match)
  min_dfa_match = min_dfa.match(string)
  if min_dfa_match != nfa_match:
    failF('match: {!r} inconsistent match: NFA: {}; min DFA: {}.', string, nfa_match, min_dfa_match)
  outFL('match: {!r} {} {}', string, *(('->', nfa_match) if nfa_match else ('--', 'incomplete')))


rule_re = re.compile(r'''(?x)
\s* # ignore leading space.
(?:
  (?P<comment> \# .*)
| % \s+ (?P<l_name> \w+ (\.\w+)? ) \s+ (?P<r_name> \w+ (\.\w+)? ) \s* (\#.*)?
| (?P<name> \w+ (\.\w+)? ) \s* : \s* (?P<pattern> .*)
| (?P<symbol> \w+ )
| (?P<tail> \| .*)
)
''')


def match_lines(path, lines):
  for line_num, line in enumerate(lines):
    line = line.rstrip() # always strip newline so that missing final newline is consistent.
    if not line: continue
    line_info = (path, line_num, line)
    match = rule_re.fullmatch(line)
    if not match:
      fail_parse((line_info, 0), 'invalid line: neither rule nor mode transition.')
    if match.group('comment'): continue
    yield (line_info, match)


def group_matches(matches):
  return group_by_heads(matches, is_head=lambda p: not p[1].group('tail'), headless=OnHeadless.keep)


def parse_legs(path, lines):
  '''
  Parse the legs source given in `lines`,
  returning a dictionary of mode names to rule objects, and a dictionary of mode transitions.
  '''
  rules = {} # keyed by name.
  simple_names = {}
  mode_transitions = {}
  for group in group_matches(match_lines(path, lines)):
    line_info, m = group[0]
    if m.group('l_name'): # mode transition.
      (src_pair, dst_pair) = parse_mode_transition(line_info, m)
      if src_pair in mode_transitions:
        fail_parse((line_info, 0), 'duplicate transition parent name: {!r}', src_pair[1])
      mode_transitions[src_pair] = dst_pair
    else:
      name, rule = parse_rule(group)
      if name in ('invalid', 'incomplete'):
        fail_parse((line_info, 0), 'rule name is reserved: {!r}', name)
      if name in rules:
        fail_parse((line_info, 0), 'duplicate rule name: {!r}', name)
      rules[name] = rule
      for simple in simplified_names(name):
        if simple in simple_names:
          fail_parse((line_info, 0), 'rule name collides when simplified: {!r}', simple_names[simple])
        simple_names[simple] = name
  return fan_by_key_fn(rules.items(), key=lambda item: mode_for_name(item[0])), mode_transitions


def parse_mode_transition(line_info, match):
  return (
    mode_and_name(match.group('l_name')),
    mode_and_name(match.group('r_name')))


def mode_and_name(name):
  return mode_for_name(name), name


def mode_for_name(name):
  mode, _, _ = name.rpartition('.')
  return (mode or 'main')


def simplified_names(name):
  n = name.lower()
  return { n.replace('.', '_'), n.replace('.', '') }


def parse_rule(group):
  line_info, match = group[0]
  name = match.group('name')
  if name: # named pattern.
    start_col = match.start('pattern')
  else:
    symbol = match.group('symbol')
    assert symbol
    name = symbol
    start_col = match.start('symbol')
  return name, parse_rule_pattern(group, start_col=start_col)


_name_re = re.compile(r'\w')

def parse_rule_pattern(group, start_col):
  'Parse a pattern and return a Rule object.'
  line_info, match = group[0]
  _, _, line = line_info
  parser_stack = [PatternParser((line_info, start_col))]
  # stack of parsers, one for each open nesting syntactic element: root, '(…)', or '[…]'.

  def flush_name(col):
    nonlocal line, name_pos
    s = name_pos[1] + 1 # omit leading `$`.
    name = line[s:col]
    try: charset = unicode_charsets[name]
    except KeyError: fail_parse(name_pos, 'unknown charset name: {!r}', name)
    parser_stack[-1].parse_charset(name_pos, charset)
    name_pos = None

  patterns = []
  for line_info, match in group:
    _, _, line = line_info
    pos = (line_info, start_col)
    escape = False
    end_col = len(line)
    name_pos = None # position of name currently being parsed or None.

    for col, c in enumerate(line):
      if col < start_col: continue
      pos = (line_info, col)
      parser = parser_stack[-1]

      if escape:
        escape = False
        try: charset = escape_charsets[c]
        except KeyError: fail_parse(pos, 'invalid escaped character: {!r}', c)
        else: parser.parse_charset(pos, charset)
        continue

      if name_pos is not None:
        if _name_re.match(c):
          continue
        elif c in ' #)]?*+':
          flush_name(col) # then proceed to regular parsing below.
        elif c in '\\$([&-^':
          fail_parse(pos, 'name must be terminated with a space character for readability.')
        else:
          fail_parse(pos, 'invalid name character: {!r}', c)

      if c == '\\':
        escape = True
      elif c == '#':
        end_col = col
        break
      elif c == ' ':
        continue
      elif c == '$':
        name_pos = pos
      elif not c.isprintable():
        fail_parse(pos, 'invalid non-printing character: {!r}'. c)
      elif c == parser.terminator:
        parser_stack.pop()
        parent = parser_stack[-1]
        parent.receive(parser.finish(pos))
      else:
        child = parser.parse(pos, c)
        if child:
          parser_stack.append(child)

    if escape:
      fail_parse(pos, 'dangling escape character')
    if name_pos is not None:
      flush_name(end_col)
    patterns.append(line[start_col:end_col])
    start_col = 0

  parser = parser_stack.pop()
  if parser_stack:
    fail_parse((line_info, end_col), 'expected terminator: {!r}', parser.terminator)
  rule = parser.finish(pos)
  rule.pattern = ' '.join(patterns)
  return rule


def fail_parse(pos, fmt, *items):
  'Print a formatted parsing failure to std err and exit.'
  (line_info, col) = pos
  (path, line_num, line_text) = line_info
  failF('{}:{}:{}: ' + fmt + '\n{}\n{}^', path, line_num + 1, col + 1, *items, line_text, ' ' * col)


def ranges_from_strings(*interval_strings):
  "Return a `str` object containing the specified range of characters denoted by each character pair."
  return tuple((ord(start), ord(last) + 1) for start, last in interval_strings)

def ranges_for_char(char):
  code = ord(char)
  return ((code, code + 1),)

escape_charsets = {
  'n': ranges_for_char('\n'),
  's': ranges_for_char(' '), # nonstandard space escape.
  't': ranges_for_char('\t'),
}
escape_charsets.update((c, ranges_for_char(c)) for c in '\\#|$?*+()[]&-^')

if False:
  for k, v in sorted(escape_charsets.items()):
    errFL('{}: {!r}', k, v)


class PatternParser:

  def __init__(self, pos, terminator=None):
    self.pos = pos
    self.terminator = terminator
    self.choices = []
    self.seq = []
    self.seq_pos = pos

  def parse(self, pos, char):
    if char == '(':
      return PatternParser(pos, terminator=')')
    elif char == '[':
      return CharsetParser(pos)
    elif char == '|':
      self.flush_seq(pos)
    elif char == '?': self.quantity(pos, char, Opt)
    elif char == '*': self.quantity(pos, char, Star)
    elif char == '+': self.quantity(pos, char, Plus)
    else:
      self.seq.append(Charset(pos, ranges=ranges_for_char(char)))

  def parse_charset(self, pos, charset):
    self.seq.append(Charset(pos, ranges=charset))

  def finish(self, pos):
    self.flush_seq(pos)
    choices = self.choices
    return choices[0] if len(choices) == 1 else Choice(self.pos, subs=tuple(choices))

  def flush_seq(self, pos):
    seq = self.seq
    if not seq: fail_parse(self.seq_pos, 'empty sequence.')
    rule = seq[0] if len(seq) == 1 else Seq(self.seq_pos, subs=tuple(seq))
    self.choices.append(rule)
    self.seq = []
    self.seq_pos = pos

  def quantity(self, pos, char, T):
    try: el = self.seq.pop()
    except IndexError: fail_parse(pos, "'{}' does not follow any pattern.", char)
    else: self.seq.append(T(pos, subs=(el,)))

  def receive(self, result):
    self.seq.append(result)


class CharsetParser():
  '''
  The Legs character set syntax is different from traditional regular expressions.
  * `[...]` introduces a nested character set.
  * `&` binary operator: set intersection.
  * `-` binary operator: set difference.
  * `^` binary operator: set symmetric difference.
  Multiple intersection operators can be chained together,
  but if a difference or set difference operator is used,
  it must be the only operator to appear witihin the character set;
  more complex expressions must be explicitly grouped.
  Thus, the set expression syntax has no operator precedence or associativity.
  '''

  def __init__(self, pos):
    self.pos = pos
    self.terminator = ']'
    self.codes = set()
    self.codes_left = None  # left operand to current operator.
    self.operator = None # current operator waiting to finish parsing right side.
    self.operator_pos = None
    self.parsed_op = False
    self.parsed_diff_op = False

  def add_code(self, pos, code):
    if code in self.codes:
      fail_parse(pos, 'repeated character in set: {!r}', ord(code))
    self.codes.add(code)

  def flush_left(self, pos, msg_context):
    if not self.codes:
      fail_parse(pos, 'empty charset preceding {}', msg_context)
    op = self.operator
    if op is None: # first operator encountered.
      assert self.codes_left is None
      self.codes_left = self.codes
    elif op == '&': self.codes_left &= self.codes
    elif op == '-': self.codes_left -= self.codes
    elif op == '^': self.codes_left ^= self.codes
    else: raise ValueError(op) # internal error.
    self.codes = set()

  def push_operator(self, pos, op):
    self.flush_left(pos, msg_context='operator')
    is_diff_op = self.operator in ('-', '^')
    if self.parsed_diff_op or (self.parsed_op and is_diff_op):
      fail_parse(pos, 'compound set expressions containing `-` or `^` operators must be grouped with `[...]`', op)
    self.parsed_op = True
    self.parsed_diff_op |= is_diff_op
    self.operator = op
    self.operator_pos = pos

  def parse(self, pos, char):
    if char == '[':
      return CharsetParser(pos)
    elif char in '&-^':
      self.push_operator(pos, char)
    else:
      self.add_code(pos, ord(char))

  def parse_charset(self, pos, charset):
    for code in codes_for_ranges(charset):
      self.add_code(pos, code)

  def parse_name(self, pos, name):
    assert self.current_name_pos is not None
    assert self.current_name_chars is not None
    if not self.current_name_chars:
      fail_parse(self.current_name_pos, 'empty charset name.')
    name = ''.join(self.current_name_chars)
    try: named_charset = unicode_charsets[name]
    except KeyError: fail_parse(self.current_name_pos, 'unknown charset name.')
    self.codes.update(codes_for_ranges(named_charset))
    self.current_name_pos = None
    self.current_name_chars = None


  def finish(self, pos):
    if self.operator: self.flush_left(pos, msg_context='terminator')
    codes = self.codes_left or self.codes
    if not codes: fail_parse(self.pos, 'empty character set.')
    return Charset(self.pos, ranges=tuple(ranges_for_codes(sorted(codes))))


def genNFA(mode, named_rules):
  '''
  Generate an NFA from a set of rules.
  The NFA can be used to match against an argument string,
  but cannot produce a token stream directly.
  The `invalid` node is unreachable, and reserved for later use by the derived DFA.
  '''

  indexer = iter(count())
  def mk_node(): return next(indexer)

  start = mk_node() # always 0; see genDFA.
  invalid = mk_node() # always 1; see genDFA.

  matchNodeNames = { invalid: ('invalid' if (mode == 'main') else mode + '_invalid') }

  transitions = defaultdict(lambda: defaultdict(set))
  for name, rule in sorted(named_rules):
    matchNode = mk_node()
    rule.genNFA(mk_node, transitions, start, matchNode)
    dict_put(matchNodeNames, matchNode, name)
  literalRules = { name : rule.literalPattern for name, rule in named_rules if rule.isLiteral }
  return NFA(transitions=freeze(transitions), matchNodeNames=matchNodeNames, literalRules=literalRules)


def combine_dfas(mode_dfa_pairs):
  indexer = iter(count())
  def mk_node(): return next(indexer)
  transitions = {}
  matchNodeNames = {}
  literalRules = {}
  modes = []
  node_modes = {}
  for mode_name, dfa in sorted(mode_dfa_pairs, key=lambda p: '' if p[0] == 'main' else p[0]):
    remap = { node : mk_node() for node in sorted(dfa.allNodes) } # preserves existing order of dfa nodes.
    incomplete_name = 'incomplete' if (mode_name == 'main') else mode_name + '_incomplete'
    mode = Immutable(name=mode_name, start=remap[0], invalid=remap[1],
      invalid_name=dfa.matchNodeNames[1], incomplete_name=incomplete_name)
    modes.append(mode)
    node_modes.update((node, mode) for node in remap.values())
    def remap_trans_dict(d): return { c : remap[dst] for c, dst in d.items() }
    transitions.update((remap[src], remap_trans_dict(d)) for src, d in sorted(dfa.transitions.items()))
    matchNodeNames.update((remap[node], name) for node, name in sorted(dfa.matchNodeNames.items()))
    literalRules.update(dfa.literalRules)
  return (DFA(transitions=transitions, matchNodeNames=matchNodeNames, literalRules=literalRules), modes, node_modes)


def output(dfa, modes, node_modes, mode_transitions, rules_path, path, test, type_prefix, license):
  name = path_name_stem(rules_path)
  ext = path_ext(path)
  supported_exts = ['.swift']
  if ext not in supported_exts:
    failF('output path has unknown extension {!r}; supported extensions are: {}.',
      ext, ', '.join(supported_exts))
  if ext == '.swift':
    output_swift(dfa=dfa, modes=modes, node_modes=node_modes, mode_transitions=mode_transitions,
      rules_path=rules_path, path=path, test=test, type_prefix=type_prefix, license=license)


if __name__ == "__main__": main()

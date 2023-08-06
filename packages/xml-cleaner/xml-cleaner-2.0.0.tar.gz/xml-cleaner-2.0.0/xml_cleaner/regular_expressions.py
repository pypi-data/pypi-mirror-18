# -*- coding: utf-8 -*-
import re
import sys

from .constants import dashes

matching_dashes = dashes[:]
matching_dashes.remove("--+")
matching_dashes.append("-+")

word_with_alpha_and_period   = re.compile("^([^\.]+)(\.\s*)$")
one_letter_long_or_repeating = re.compile("^(?:(?:[a-z])|(?:[a-z](?:\.[a-z])+))$", re.IGNORECASE)
no_punctuation               = re.compile("^\w+$")
left_quote_shifter           = re.compile(u"((`‘(?!`))|(‘(?!‘))\s*)(?=.*\w)", re.UNICODE)
left_quote_converter         = re.compile(u'([«"“]\s*)(?=.*\w)', re.UNICODE)
left_single_quote_converter  = re.compile(u"(?:(\W|^))('\s*)(?=.*\w)", re.UNICODE)
right_single_quote_converter = re.compile(u"(['’]+)(?=\W|$)\s*", re.UNICODE)

if sys.version_info >= (3,3):
	dash_converter = re.compile("|".join(dashes))
else:
	dash_converter = re.compile(u"|".join(dashes))

simple_dash_finder           = re.compile("(-\s*)")
advanced_dash_finder         = re.compile("(" + "|".join(matching_dashes) + ")\s*")
url_file_finder              = re.compile("(?:[-a-zA-Z0-9@%._\+~#=]{2,256}://)?"
                                          "(?:www\.)?[-a-zA-Z0-9@:%\._\+~#=]{2,"
                                          "256}\.[a-z]{2,6}[-a-zA-Z0-9@:%_\+.~#"
                                          "?&//=]*\s*")
comma_shifter                = re.compile("(,(?!\d)\s*)")
remaining_quote_converter    = re.compile(u'(.)(?=["“”»])')
shifted_ellipses             = re.compile("(\.\.\.+|…)\s*")
shifted_standard_punctuation = re.compile("([\(\[\{\}\]\)\!\?#\$%;~|/:])\s*")
period_mover                 = re.compile(u"([a-zA-ZÀ-Þ]{2})([\./])\s+([a-zA-ZÀ-Þ]{2})")
pure_whitespace              = re.compile("\s+")
english_specific_appendages = re.compile(u"([A-Za-z])(?=['’]([dms])\\b)", re.UNICODE)
english_nots = re.compile(u"(.)(?=n['’]t\\b)", re.UNICODE)
english_contractions = re.compile(u"(.)(?=['’](ve|ll|re)\\b)")
french_appendages = re.compile(u"(\\b[tjnlsmdclTJNLSMLDC]|qu)['’](?=[^tdms])")
word_with_period = re.compile("[^\s\.]+\.{0,1}")

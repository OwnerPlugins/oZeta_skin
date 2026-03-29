# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os
import gettext


def localeInit():
    # getLanguage returns e.g. "fi_FI" for "language_country"
    lang = language.getLanguage()[:2]
    # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
    os.environ["LANGUAGE"] = lang
    gettext.bindtextdomain(
        "WeatherPlugin",
        resolveFilename(
            SCOPE_PLUGINS,
            "Extensions/WeatherPlugin/locale"))


def _(txt):
    t = gettext.dgettext("WeatherPlugin", txt)
    if t == txt:
        print("[WeatherPlugin] fallback to default translation for", txt)
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)

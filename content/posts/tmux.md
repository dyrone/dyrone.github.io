---
title: "Tmux"
date: 2022-10-19T19:59:29+08:00
draft: true
tags:
    - "tools"
---

## Copy text across the windows

> Origin: https://unix.stackexchange.com/questions/58763/copy-text-from-one-tmux-pane-to-another-using-vim

You'll have to use tmux shortcuts. Assuming your tmux command shortcut is the
default: Ctrl+b, then:

Ctrl+b, [ Enter copy(?) mode.

Move to start/end of text to highlight.

Ctrl+Space

Start highlighting text (on Arch Linux). When I've compiled tmux from source on
OSX and other Linux's, just Space on its own usually works. Selected text
changes the colours, so you'll know if the command worked.

Move to opposite end of text to copy.

Alt+w Copies selected text into tmux clipboard. On Mac, use Esc+w. Try Enter if
none of the above work.

Move cursor to opposite tmux pane, or completely different tmux window. Put the
cursor where you want to paste the text you just copied.

Ctrl+b, ] Paste copied text from tmux clipboard.

tmux is quite good at mapping commands to custom keyboard shortcuts.

See Ctrl+b,? for the full list of set keyboard shortcuts.


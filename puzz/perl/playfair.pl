#!/usr/bin/perl

open FHAND, "<dots.txt";
@lines = <FHAND>;

foreach $line (@lines) {
  @junk = split('',$line);
  foreach (0..$#junk) {
    print (($junk[$_] eq $junk[$_+1]) ? " ": "X");
  }
  print "\n";
}
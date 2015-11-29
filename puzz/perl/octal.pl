#!/usr/bin/perl

open FHAND, "<num8.txt";
@lines = <FHAND>;
close FHAND;
open FOO, ">base10.txt";

foreach (@lines) {
  chomp;
  @stuff = split('');
  $val = 0;
  while (scalar @stuff) {
    $val *= 8;
    $val += shift(@stuff);
  }
  print FOO $val, "\n";
}

close FOO;

#!/usr/bin/perl

open FHAND, "<code-vi.txt";
@lines = <FHAND>;
close FHAND;

chomp @lines;

foreach (@lines) {
  tr/a-z/A-Z/;
  tr/J/I/;
  s/[^A-Z]//g;
}

@codechars = split('',$lines[0]);

foreach (@codechars) {
  $_ = ord($_) - ord('A');
}

@code = split('',$lines[1]);
for $offset (0..$#codechars) {
  for $pos (0..$#code) {
    $val = $code[$pos];
    next if ($val !~ /[A-Z]/);
    $mo = $codechars[($offset + $pos) % scalar @codechars];
    $dec = (ord($val) - ord('A') - $mo + 26) % 26;
    print chr($dec + ord('A'));
  }
  print "\n";
}


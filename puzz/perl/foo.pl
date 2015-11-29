#!/usr/bin/perl

foreach (<>) {
  chomp;
  s/A-Z/a-z/g;
  next unless (/^...........$/);
  $l = 'a';
  next if (/$l.*$l/); $l = 'b';
  next if (/$l.*$l/); $l = 'c';
  next if (/$l.*$l/); $l = 'd';
  next if (/$l.*$l/); $l = 'e';
  next if (/$l.*$l/); $l = 'f';
  next if (/$l.*$l/); $l = 'g';
  next if (/$l.*$l/); $l = 'h';
  next if (/$l.*$l/); $l = 'i';
  next if (/$l.*$l/); $l = 'j';
  next if (/$l.*$l/); $l = 'k';
  next if (/$l.*$l/); $l = 'l';
  next if (/$l.*$l/); $l = 'm';
  next if (/$l.*$l/); $l = 'n';
  next if (/$l.*$l/); $l = 'o';
  next if (/$l.*$l/); $l = 'p';
  next if (/$l.*$l/); $l = 'q';
  next if (/$l.*$l/); $l = 'r';
  next if (/$l.*$l/); $l = 's';
  next if (/$l.*$l/); $l = 't';
  next if (/$l.*$l/); $l = 'u';
  next if (/$l.*$l/); $l = 'v';
  next if (/$l.*$l/); $l = 'w';
  next if (/$l.*$l/); $l = 'x';
  next if (/$l.*$l/); $l = 'y';
  next if (/$l.*$l/); $l = 'z';
  next if (/$l.*$l/); $l = '';
  print $_, "\n";
}


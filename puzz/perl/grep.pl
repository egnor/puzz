#!/usr/bin/perl

@files = ("words.txt","american.txt","propernames.txt");
@files = ("words.txt");

foreach $filename (@files) {
  open FHAND, "<".$filename;
  foreach $line (<FHAND>) {
    print $line if ($line =~

      /hunt/

    );
  }
  close FHAND;
}

$wait = <STDIN>;
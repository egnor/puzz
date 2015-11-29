#!/usr/bin/perl

open FHAND, "<code.txt";
@lines = <FHAND>;
close FHAND;

foreach (@lines) {
  s/ /_/g;
}

%mapping;
%count;

sub rbycount {
  $count{$b} <=> $count{$a};
}

chomp @lines;
@oldlines = @lines;

$prompt = "(switch which)? ";
print @lines;
print $prompt;
while ($cmd = <STDIN>) {
  chomp $cmd;
  if ($cmd !~ /^\w\w$/) {
    print "--Invalid command! (hh for help)\n";
    print @lines;
  } elsif ($cmd eq "hh") {
    print "hh for help\n";
    print "ww to write to out.txt\n";
    print "mm to show mapping/frequency\n";
    print "nn to show mappings by alphabet\n";
    print "cc for caesar-shift 1\n";
  } elsif ($cmd eq "ww") {
    open FHAND, ">out.txt";
    print FHAND @lines;
    close FHAND;
    print "written to out.txt\n";
  } elsif ($cmd eq "mm") {
    %mapping = ();
    %count = ();
    foreach (0..$#lines) {
      @old = split '', $oldlines[$_];
      @new = split '', $lines[$_];
      foreach (0..$#old) {
        next if ($old[$_] !~ /^\w$/);
        $mapping{$old[$_]} = $new[$_];
        $count{$old[$_]}++;
      }
    }
    @list = sort rbycount keys %mapping;
    @output = ();
    foreach (@list) {
      push @output, (sprintf "%s->%s:%3d   ", $_, $mapping{$_}, $count{$_});
    }
    $rows = int ((2 + scalar @output)/3);
    foreach (0..($rows-1)) {
      print $output[$_] if ($_ <= $#output);
      print $output[$rows+$_] if ($rows+$_ <= $#output);
      print $output[2*$rows+$_] if (2*$rows+$_ <= $#output);
      print "\n";
    }
  } elsif ($cmd eq "nn") {
    %mapping = ();
    %reverse = ();
    foreach (0..$#lines) {
      @old = split '', $oldlines[$_];
      @new = split '', $lines[$_];
      foreach (0..$#old) {
        next if ($old[$_] !~ /^\w$/);
        $mapping{$old[$_]} = $new[$_];
        $reverse{$new[$_]} = $old[$_];
      }
    }
    print "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";
    foreach ('A'..'Z') {
      $t = $mapping{$_};
      print (($t eq "") ? "?" : $t);
    }
    print "\n";
    print "\n";
    print "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";
    foreach ('A'..'Z') {
      $t = $reverse{$_};
      print (($t eq "") ? "?" : $t);
    }
    print "\n";
  } elsif ($cmd eq "cc") {
    @result = ();
    foreach $idx (0..$#lines) {
      @new = split '', $lines[$idx];
      foreach (@new) {
        if ($_ =~ /[a-yA-Y]/) {
          $_++;
        } elsif ($_ =~ /[zZ]/) {
          $_ =~ tr/zZ/aA/;
        }
      }
      push @result, join('',@new);
    }
    @lines = @result;
    print @lines;
  } else {
    $char1 = substr($cmd,0,1);
    $char2 = substr($cmd,1,1);
    foreach (@lines) {
      s/$char1/\|/g;
      s/$char2/$char1/g;
      s/\|/$char2/g;
    }
    for (0..$#lines) {
      print $lines[$_], "  ", $oldlines[$_], "\n";
    }
  }
  print $prompt;
}

#!/usr/bin/perl


use strict;
use FileHandle;
use Data::Dumper;

$| = 1;

my $dir = '.';

opendir(DIR, $dir) or die $!;

my @files;
my $anchor = shift;

my @stubs;

push(@stubs,$anchor);

while (my $file = readdir(DIR)) {
    next unless ($file =~ /$anchor-(.*)\.brh.dat/);

    my $stub = $file;
    $stub =~ s/$anchor-(.*)\.brh\.dat/$1/;

    push(@stubs,$stub);

}

closedir(DIR);

my $i = 1;

my %hits;
my @qids;

while ($i < scalar(@stubs)) {
    my $stub0 = $stubs[0];
    my $stub = $stubs[$i];
    
    my $brhfile = "$stub0-$stub.brh.dat";

    if (! -e $brhfile) {
	print "ERROR :No brhfile $brhfile\n";
    }
    my $fh = new FileHandle();
    
    $fh->open("<$brhfile");
    
    while (my $line = <$fh>) {

	chomp($line);
	
	my @f = split(/\t/,$line,5);
	
	my $found = $f[1];

	if ($found == 1) {
	    my $qid = $f[2];
	    my $hid = $f[3];
	    
	    $hits{$qid}{$stub}{'hid'} = $hid;
	    $hits{$qid}{$stub}{'line'} = $line;
	}
    }
    $fh->close();
    $i++;
}

#print Dumper(%hits);

foreach my $stub (@stubs) {  print "$stub\t";}
print "\n";

my @qids = keys(%hits);
#print Dumper(@qids);

foreach my $qid (@qids) {

    print $qid;
    
    my $i = 1;
    my $count = 0;
    while ($i < scalar(@stubs)) {

	my $hid = $hits{$qid}{$stubs[$i]}{'hid'};
	if ($hid eq "") { 
	    $hid = "-"; 
	} else {
	    $count++;
	}
	print "\t" . $hid;
	$i++;
    }
    print "\t$count\n";
}



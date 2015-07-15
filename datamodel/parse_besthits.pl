#!/usr/local/bin/perl

use strict;

$| = 1;

my $db1 = shift;
my $db2 = shift;

use FileHandle();

my $fh1 = new FileHandle();
my $fh2 = new FileHandle();

$fh1->open("<$db1");
$fh2->open("<$db2");


my %hits1;
my %hits2;

my $prev = undef;

while (my $line = <$fh1>) {

    chomp($line);

<<<<<<< HEAD
    if ($line =~ /^gi/) {
=======
    #if ($line =~ /^gi/) {
>>>>>>> f24e99b9a5c4fcc115203ebd7e12b8a08a35b53d
	my @f = split(/\t/,$line);

	my $qid = $f[0];
	my $hid = $f[1];

	if (!$prev || $prev ne $qid) {
	    $hits1{$qid}{'hid'} = $hid;
	    $hits1{$qid}{'line'} = $line;
	}

	$prev = $qid;
	

<<<<<<< HEAD
    }
=======
    #}
>>>>>>> f24e99b9a5c4fcc115203ebd7e12b8a08a35b53d
}

$prev = undef;

while (my $line = <$fh2>) {

    chomp($line);

<<<<<<< HEAD
    if ($line =~ /^gi/) {
=======
    #if ($line =~ /^gi/) {
>>>>>>> f24e99b9a5c4fcc115203ebd7e12b8a08a35b53d
	my @f = split(/\t/,$line);

	my $qid = $f[0];
	my $hid = $f[1];

	if (!$prev || $prev ne $qid) {
	    $hits2{$qid}{'hid'} = $hid;
	    $hits2{$qid}{'line'} = $line;

	}
	$prev = $qid;
<<<<<<< HEAD
    }
=======
    #}
>>>>>>> f24e99b9a5c4fcc115203ebd7e12b8a08a35b53d
}


foreach my $qid (keys(%hits1)) {
    my $hid  = $hits1{$qid}{'hid'};
    my $line = $hits1{$qid}{'line'};
    my $rqid = $hits2{$hid}{'hid'};

    my $found = 0;
    if ($qid eq $rqid) {
	$found = 1;
    }
    print "$db1\t$found\t$line\n";
}



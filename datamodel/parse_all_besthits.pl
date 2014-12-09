#!/usr/bin/perl


use strict;

$| = 1;

my $dir = '.';

opendir(DIR, $dir) or die $!;

my @files;

while (my $file = readdir(DIR)) {


    next unless ($file =~ m/\.pep.fa/);

    print "$file\n";
    push @files,$file;

}

closedir(DIR);


my $i = 0;

while ($i < scalar(@files)) {
    my $file1 = $files[$i];

    my $stub1 = $file1;
    $stub1 =~ s/(.*)\.pep\.fa/$1/;

    my $j = 0;

    while ($j < scalar(@files)) {
	if ($j != $i)  {
	    my $file2 = $files[$j];
	    my $stub2 = $file2;
	    $stub2 =~ s/(.*)\.pep\.fa/$1/;
	    
	    my $bfile1 = $stub1 . "-" . $stub2 . ".blastp";
	    my $bfile2 = $stub2 . "-" . $stub1 . ".blastp";
	    
	    print "Blast file $bfile1 $bfile2\n";
	    
	    my $cmd = "perl ./datamodel/parse_besthits.pl $bfile1 $bfile2 > $stub1-$stub2.brh.dat";
	    
	    print $cmd;
	    
	    system($cmd);
	}
	$j++;
    }
    $i++;
}

#!perl
#**********************************************************
#*                                                        *
#*   SelectMoleSame - Select all same molecules at once   *
#*                                                        *
#**********************************************************
# Version: 0.1
# Author: MS
# Date: 17/07/2024
#
# The script selects all the same molecules in the 3D structure
# and you could set them as a new set with a unique name. The 
# temporary file named "tmp.xtd" is created in the same directory
# of original file. it should be deleted automatically after the 
# script is executed, but you need to delete it manually now.
#
# Usage:
# variable $doc (line 25) according to the name of the 3D
# structure file.

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

my $doc = $Documents{"sorp.xsd"};

my $fragment = $doc->Selected->Atoms(0)->Fragment;
my $itemCount = $fragment->Atoms->Count;
my $docPattern = Documents->New("tmp.xsd");

$docPattern->CopyFrom($fragment);

foreach my $at (@{$docPattern->Atoms}) {$at->IsSelected = "NO";}
my $patternfrag = $docPattern->Atoms(0)->Fragment;
my $subPattern = $docPattern->Atoms;
my $substructures = $doc->FindPatterns($docPattern, $subPattern);

foreach my $substr (@{$substructures}) {
    my $fragment = $substr->Item(0)->Ancestors->Molecule;
    if ($fragment->Atoms->Count == $itemCount)  
    { foreach my $at (@{$substr->Items}) {$at->IsSelected = "YES";} }
    $substr->Delete;
}  

$docPattern->Delete; 
                     
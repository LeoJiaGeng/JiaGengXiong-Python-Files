use strict;
use warnings;
use MaterialsScript qw(:all);

# Author: Leo 

# Current version: 1.0
# Update log 
# 2024-10-8 Version: 1.0: The first version released by Leo
# counting how many frames in which the atom in set 1 is bonded to the atom in set 2 

###### Begin User INPUT ####################

my $doc = $Documents{"GGA-NVT-2000.xtd"};

my $setname1 = "Hatom";
my $setname2 = "Oatom";
my $bondcutoff = 1.20;
my $startframe = 1; 

my $Hatoms = $doc->UnitCell->Sets($setname1)->Atoms;
my $Oatoms = $doc->UnitCell->Sets($setname2)->Atoms;

####### End User INPUT #####################

# Step 1: define the functions of calculting the length of any two atoms

#Compute a vector as the delta between point1 & point2
sub Vector {
    my ($point1, $point2) = @_;

    return Point(X => $point1->X - $point2->X, 
                 Y => $point1->Y - $point2->Y,
                 Z => $point1->Z - $point2->Z);
}

#Calculate the length of a vector
sub Length {
    my ($vector) = @_;

    return sqrt($vector->X * $vector->X + $vector->Y * $vector->Y + $vector->Z * $vector->Z);
}

#Calculate the length of two atoms
sub IsBond {
    my ($atoms1, $atoms2) = @_;
    my $time = 0;
    my $lastbond = 0;
	
    foreach my $atom1 (@$atoms1) {
        foreach my $atom2 (@$atoms2) {
            my $val = Vector($atom1, $atom2);
            my $bond = Length($val);
            if($bond < $bondcutoff) {
                print "bond is $bond\n " ;
                $lastbond = $bond;	
                ++$time;				
            }  
        }
    }
    return ($lastbond, $time);
}

# Step 2: creat a new table to save calculting data

# Create the column for result in the sheet
my $std = Documents->New($doc->Name . " bonds.std");
my $bondssheet=$std->InsertSheet;
   $bondssheet->Title = "bonds";
   $bondssheet->ColumnHeading(0) = "frme number";
   $bondssheet->ColumnHeading(1) = "isBonds";
   $bondssheet->ColumnHeading(2) = "countBonds";

#  Read every frame and calculate the bond distance
my $numFrames = $doc->Trajectory->NumFrames;  
for (my $Counter = $startframe; $Counter <= $numFrames; ++$Counter) {  

    $doc->Trajectory->CurrentFrame = $Counter; 
    my ($lastbond, $bondscount) = IsBond($Hatoms, $Oatoms);
    $bondssheet->Cell($Counter-$startframe,0) = $Counter;
    $bondssheet->Cell($Counter-$startframe,1) = $lastbond;
    $bondssheet->Cell($Counter-$startframe,2) = $bondscount;
}

print "finshed! \n " ;


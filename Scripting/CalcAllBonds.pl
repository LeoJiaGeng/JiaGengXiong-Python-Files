use strict;
use warnings;
use MaterialsScript qw(:all);

# Author: Leo 

# Current version: 1.1
# Update log 
# 2024-10-8 Version: 1.0: The first version released
# counting how many frames in which the atom in set 1 is bonded to the atom in set 2 
# 2024-10-11 Version: 1.1: The second version released
# increasing the interval for frames to reduce the calculation
# 2024-10-15 Version: 1.3: The third version released
# print the detail of frame number to locate the energy line in text 

###### Begin User INPUT ####################

my $doc = $Documents{"GGA-NVT-2000.xtd"};

my $setname1 = "Hatom";
my $setname2 = "Oatom";
my $bondcutoff = 1.20;     # the distance of bonding
my $startframe = 1;        # the number of starting frames
my $countinterval = 2;     # the interval of counting frames

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
    my ($atoms1, $atoms2, $curnum) = @_;
    my $time = 0;
    my $lastbond = 0;
	
    foreach my $atom1 (@$atoms1) {
        foreach my $atom2 (@$atoms2) {
            my $val = Vector($atom1, $atom2);
            my $bond = Length($val);
            if($bond < $bondcutoff) {
                print "number of frame is $curnum, bond is $bond\n " ;
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
for (my $Counter = $startframe; $Counter <= $numFrames; $Counter += $countinterval) {  

    $doc->Trajectory->CurrentFrame = $Counter; 
    my ($lastbond, $bondscount) = IsBond($Hatoms, $Oatoms, $Counter);
    my $counternum = ($Counter-$startframe)/$countinterval;
    $bondssheet->Cell($counternum,0) = $Counter;
    $bondssheet->Cell($counternum,1) = $lastbond;
    $bondssheet->Cell($counternum,2) = $bondscount;
}

print "finshed! \n " ;


#!perl

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

# Author: Luminary (BiliBili UID: 677482886)

# Current version: 2.0
# Update log 
# 2022-12-11 Version: 1.0: The first version released
# 2024-09-04 Version: 2.0: The second version released by Leo
# increase the atoms number in the second set to avoid the error of molcular number

###### Begin User INPUT ####################

my $doc = $Documents{"Layer.xtd"};     #the xtd files to be analyzed

my $startframe=11;                          #the first frame number in xtd to be analyzed, generally after which the system should reach equilibrium 
my $Setname1 = 'I-C4';                      #the name of one set name in pair to be analyzed
my $Setname2 = 'N-C4-1' ;                   #the name of the other set in pair to be analyzed
my $Setname2_atoms = 12 ;                   #the number of atoms in the second set to be analyzed, used to calculate the density
my $RDF_cut  =  10 ;                        #Specify the cutoff, in A, for RDF calculation. All pair separations greater than this value are ignored.
my $Interval = 0.02;                        #Specify the bin width, in A, for RDF calculation.


####### End User INPUT #####################

# define constant

use constant PI => 3.14159265358979323846264338327950288419716939937510;


# Step 1: get the original RDF data 

# Calculate the RDF data using materialsScript
my $results = Modules->Forcite->Analysis->RadialDistributionFunction($doc, Settings(
	ActiveDocumentFrameRange => $startframe.'-END', 
	RDFBinWidth => $Interval, 
	RDFCutoff => $RDF_cut, 
	RDFSetA => $Setname1, 
	RDFSetB => $Setname2));
my $outRDFChart = $results->RDFChart;
my $outRDFChartAsStudyTable = $results->RDFChartAsStudyTable;


# Step 2: calculate the average box volume in all the frames to be analyzed

# Copy the original RDF table
my $std = Documents->New($doc->Name . " CN.std");
   $std->CopyFrom($outRDFChartAsStudyTable);
my $dataSheet = $std->Sheets(2); 
   $dataSheet->Title = "RDF and CN";
   $dataSheet->InsertColumn(2, "CN");
   
# Create the column for box volume in the sheet   
my $volumesheet=$std->InsertSheet;
   $volumesheet->Title = "Box volume";
   $volumesheet->ColumnHeading(0) = "frme number";
   $volumesheet->ColumnHeading(1) = "Box volume (A^3)";

#  Read every frame and calculate the box volume, why not use the analysistoolbox?  
my $numFrames = $doc->Trajectory->NumFrames;   
my $totalvolume  = 0;
for (my $Counter = $startframe; $Counter <= $numFrames; ++$Counter) 
	{  
	
	my $temdoc = Documents->New("$doc"."_$Counter.xsd"); 
	$doc->Trajectory->CurrentFrame = $Counter; 
	$temdoc->CopyFrom($doc);
	my $volume = $temdoc->SymmetrySystem->Volume;
	$volumesheet->Cell($Counter-$startframe,0) = $Counter;
	$volumesheet->Cell($Counter-$startframe,1) = $volume;
	$temdoc->Discard;
	$totalvolume += $volume;
	}
# Now calculate the average box volume
my $avelvolume  = $totalvolume/($numFrames-$startframe+1);  

print " The average box volume (A^3) is $avelvolume\n " ;

   
# Step 3: calculate the CN from original RDF data 

# calculate the number of atoms and the density of the second set 
my $CN  = 0;
my $rowCount = $dataSheet->RowCount;
my $AtomNuminSet=($doc->UnitCell->Sets("$Setname2")->Atoms->Count)/$Setname2_atoms;
my $rho= $AtomNuminSet/$avelvolume;

# calculate the CN using the formula rho*4*PI*r^2*g(r)
for (my $rowNum = 1; $rowNum <= $rowCount; ++$rowNum) 
   {
   my $radius = $dataSheet->Cell($rowNum-1,0);
   my $g_R    = $dataSheet->Cell($rowNum-1,1);
   $CN       += $rho*4*PI*$radius*$radius*$g_R*$Interval;
   $dataSheet->Cell($rowNum-1,2) = $CN;
   }
   
# Step 4:  Check the CN

# read the Rmax value(cutoff) from the last row of the table
my $Rmax     = $dataSheet->Cell($rowCount-1,0);
#my $Rmax     = $Rmax+$Interval;
print "the Rmax is $Rmax\n" ; 

# Calculate the ball volume at Rmax
my $VatRmax  = 4/3*PI*$Rmax*$Rmax*$Rmax;
# calculate the CN using the formula V*rho
my $CNmax_pre= $VatRmax*$rho;
# read the CN value from the last row of the table
my $CNmax_cal= $dataSheet->Cell($rowCount-1,2);
# calculate the deviation between the full box and the cutoff sphere
my $CN_deviation=($CNmax_cal-$CNmax_pre)/$CNmax_pre*100;

print "the total atom number in Set 2 is $AtomNuminSet\n " ;
print "the predicted CN at Rmax is $CNmax_pre\n " ;
print "the calculted CN at Rmax is $CNmax_cal\n " ;
print "the deviation is $CN_deviation%\n " ;


   


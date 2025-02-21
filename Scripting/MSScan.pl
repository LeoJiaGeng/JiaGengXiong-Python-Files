#!perl
use strict;
use warnings;
use MaterialsScript qw(:all);

# Modules: Materials Visualizer, DMol3

# For the restrictive optimization in MS, you should fix the bond length by yourself. 
# It is worth noting that you need to adjust it manually and put all the substances on the Y axis.

# run module of dmol3
sub run_doml3 {
    my ($inputdoc) = @_;

    my $results = Modules->DMol3->Energy->Run($inputdoc, Settings(
        UseSymmetry => "No", 
        Quality => "Medium", 
        Multiplicity => "Singlet", 
        UseFormalSpin => "No", 
        TheoryLevel => "GGA", 
        BasisFile => "4.4", 
        AtomCutoff => 4.2, 
        MaximumSCFCycles => 500, 
        UseSmearing => "Yes", 
        Smearing => 0.01, 
        Iterations => 1000, 
        MaximumDisplacement => 0.15));
    my $result_structure = $results->Structure;
    my $result_energy = $results->TotalEnergy;
    print "result energy: $result_energy \n";
    return $result_structure, $result_energy;
}

##########################################################################################
# User editable settings

# The name of all the xsd file
my @allxsdnames = ('Al4O6', 'AP-HClO4', 'AP-NH3', 'BGAP-CH3N3', 'BGAP-CH3OCH3', 'BGAP-CH3OH', 'BTTN', 'CH3CN', 'CH3OCN', 'CL-20', 'CO2', 'H2CO3', 'H2O', 'HDI', 'HMX', 'HTCE', 'IPDI', 'NG', 'O2', 'PEG', 'PET-1', 'PET-2', 'TDI', 'TEGDN'); 
my $calc_flag = 0; # set to 1 to run the calculation and structure, 0 is only structure
my $bmole = "AL";  # the movement of structure

# Settings for the scan steps
my $step_type = 0; # set to 0 to use below z_list; set 1 to use start_z and end_z 
our @z_list = (0.1, 0.2, 1, 2, 3);
my $start_z = 1;
my $end_z = 3;

# End user editable settings
##########################################################################################

if ($step_type == 1) {
    # use same step size for all z values
    @z_list=($start_z..$end_z);
    print "z_list: @z_list  \n";
}

foreach my $onexsdname (@allxsdnames) {

    my $doc = $Documents{"$onexsdname.xsd"};

    # create the table to save detail data
    my $std = Documents->New("$onexsdname-scan.std");
    my $scansheet=$std->InsertSheet;
    $scansheet->Title = "scan_results";
    $scansheet->ColumnHeading(0) = "Index";
    $scansheet->ColumnHeading(1) = "Start_frme";
    $scansheet->ColumnHeading(2) = "End_frme";
    $scansheet->ColumnHeading(3) = "Energy";

    my $index = 0;
    foreach my $z (@z_list){
        # Create a new document copy the original document
        my $scandoc = Documents->New("$onexsdname-$z.xsd");
        $scandoc->CopyFrom($doc);

        # get all atoms corrdinates
        my $bmoleatoms = $scandoc->UnitCell->Sets($bmole)->Atoms;

        foreach my $atom (@$bmoleatoms) {
            # add the atom to the surface at the minimum Z value
            $atom->Y += $z;
        }

        # add the index and original structure to the document
        $scansheet->Cell($index,0) = $index+1;
        $scansheet->Cell($index,1) = $scandoc;

        my $structure = $scandoc;
        my $energy = 0;
        # control the calculation
        if ($calc_flag == 1) {
            # run this document using dmol3
            my ($structure, $energy) = run_doml3($scandoc); 
        }

        # add the end structure to the document
        $scansheet->Cell($index,2) = $structure;
        $scansheet->Cell($index,3) = $energy;

        $index++;
        print "finshed $index times \n " ;
    }
}
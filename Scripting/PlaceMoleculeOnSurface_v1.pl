#!perl

use strict;
use MaterialsScript qw(:all);

# A short script to show how to use a sub-routine to place a molecule on a surface.
# This script passes in the surface and sorbant documents together with the
# minimum Z value to start placing the molecule on the surface.

# The molecule is first added at the minimum Z value and is then translated until
# there is only one close contact. The minimum Z value can be set to zero but this
# will mean more close contacts calculations.

# Note. This script assumes that the molecule is oriented with C along Z and B in
# YZ plane and will give an error if it is not.

###########################################################################################
# Begin user editable settings

my $surfaceXSD = "FeSurf"; 		          # The name of the surface document
my $minimumZ = 5.0;				          # Starting value of Z for molecule to be placed on surface
my @sorbantXSD = ('Al4O6', 'AP-HClO4', 'AP-NH3', 'BGAP-CH3N3', 'BGAP-CH3OCH3', 'BGAP-CH3OH', 'BTTN', 'CH3CN', 'CH3OCN', 'CL-20', 'CO2', 'H2CO3', 'H2O', 'HDI', 'HMX', 'HTCE', 'IPDI', 'NG', 'O2', 'PEG', 'PET-1', 'PET-2', 'TDI', 'TEGDN'); # The name of the study table containing the sorbant
my $set="AL-4";

# End user editable settings
############################################################################################

my $fractionalZStart;
my $orientation;
my $surfaceDoc ;
my $sorbantDoc ;

foreach my $structure (@sorbantXSD) {
    print "Processing structure: $structure\n";

    # Set the documents up based on the names specified above
    $surfaceDoc = $Documents{"$surfaceXSD.xsd"};
    $sorbantDoc = $Documents{"$structure.xsd"};

    # Check that the alignment is correct and die if it is not
    $orientation = $surfaceDoc->UnitCell->Lattice3D->OrientationConvention;

    if ($orientation ne "C along Z, B in YZ plane") {
        die "Please change the orientation of the structure to C along Z, B in YZ plane";
    }

    # Get the length in the C direction
    my $lengthC = $surfaceDoc->UnitCell->Lattice3D->LengthC;

    # Converts the starting Z coordinate into fractional coordinates
    $fractionalZStart = $minimumZ / $lengthC;

    # Place the molecule on the surface
    my $sorbedSurface = place_molecule_on_surface($surfaceDoc, $fractionalZStart, $sorbantDoc, $surfaceXSD, $structure,$set);

    print "Calculation complete.\n";
}

# Subroutine to place the molecule on the surface
sub place_molecule_on_surface {

    my ($surfaceDoc, $minimumZ, $sorbant, $surf, $mol,$set) = @_;

    # Create a centroid to translate
    $sorbant->CreateCentroid($sorbant->Atoms);

    # Create a new document containing the sorbed surface and copy the sorbant in
    my $sorbedSurface = Documents->New("$surf-$mol.xsd");

    $sorbedSurface->CopyFrom($surfaceDoc);
    $sorbedSurface->CopyFrom($sorbant);
    $sorbant->Centroids->Delete;

    # Define the centroid for translating and the molecule for the close contacts calculation
    my $centroid = $sorbedSurface->UnitCell->Centroids(0);
    my $sorbantMolecule = $centroid->Ancestors->Molecule;

    # Place molecule randomly in X and Y but at fractionalZStart value
    my $set = $surfaceDoc->UnitCell->Sets("$set")->Atoms;
    my $n=0; my $x=0; my $y=0; my $z=0;

    foreach my $atom (@$set) {
    # my $atom = $surfaceDoc->Atoms(0);
    #$atom = $surfaceDoc->UnitCell->Atoms($i-1);
        my $fxyz = $atom->FractionalXYZ;

        $n++;
        $x += $fxyz->X;
        $y += $fxyz->Y;
        $z += $fxyz->Z;
        #printf "Atom coordinates: $x $y $z\n";
    }
    $x /= $n;
    $y /= $n;

    printf "Atom coordinates: $x $y $z\n";

    $centroid->FractionalXYZ=Point({X=>$x, Y=>$y, Z=>$fractionalZStart});
    # forbidden rotation fixed direction
    # $centroid->RotateAbout(rand(360),$centroid->CentroidXYZ);

    my $closeContacts = 10;
    my $attemptCounter = 0;

    # Translate the molecule in the Z-direction until there is only 1 close contact
    while ($closeContacts > 0) {
        $centroid->Translate(Point(X=>0, Y=>0, Z=>0.5));
        $sorbantMolecule->CalculateCloseContacts;
        $closeContacts = $sorbedSurface->UnitCell->CloseContacts->Count;
        print "Translated, close contacts are $closeContacts.\n";

        ++$attemptCounter;
        if ($attemptCounter > 1000) {
            die "Tried to place molecule too many times.\n\n";
        }
    }

    print "Successfully placed molecule after $attemptCounter attempts.\n";

    $centroid->Delete;
    return $sorbedSurface;
}

#!perl
#**********************************************************
#*                                                        *
#*   SetInitVel - set initial velocity for atoms          *
#*                                                        *
#**********************************************************
# Version: 0.1
# Author: MS
# Date: 19/07/2024
#
# The script set initial velocity for atoms in a 3D structure
#
# Usage:
# variable $doc (line 21) according to the name of the 3D
# structure file. variable $set (line 23) according to the name
# of the set of atoms to be set initial velocity.

use strict;
use MaterialsScript qw(:all);

my $doc = $Documents{"$doc"};

my $C4 = $doc->UnitCell->Sets("$set")->Atoms;

# the units of initial velocity is Å/ps = 100 m/s 
foreach my $atom (@$C4) {
                $atom->Velocity = Point ( X => 0, Y => 0, Z => -0.01 );}

my $results = Modules->Forcite->Dynamics->Run($doc, Settings(
	Quality => "Fine", 
	CurrentForcefield => "COMPASS", 
	ChargeAssignment => "Forcefield assigned", 
	Ensemble3D => "NVT", 
	Temperature => 300, 
    TimeStep => 1, 
	NumberOfSteps => 50000, 
    TrajectoryFrequency => 1000, 
	InitialVelocities => "Current",
    Thermostat => "NHL",
    WriteForces => "No",
    WriteVelocities => "Yes",
    ));
my $outTrajectory = $results->Trajectory;


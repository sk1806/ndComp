 g++ ./geometry_geant4_create_export.C -o geometry_export `geant4-config --cflags --libs` `root-config --cflags --libs` -lxerces-c -lGeom
# Note:  Requires Geant4 to be compiled with GDML

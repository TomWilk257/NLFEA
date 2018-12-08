# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
# Import relevant modules 
def FreqAnalysis():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    import os
# Import geometry as STEP file to create the part, change geometryFile property for other part types
    File = 'C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/GIP/BeamGeom.stp'
    filename_w_ext = os.path.basename(File)
    filename, file_extension = os.path.splitext(filename_w_ext)
    step = mdb.openStep(File, scaleFromFile=OFF)
    mdb.models['Model-1'].PartFromGeometryFile(name=filename, geometryFile=step, 
        combine=False, mergeSolidRegions=True, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY, scale=0.001) # Geometry created in mm, scale adjusts to m (SI)
    #Then change part name to Beam
    if filename!='Beam':
        mdb.models['Model-1'].parts.changeKey(fromName=filename, toName='Beam') # To fit with the pre-written variable names  
    p = mdb.models['Model-1'].parts['Beam']
    ## material properties and name
    mdb.models['Model-1'].Material(name='Steel') # Could build in prperty inputs
    mdb.models['Model-1'].materials['Steel'].Density(table=((7850, ), ))
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000000000, 0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Steel', thickness=None)
    ## applying it to the model
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    region = (c,)
    p = mdb.models['Model-1'].parts['Beam']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Beam']
    a.Instance(name='Beam-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
## create frequency analysis step
    mdb.models['Model-1'].FrequencyStep(name='Frequency', previous='Initial', 
        limitSavedEigenvectorRegion=None, numEigen=10) # numEigen = no of modes analysed
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Frequency')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)
## Clamped boundary conditions
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Beam-1'].faces
    fixed_ptx=0
    fixed_pty=0
    fixed_ptz=0
    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
    fixed_end_face = f1.findAt((fixed_pt,))
    myRegion = regionToolset.Region(faces=fixed_end_face)
    mdb.models['Model-1'].EncastreBC(name='Clamped-1', createStepName='Initial', 
        region=myRegion, localCsys=None)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
## Viewport
    p1 = mdb.models['Model-1'].parts['Beam']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
##Meshing
    p=mdb.models['Model-1'].parts['Beam']
    c=p.cells.findAt((0,0,0.325),)
    pickedregions=(c,)
    ElemType1=mesh.ElemType(elemCode=C3D20, secondOrderAccuracy=OFF)
    p.setElementType(regions=pickedregions, elemTypes=(ElemType1,))
    p.setMeshControls(regions=pickedregions, elemShape=HEX)
    p.seedPart(size=0.010, deviationFactor=0.01)
    p.generateMesh()
    p = mdb.models['Model-1'].parts['Beam']
##Viewport
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
## Generate matrices
    mdb.models['Model-1'].keywordBlock.synchVersions(storeNodesAndElements=False)
    mdb.models['Model-1'].keywordBlock.insert(24, """
    ** ----------------------------------------------------------------
    **
    * Step, name=exportmatrix
    *matrix generate, mass, stiffness
    *matrix output, mass, stiffness, format=coordinate
    *end step
    **
    **""")
    ## Run job
    mdb.Job(name='Frequency', model='Model-1', description='Frequency Analysis', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Frequency'].submit(consistencyChecking=OFF)
    session.mdbData.summary()
FreqAnalysis()

def Saving():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    #mdb.saveAs(pathName='C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/ExperimentalBeamFreq')
    mdb.saveAs(pathName='C:/temp/ExperimentalBeamFreq')
Saving()





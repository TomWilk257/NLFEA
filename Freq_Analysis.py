# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

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
    ## profile for extrusion created
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    ## rectangular profile
    s.rectangle(point1=(0.015, 0.001), point2=(-0.015, -0.001))
    ## Type of extrusion 
    p = mdb.models['Model-1'].Part(name='Beam', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Beam']
    p.BaseSolidExtrude(sketch=s, depth=0.65) ## length of extrusion
    s.unsetPrimaryObject()
    #End of sketching profile
    #Or can be imported
##    step = mdb.openStep(
##        'C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/GIP/BeamGeom.stp', 
##        scaleFromFile=OFF)
##    mdb.models['Model-1'].PartFromGeometryFile(name='BeamGeom', geometryFile=step, 
##        combine=False, mergeSolidRegions=True, dimensionality=THREE_D, 
##        type=DEFORMABLE_BODY)
##    mdb.models['Model-1'].parts.changeKey(fromName='BeamGeom', toName='Beam')
##    #Then change part name to Beam
##    p = mdb.models['Model-1'].parts['Beam']
    ## changing the view
##    session.viewports['Viewport: 1'].setValues(displayedObject=p)
##    del mdb.models['Model-1'].sketches['__profile__']
##    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
##        engineeringFeatures=ON)
##    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
##        referenceRepresentation=OFF)
    ## material properties and name
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Density(table=((7850, ), ))
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((210000000000, 0.3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Steel', thickness=None)
    ## applying it to the model
    p = mdb.models['Model-1'].parts['Beam']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(cells=cells, name='Set-1')
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
##    a = mdb.models['Model-1'].rootAssembly
##    f1 = a.instances['Beam-1'].faces
##    fixed_ptx=0
##    fixed_pty=0
##    fixed_ptz=0
##    fixed_pt=(fixed_ptx,fixed_pty,fixed_ptz)
##    fixed_end_face = f1.findAt((fixed_pt,))
##    myRegion = regionToolset.Region(faces=fixed_end_face)
## Clamped boundary conditions
##    mdb.models['Model-1'].EncastreBC(name='Clamped', createStepName='Frequency', 
##        region=myRegion, localCsys=None)
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
##    Region=regionToolset.Region(faces=p.faces[:])
    pickedregions=(c,)
    ElemType1=mesh.ElemType(elemCode=C3D20, secondOrderAccuracy=OFF)
    p.setElementType(regions=pickedregions, elemTypes=(ElemType1,))
##    ElemType2=mesh.ElemType(elemCode=B31H, secondOrderAccuracy=ON)
##    region = a.instances['Beam-1'].edges
##    a.Set(edges=region, name='Set-edges')
##    edges = a.sets['Set-edges']
##    p.setElementType(regions=edges, elemTypes=(ElemType2,))
    p.setMeshControls(regions=pickedregions, elemShape=HEX)
    p.seedPart(size=0.03, deviationFactor=0.01)
##    p.seedEdgeByNumber(edges=, number=4)
    p.generateMesh()
    p = mdb.models['Model-1'].parts['Beam']
##Viewport
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
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

##    o3 = session.openOdb(name='C:/temp/Frequency.odb')
##    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.animationController.setValues(animationType=HARMONIC, viewports=(
##        'Viewport: 1', ))
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=TIME_HISTORY)
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=SCALE_FACTOR)
##    session.animationController.play(duration=UNLIMITED)
##    session.animationController.setValues(animationType=HARMONIC)
##    session.animationController.play(duration=UNLIMITED)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=3)
##    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
##        CONTOURS_ON_DEF, ))



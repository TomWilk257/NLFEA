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
    import csv
 #Or can be imported
    step = mdb.openStep(
        'C:/Users/tw15036/OneDrive - University of Bristol/Documents/Year 4/GIP/BeamGeom.stp', 
        scaleFromFile=OFF)
    mdb.models['Model-1'].PartFromGeometryFile(name='BeamGeom', geometryFile=step, 
        combine=False, mergeSolidRegions=True, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY, scale=0.001)
    #Then change part name to Beam
    mdb.models['Model-1'].parts.changeKey(fromName='BeamGeom', toName='Beam')    
    p = mdb.models['Model-1'].parts['Beam']
## material properties and name
    mdb.models['Model-1'].Material(name='Steel')
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
##Apply Loading
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', nlgeom=ON)
    instanceNodes = mdb.models['Model-1'].rootAssembly.instances['Beam-1'].nodes
    #Import Forces
    file=csv.reader(open('C:\\Users\\tw15036\\OneDrive - University of Bristol\\Documents\\Year 4\\GIP\\Abaqus Output Files\\myFile2.csv','r'))
    n=[]
    for row in file:
        n.append(row)
    for i in range(0,len(n)):      
        #nodeLabel = tuple(range(1,100))
        nodeLabel=[i]
        [cf11,cf22,cf33]=map(float,n[i])
        meshNodeObj = instanceNodes.sequenceFromLabels(nodeLabel)
        myRegion = regionToolset.Region(nodes=meshNodeObj)
        mdb.models['Model-1'].ConcentratedForce(name='Load-'+str(i), createStepName='Step-1', 
           region=myRegion, cf1=cf11, cf2=cf22, cf3=cf33, distributionType=UNIFORM, field='', 
           localCsys=None)
    ##Viewport
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=ON, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    ## Run job
    mdb.Job(name='Mode_Shape', model='Model-1', description='Mode Shape', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Mode_Shape'].submit(consistencyChecking=OFF)
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



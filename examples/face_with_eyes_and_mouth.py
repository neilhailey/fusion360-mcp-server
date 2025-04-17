"""
3D Smiley Face

This script creates a 3D smiley face in Fusion 360 with the following steps:
1. Start with a sketch on the XY plane
2. Draw a circle with diameter 50 mm
3. Draw two circles with diameter 5 mm at (-15, 15) mm and (15, 15) mm for the eyes
4. Draw a circle with diameter 20 mm at (0, -10) mm for the mouth
5. Extrude the profile (with the holes) to a height of 10 mm
6. Add a 1.5 mm fillet to all edges

To run this script in Fusion 360:
1. Open Fusion 360
2. Click on the "Scripts and Add-Ins" button in the toolbar
3. Click the "+" button to add a new script
4. Select this file
5. Click "Run"
"""

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design
        rootComp = design.rootComponent

        # 1. Create a new sketch on the XY plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # 2. Draw a circle with diameter 50 mm
        circles = sketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        faceCircle = circles.addByCenterRadius(centerPoint, 50.0)  # 50 mm diameter = 25 mm radius

        # 3. Draw two circles with diameter 5 mm at (-15, 15) mm and (15, 15) mm for the eyes
        leftEyeCenter = adsk.core.Point3D.create(-15, 15, 0)
        rightEyeCenter = adsk.core.Point3D.create(15, 15, 0)
        leftEye = circles.addByCenterRadius(leftEyeCenter, 2.5)  # 5 mm diameter = 2.5 mm radius
        rightEye = circles.addByCenterRadius(rightEyeCenter, 2.5)  # 5 mm diameter = 2.5 mm radius

        # 4. Draw a circle with diameter 20 mm at (0, -10) mm for the mouth
        mouthCenter = adsk.core.Point3D.create(0, -10, 0)
        mouth = circles.addByCenterRadius(mouthCenter, 10.0)  # 20 mm diameter = 10 mm radius

        # 5. Extrude the profile (with the holes) to a height of 10 mm
        # Get the profile defined by the face circle with the eyes and mouth holes
        prof = sketch.profiles.item(0)  # The outer profile with the holes
        
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Define the extrusion distance
        distance = adsk.core.ValueInput.createByReal(10.0)  # 10 mm height
        extInput.setDistanceExtent(False, distance)
        
        # Create the extrusion
        ext = extrudes.add(extInput)

        # 6. Add a 1.5 mm fillet to all edges
        # Get all edges to apply the fillet
        body = ext.bodies.item(0)
        edges = adsk.core.ObjectCollection.create()
        
        for edge in body.edges:
            edges.add(edge)
        
        # Create a fillet input
        fillets = rootComp.features.filletFeatures
        filletInput = fillets.createInput()
        filletInput.addConstantRadiusEdgeSet(edges, adsk.core.ValueInput.createByReal(1.5), False)  # Reduced from 4mm to 1.5mm
        filletInput.isG2 = False
        filletInput.isRollingBallCorner = True
        
        # Create the fillet
        fillets.add(filletInput)
        
        ui.messageBox('3D Smiley Face created successfully')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

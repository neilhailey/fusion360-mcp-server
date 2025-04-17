"""
Circle with Hole and Fillets

This script creates a 3D shape in Fusion 360 with the following steps:
1. Start with a sketch on the XY plane
2. Draw a circle with diameter 50 mm
3. Draw a circle with radius 20 mm at the center of the circle
4. Extrude the profile (with the hole) to a height of 10 mm
5. Add a 2 mm fillet to all edges

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
        outerCircle = circles.addByCenterRadius(centerPoint, 25.0)  # 50 mm diameter = 25 mm radius

        # 3. Draw a circle with radius 20 mm at the center of the circle
        innerCircle = circles.addByCenterRadius(centerPoint, 20.0)  # 20 mm radius

        # 4. Extrude the profile (with the hole) to a height of 10 mm
        # Get the profile defined by the outer circle with the hole
        prof = sketch.profiles.item(0)  # The outer profile with the hole
        
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Define the extrusion distance
        distance = adsk.core.ValueInput.createByReal(10.0)  # 10 mm height
        extInput.setDistanceExtent(False, distance)
        
        # Create the extrusion
        ext = extrudes.add(extInput)

        # 5. Add a 2 mm fillet to all edges
        # Get all edges to apply the fillet
        body = ext.bodies.item(0)
        edges = adsk.core.ObjectCollection.create()
        
        for edge in body.edges:
            edges.add(edge)
        
        # Create a fillet input
        fillets = rootComp.features.filletFeatures
        filletInput = fillets.createInput()
        filletInput.addConstantRadiusEdgeSet(edges, adsk.core.ValueInput.createByReal(2.0), False)  # 2 mm fillet
        filletInput.isG2 = False
        filletInput.isRollingBallCorner = True
        
        # Create the fillet
        fillets.add(filletInput)
        
        ui.messageBox('Circle with hole and fillets created successfully')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

"""
Example: Rectangle with Hole and Fillets

This script creates a 3D shape in Fusion 360 with the following specifications:
1. Start with a sketch on the XY plane
2. Draw a rectangle 20x10 mm
3. Draw a circle with radius 3 mm at the center of the rectangle
4. Extrude the profile (with the hole) to a height of 5 mm
5. Add a 1 mm fillet to all edges

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
        
        # 2. Draw a rectangle 20x10 mm
        # We'll center the rectangle at the origin
        rectangles = sketch.sketchCurves.sketchLines
        rectangle = rectangles.addTwoPointRectangle(
            adsk.core.Point3D.create(-10, -5, 0),  # Bottom-left corner
            adsk.core.Point3D.create(10, 5, 0)     # Top-right corner
        )
        
        # 3. Draw a circle with radius 3 mm at the center of the rectangle
        circles = sketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)  # Center of the rectangle
        circle = circles.addByCenterRadius(centerPoint, 3)
        
        # 4. Extrude the profile (with the hole) to a height of 5 mm
        # Get the profile that includes the rectangle with the hole
        profiles = sketch.profiles
        # The outer profile should be at index 0
        outerProfile = profiles.item(0)
        
        # Create an extrusion
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(outerProfile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Define the extrusion distance
        distance = adsk.core.ValueInput.createByReal(5)  # 5 mm height
        extInput.setDistanceExtent(False, distance)
        
        # Create the extrusion
        extrude = extrudes.add(extInput)
        
        # 5. Add a 1 mm fillet to all edges
        # Get the body created by extrusion
        body = rootComp.bRepBodies.item(0)
        
        # Create a fillet feature
        fillets = rootComp.features.filletFeatures
        
        # Create an object collection for all edges
        edgeCollection = adsk.core.ObjectCollection.create()
        
        # Add all edges to the collection
        for edge in body.edges:
            edgeCollection.add(edge)
        
        # Create the fillet input
        filletInput = fillets.createInput()
        
        # Set the fillet radius to 1 mm
        filletRadius = adsk.core.ValueInput.createByReal(1)
        
        # Add the edges to the fillet with the specified radius
        filletInput.addConstantRadiusEdgeSet(edgeCollection, filletRadius, True)
        
        # Create the fillet
        fillet = fillets.add(filletInput)
        
        ui.messageBox('Rectangle with hole and fillets created successfully')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

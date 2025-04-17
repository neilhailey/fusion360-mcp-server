"""
Smiley Face in Fusion 360

This script creates a 3D smiley face in Fusion 360 with the following steps:
1. Create a sketch of a circle in the center of the xy plane with a diameter of 50mm
2. Extrude the circle up 5mm
3. Start a sketch on the top surface of the extruded circle
4. Create two circles (eyes) in the upper regions with diameter 5mm
5. Create a circle (smile) centered on the y axis, towards the bottom
6. Extrude the 3 circles -3mm to cut into the first body

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
        
        # 1. Create a sketch of a circle in the center of the xy plane with a diameter of 50mm
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        # Draw the main circle (face)
        circles = sketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        mainCircle = circles.addByCenterRadius(centerPoint, 25)  # 50mm diameter = 25mm radius
        
        # 2. Extrude the circle up 5mm
        profiles = sketch.profiles
        faceProfile = profiles.item(0)
        
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(faceProfile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        distance = adsk.core.ValueInput.createByReal(5)  # 5mm height
        extInput.setDistanceExtent(False, distance)
        
        faceExtrude = extrudes.add(extInput)
        
        # 3. Start a sketch on the top surface of the extruded circle
        # Get the top face of the extruded circle
        body = rootComp.bRepBodies.item(0)
        topFace = None
        
        for face in body.faces:
            # Find the face that's parallel to the XY plane and has a positive Z value
            if abs(face.geometry.normal.z - 1) < 0.001:
                topFace = face
                break
        
        # Create a sketch on the top face
        topSketch = sketches.add(topFace)
        
        # 4. Create two circles (eyes) in the upper regions with diameter 5mm
        # Left eye - positioned in the upper left quadrant
        leftEyeCenter = adsk.core.Point3D.create(-10, 10, 0)
        leftEye = topSketch.sketchCurves.sketchCircles.addByCenterRadius(leftEyeCenter, 2.5)  # 5mm diameter = 2.5mm radius
        
        # Right eye - positioned in the upper right quadrant
        rightEyeCenter = adsk.core.Point3D.create(10, 10, 0)
        rightEye = topSketch.sketchCurves.sketchCircles.addByCenterRadius(rightEyeCenter, 2.5)  # 5mm diameter = 2.5mm radius
        
        # 5. Create a circle (smile) centered on the y axis, towards the bottom
        smileCenter = adsk.core.Point3D.create(0, -10, 0)
        smile = topSketch.sketchCurves.sketchCircles.addByCenterRadius(smileCenter, 7.5)  # 15mm diameter = 7.5mm radius
        
        # 6. Extrude the 3 circles -3mm to cut into the first body
        # Get the profiles for the eyes and smile
        topProfiles = topSketch.profiles
        
        # Create a collection of profiles to extrude
        profileCollection = adsk.core.ObjectCollection.create()
        for i in range(topProfiles.count):
            profileCollection.add(topProfiles.item(i))
        
        # Create the extrusion to cut into the body
        cutInput = extrudes.createInput(profileCollection, adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        # Set the extrusion distance to -3mm (negative to cut into the body)
        cutDistance = adsk.core.ValueInput.createByReal(3)
        cutInput.setDistanceExtent(False, cutDistance)
        
        # Create the cut
        cutExtrude = extrudes.add(cutInput)
        
        ui.messageBox('Smiley face created successfully')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# 3DE4.script.name: Overscan Calculator
# 3DE4.script.version: v1.0

import tde4  # Import 3DEqualizer's scripting module

# Function to calculate overscanned aperture dimensions
def calculate_overscan_aperture(ud_width, ud_height, scan_width, scan_height, aperture_width, aperture_height):
    
    ratio_w = ud_width / scan_width
    ratio_h = ud_height / scan_height
    new_aperture_width = aperture_width * ratio_w
    new_aperture_height = aperture_height * ratio_h

    return new_aperture_width, new_aperture_height

# Get the current active camera from the project
cam_id = tde4.getCurrentCamera()

# Read scan resolution values from the camera
scan_width = tde4.getCameraImageWidth(cam_id)
scan_height = tde4.getCameraImageHeight(cam_id)

req = tde4.createCustomRequester()

# Add input fields for user-defined (UD) plate resolution
tde4.addTextFieldWidget(req, "ud_width", "UD Plate Width (px)", "")
tde4.addTextFieldWidget(req, "ud_height", "UD Plate Height (px)", "")

# Add non-editable fields showing the original scan resolution
tde4.addTextFieldWidget(req, "scan_width", "Scan Plate Width (px)", str(scan_width))
tde4.setWidgetSensitiveFlag(req, "scan_width", 0)  # Disable editing

tde4.addTextFieldWidget(req, "scan_height", "Scan Plate Height (px)", str(scan_height))
tde4.setWidgetSensitiveFlag(req, "scan_height", 0)  # Disable editing

# Add fields for aperture size input in inches
tde4.addTextFieldWidget(req, "aperture_width", "Aperture Width (in)", "")
tde4.addTextFieldWidget(req, "aperture_height", "Aperture Height (in)", "")

# Show the GUI and get return value (1 = "Calculate" clicked, 0 = "Cancel")
ret = tde4.postCustomRequester(req, "Overscan Aperture Calculator (By Aniket Ausarmal)", 600, 0, "Calculate", "Cancel")

# Proceed only if "Calculate" is clicked
if ret == 1:
    try:
        ud_width = float(tde4.getWidgetValue(req, "ud_width"))
        if ud_width < scan_width:
            a = "UD Plate Width Value Is Lower Than Scan Width Value"
            tde4.postQuestionRequester("ERROR", a, "OK")
        
        ud_height = float(tde4.getWidgetValue(req, "ud_height"))
        if ud_height < scan_height:
            a = "UD Plate Height Value Is Lower Than Scan Height Value"
            tde4.postQuestionRequester("ERROR", a, "OK")

        scan_width = int(tde4.getWidgetValue(req, "scan_width"))
        scan_height = int(tde4.getWidgetValue(req, "scan_height"))
        aperture_width = float(tde4.getWidgetValue(req, "aperture_width"))
        aperture_height = float(tde4.getWidgetValue(req, "aperture_height"))

        new_w, new_h = calculate_overscan_aperture(
            ud_width, ud_height, scan_width, scan_height, aperture_width, aperture_height)

        msg = "Overscanned Aperture: \n Width:  {:.4f} in\n Height: {:.4f} in".format(new_w, new_h)
        tde4.postQuestionRequester("Result", msg, "OK")

    except ValueError:
        tde4.postQuestionRequester("ERROR", "Invalid input: Please enter numeric values", "OK")
    
    except:
        tde4.postQuestionRequester("ERROR", "Unexpected error occurred", "OK")

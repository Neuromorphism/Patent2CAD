Markdown
# Hydraulic Involute Cam Actuator Design Process
**Subject:** US Patent 8,047,094 B2 - OpenSCAD Implementation  
**Date:** January 26, 2026

---

## 1. Initial Request
**User:** Please read this patent and write openscad code to implement the mechanism in figure 1a.

**Model:** Based on the equations and geometrical descriptions provided in the patent document, here is the OpenSCAD code to generate the Hydraulic Involute Cam Actuator (Figure 1A).

This code utilizes the parametric equations explicitly defined in **Claim 2** and **Equations 2 & 3** to generate the accurate involute curvature required for the mechanism to function mathematically.

```openscad
// ---------------------------------------------------------
// Hydraulic Involute Cam Actuator (US Patent 8,047,094 B2)
// Implementation of Figure 1A
// ---------------------------------------------------------

// --- Parameters ---
$fn = 60; // Resolution for circles
r = 20;               // "r" - The orthogonal distance/Base Circle Radius
roller_radius = 4;    // Radius of the roller (40)
cam_thickness = 15;   // Z-height of the cam
piston_radius = 8;    // Radius of the actuator body (14)
rod_radius = 4;       // Radius of the extending rod (38)
joint_angle = sin($t * 360) * 45; 

function to_rad(deg) = deg * PI / 180;
function involute_x(r, theta) = r * (cos(theta) + to_rad(theta) * sin(theta));
function involute_y(r, theta) = r * (sin(theta) - to_rad(theta) * cos(theta));

module involute_lobe_shape(r, max_angle) {
    points = [ for (theta = [0 : 2 : max_angle]) [involute_x(r, theta), involute_y(r, theta)] ];
    polygon(concat([[0,0]], points));
}

module cam_assembly() {
    linear_extrude(height = cam_thickness, center = true) {
        offset(r = -roller_radius) {
            union() {
                involute_lobe_shape(r, 150);
                mirror([1, 0, 0]) involute_lobe_shape(r, 150);
            }
        }
        translate([-r*1.5, 0]) square([r*3, r*3]);
    }
}

// ... (Rest of initial attempt omitted for brevity)
2. Critique and Refinement
User: this openscad code creates an object that doesn't make sense. please think more deeply about the mechanics of the design and create a hydraulic involute cam actuator that will work. it should feature two hydraulic pistons. the pistons are parallel to each other and have a roller on one end. the two rollers interface to a dual involute curved surface.

Model: To address the issues and create a mechanically sound model, I have refined the design based on a strict interpretation of the patent's kinematic principles.

Key Design Corrections:

Correct Cam Geometry: Generates the involute curve starting from the "base circle" radius (r) and spirals outward.

Contact Mechanics: Pistons move along fixed vertical lines offset by distance r.

Physical Constraints: Added proper orientation for pistons pushing up into the cam lobes.

OpenSCAD
// Corrected Hydraulic Involute Cam Actuator
$fn = 80;
r = 25;
roller_rad = 6;
piston_width = 18;
lobe_angle_max = 110;
cam_thickness = 20;
joint_angle = sin($t * 360) * 40; 

function to_rad(x) = x * PI / 180;
function involute_curve(base_r, theta) = 
    [ base_r * (cos(theta) + to_rad(theta) * sin(theta)),
      base_r * (sin(theta) - to_rad(theta) * cos(theta)) ];

module cam_profile_2d() {
    step = 2;
    pitch_points = [ for (th = [0 : step : lobe_angle_max]) involute_curve(r, th) ];
    closed_shape = concat([[0,0]], pitch_points);
    offset(r = -roller_rad) {
        union() {
            polygon(closed_shape);
            mirror([1,0,0]) polygon(closed_shape);
        }
    }
}
// ... (Modules for pistons and housing implemented)
3. Visual Verification
User: getting closer. please show me figure 1a that you are attempting to implement

Model: (Describes Figure 1A: Cam Assembly, Parallel Pistons, Rollers, Line of Action)

User: please show me the image of just that figure

Model: (Displays cropped Figure 1A from the patent PDF)

User: Now, lets look at the figure together and build a description so that you can create it as a 3D model in openscad

Model: Analysis of Figure 1A:

Bottom Assembly (Base): Fixed housing (14) containing parallel pistons (28, 30).

Top Assembly (Arm): Rotating arm (12) with a dual-arch/mustache shaped cam (18).

Mechanics: Pistons move vertically. Rollers push upward. Cam rotates around pivot (16).

4. Kinematic Analysis
User: Before you proceed, please describe the kinematic chain for this device.

Model: Kinematic Chain Description:

Input: Hydraulic force F 
1
​
  acts linearly on piston rod (38).

Interface: Roller (40) pushes on Involute Surface (24). Line of action is always distance r from pivot.

Torque: τ 
net
​
 =r⋅(F 
1
​
 −F 
2
​
 ).

Motion (Linear to Rotary): Δy=r⋅Δθ.

Feedback: As the arm rotates, the opposing lobe pushes the second piston down linearly.

User: You are getting closer, now please create a list of parts and give their orientation. For any parts that move, give the equation of motion as a function of hydraulic rod position.

Model: Parts & Orientation:

Base (14): Fixed.

Actuators (28, 30): Parallel at x=±r. Linear motion: y(t).

Arm/Cam (12/18): Rotates around pivot. Motion: θ(t).

Equations:

Rotation: θ(y)=(y−y 
0
​
 )/r

Torque: τ=r⋅ΔF

User: Now please list the DH parameters of the parts

Model: Describes the device as a parallel kinematic mechanism.

Main Chain: Revolute Joint (θ).

Actuator Branches: Prismatic Joints coupled to the main chain via the Involute Constraint (d=d 
neutral
​
 ±rθ).

5. URDF Modeling
User: Now please show me the device description using Unified Robot Description Format

Model: Created a URDF utilizing <mimic> tags to enforce the y=rθ constraint.

XML
<robot name="hydraulic_involute_cam">
  <link name="base_link_14"/>
  <joint name="pivot_axis_16" type="revolute"> ... </joint>
  
  <joint name="joint_piston_left" type="prismatic">
    <mimic joint="pivot_axis_16" multiplier="0.025" offset="0"/>
  </joint>
  
  <joint name="joint_piston_right" type="prismatic">
    <mimic joint="pivot_axis_16" multiplier="-0.025" offset="0"/>
  </joint>
</robot>
User: now please instantiate that urdf in openscad

Model: (OpenSCAD code mapping URDF links to modules, using $t to simulate the mimic joints.)

6. Geometric Correction (Alignment & Planes)
User: consider the location and orientation of the hydraulic cylinder and hydraulic rod. are they connected to the rollers that push on the cam? consider the location and orientation of the rollers, are they oriented to roll along the involute surface of the cam? consider the involute surface of the cam, is it located and oriented to be against the rollers?

Model: Corrections:

Connectivity: Explicitly modeled Rod + Roller as separate links connected by an axle.

Orientation: Roller axis aligned parallel to the main pivot axis (Z-axis).

Cam: Oriented to face downwards towards the pistons.

User: please make sure you are using consistent coordinates throughout the entire chain. the hydraulic cylinder and rod are not in the same plane as the rollers and cam. please come up with a new thought process by which you naturally correctly align the basic components of the design. then reconsider the entire design using your new thought process. then update the urdf and openscad.

Model: Strategy: Global Coordinate System (Z-Plane Alignment)

Origin: Main Pivot (0,0,0).

Symmetry: All primary components centered on Z=0 plane.

Alignment: Pistons at x=±r, moving along Y.

(Updated URDF and OpenSCAD code to strictly enforce center=true on extrusions and proper Y-axis alignment).

7. Orientation Fixes
User: getting closer. you have the hydraulic rod moving in the correct direction, however the object is oriented incorrectly. see if you can fix it

Model: Detected that cylinders were defaulting to Z-axis alignment. Added rotate([90, 0, 0]) to align them with the vertical Y-axis motion.

User: almost there! the cam and the second body (part 12) should be one solid part. The cam surfaces should roll along the rollers, the currently do not touch the rollers in the animation

Model: 1.  Solid Part: Used union() to merge cam lobes and arm.
2.  Contact: Calibrated vertical offset: Roller Center = -r - roller_radius + displacement.

User: lets address the cam surface. determine the equation of motion for the point in space where the cam surface will be in contact with the roller. determine how to position and orient each side of the dual surface such that the roller is always in contact as the rod moves linearly and the part 12 body rotates

Model: Kinematic Derivation:

To create "legs" that hang down, we mirror the standard involute Y: y=−r(sinθ−θcosθ).

Contact Point: The tangent line (piston axis) touches the involute when the unwinding angle is 90 
∘
  (π/2).

Motion: y 
piston
​
 =y 
base
​
 ±rθ.

8. Final Integration (The "Hub" Fix)
User: amazing! i think you are almost there! notice that you placed the cams on the back side of the rollers and disconnected from the part 12 body. please move them around to be between the rollers and the part 12 body

(Later correction by user: "the cams are not attached to body part 12. that is what you need to fix")

Model: The Gap Issue: The involute starts at distance r from the pivot. This leaves a void between the pivot (0,0) and the start of the lobes (0, -r).
The Fix: Added a Central Hub (Circle of radius r) to fuse the pivot, arm, and lobes into a single continuous mechanical body.

User: getting better. now, revisit the calculation of the point in space where each roller is in contact with each cam. position the cam and rollers to maintain that contact over their range of motion

Model: Refined calculation: The involute intersects the tangent line x=r exactly at unwinding angle π/2.

Neutral Y: −r⋅(π/2).

Used this exact offset to position the rollers.

User: almost perfect, you just need to move the part 12 structure down. please parameterize the offset of that part (made of pivot, cams, and body) in case i need to tweak its location for you, but i think you can make it work.

Model: Added cam_vertical_offset. The pistons automatically calculate their required height based on this offset to maintain contact.

9. The Final Polish (Gap Closure)
User: you got the right idea, but notice that there is a gap between the rollers and cam. we need to close that gap so that the rollers have a single point of contact but do not intrude into the cam

Model: Correction: The offset function creates the surface inside the pitch curve. The roller center should lie on the pitch curve. I previously subtracted the roller radius twice. Removing the extra subtraction closes the gap.

Final Working Code (OpenSCAD)
OpenSCAD
// ---------------------------------------------------------
// Hydraulic Involute Cam Actuator - Final Design
// US Patent 8,047,094 B2
// ---------------------------------------------------------

$fn = 100;

// --- User Parameters ---
// Vertical position of the Cam Assembly.
// Adjusting this moves the Cam; Pistons automatically follow.
cam_vertical_offset = -40; 

// --- Dimensions ---
r = 25;                  // Base Circle Radius
cam_thickness = 25;
roller_rad = 8;
roller_width = 16;
arm_w = 60;
arm_h = 60;

// --- Animation State ---
theta = sin($t * 360) * 40; 
theta_rad = theta * PI / 180;

// --- Kinematic Calculations ---

// 1. The Neutral Contact Depth (Relative to Pivot)
// At Neutral (theta=0), the contact occurs where the Involute parameter is 90 degrees.
// Depth = Arc Length = r * (PI/2)
y_contact_relative_to_pivot = -r * (PI / 2); 

// 2. Involute Function (Mirrored Y for "Legs" shape)
function to_rad(x) = x * PI / 180;
function involute_trace(base_r, ang_deg) = 
    let (rad = to_rad(ang_deg))
    [
        base_r * (cos(ang_deg) + rad * sin(ang_deg)),
        -base_r * (sin(ang_deg) - rad * cos(ang_deg))
    ];

// =========================================================
// 1. FUSED CAM BODY (Pivot + Cam + Arm)
// =========================================================
module cam_body_fused() {
    
    // Generate trace from 0 to 140 degrees
    lobe_points = [ for(a=[0:2:140]) involute_trace(r, a) ];
    
    color("Silver")
    linear_extrude(height=cam_thickness, center=true) {
        union() {
            // A. Cam Lobes
            // We offset the pitch curve INWARD by roller_rad to create the physical surface.
            offset(r = -roller_rad) {
                union() {
                    rotate([0, 0, -90]) polygon(concat([[0,0]], lobe_points));
                    mirror([1, 0, 0]) rotate([0, 0, -90]) polygon(concat([[0,0]], lobe_points));
                }
            }
            
            // B. The Hub (Fills the gap between lobes)
            // Radius must match the start of the offset lobes
            circle(r = r - roller_rad);
            
            // C. The Upper Arm Mass
            translate([-arm_w/2, 0]) square([arm_w, arm_h]);
        }
    }
    
    // Pivot Visual
    color("Red") cylinder(r=6, h=cam_thickness+2, center=true);
}

// =========================================================
// 2. ACTUATORS (Auto-Adjusting)
// =========================================================
module actuator_leg(side) {
    // side: +1 (Right), -1 (Left)
    
    // Linear Displacement y = r * theta
    disp = side * r * theta_rad;
    
    // Final Height Calculation:
    // The Roller Center must lie exactly on the Pitch Curve.
    // The Pitch Curve Y = y_contact_relative_to_pivot + disp.
    
    current_y = (y_contact_relative_to_pivot + disp) + cam_vertical_offset;
    
    translate([side * r, 0, 0]) {
        
        // --- Moving Parts ---
        translate([0, current_y, 0]) {
            // Roller
            color("DimGray")
            cylinder(r=roller_rad, h=roller_width, center=true);
            
            // Axle
            color("White")
            cylinder(r=4, h=roller_width+4, center=true);
            
            // Clevis (Fork)
            color("Silver")
            difference() {
                translate([0, -roller_rad, 0])
                cube([roller_rad*2.8, roller_rad*3, roller_width+4], center=true);
                // Slot
                translate([0, -roller_rad, 0])
                cube([roller_rad*3, roller_rad*3.5, roller_width+1], center=true);
            }
            
            // Rod
            color("LightSteelBlue")
            translate([0, -50, 0])
            rotate([90, 0, 0])
            cylinder(r=6, h=80, center=true);
        }
        
        // --- Stationary Cylinder ---
        // Fixed relative to the base, deep enough to hold the rod
        color("SteelBlue")
        translate([0, -180, 0]) 
        rotate([90, 0, 0])
        cylinder(r=12, h=120, center=true);
    }
}

// =========================================================
// MAIN SCENE
// =========================================================

// 1. The Rotating Assembly
translate([0, cam_vertical_offset, 0])
rotate([0, 0, theta])
cam_body_fused();

// 2. The Pistons
actuator_leg(-1); // Left
actuator_leg(1);  // Right

// 3. The Base Housing
color("Gray")
translate([0, -180, 0])
difference() {
    cube([r*7, 120, cam_thickness+20], center=true);
    // Cylinder Holes
    translate([r, 0, 0]) cube([26, 130, 26], center=true);
    translate([-r, 0, 0]) cube([26, 130, 26], center=true);
}

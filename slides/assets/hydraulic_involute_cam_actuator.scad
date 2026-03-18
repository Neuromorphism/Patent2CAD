// Hydraulic Involute Cam Actuator - Final Design
// Based on the final OpenSCAD listing captured in patent2cad.md

$fn = 100;

// Vertical position of the cam assembly.
cam_vertical_offset = -40;

// Dimensions
r = 25;
cam_thickness = 25;
roller_rad = 8;
roller_width = 16;
arm_w = 60;
arm_h = 60;

// Static render state.
theta = 28;
theta_rad = theta * PI / 180;

// At neutral contact, the involute parameter is 90 degrees.
y_contact_relative_to_pivot = -r * (PI / 2);

function to_rad(x) = x * PI / 180;
function involute_trace(base_r, ang_deg) =
    let (rad = to_rad(ang_deg))
    [
        base_r * (cos(ang_deg) + rad * sin(ang_deg)),
        -base_r * (sin(ang_deg) - rad * cos(ang_deg))
    ];

module cam_body_fused() {
    lobe_points = [ for (a = [0 : 2 : 140]) involute_trace(r, a) ];

    color("Silver")
    linear_extrude(height = cam_thickness, center = true) {
        union() {
            // Create the physical cam by offsetting the pitch curve inward.
            offset(r = -roller_rad) {
                union() {
                    rotate([0, 0, -90]) polygon(concat([[0, 0]], lobe_points));
                    mirror([1, 0, 0]) rotate([0, 0, -90]) polygon(concat([[0, 0]], lobe_points));
                }
            }

            circle(r = r - roller_rad);
            translate([-arm_w / 2, 0]) square([arm_w, arm_h]);
        }
    }

    color("Red") cylinder(r = 6, h = cam_thickness + 2, center = true);
}

module actuator_leg(side) {
    disp = side * r * theta_rad;
    current_y = (y_contact_relative_to_pivot + disp) + cam_vertical_offset;

    translate([side * r, 0, 0]) {
        translate([0, current_y, 0]) {
            color("DimGray")
            cylinder(r = roller_rad, h = roller_width, center = true);

            color("White")
            cylinder(r = 4, h = roller_width + 4, center = true);

            color("Silver")
            difference() {
                translate([0, -roller_rad, 0])
                cube([roller_rad * 2.8, roller_rad * 3, roller_width + 4], center = true);

                translate([0, -roller_rad, 0])
                cube([roller_rad * 3, roller_rad * 3.5, roller_width + 1], center = true);
            }

            color("LightSteelBlue")
            translate([0, -50, 0])
            rotate([90, 0, 0])
            cylinder(r = 6, h = 80, center = true);
        }

        color("SteelBlue")
        translate([0, -180, 0])
        rotate([90, 0, 0])
        cylinder(r = 12, h = 120, center = true);
    }
}

translate([0, cam_vertical_offset, 0])
rotate([0, 0, theta])
cam_body_fused();

actuator_leg(-1);
actuator_leg(1);

color("Gray")
translate([0, -180, 0])
difference() {
    cube([r * 7, 120, cam_thickness + 20], center = true);
    translate([r, 0, 0]) cube([26, 130, 26], center = true);
    translate([-r, 0, 0]) cube([26, 130, 26], center = true);
}

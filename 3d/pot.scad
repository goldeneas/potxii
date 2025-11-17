pot_width = 20;
pot_depth = 20;
pot_height = 20;

tank_width = 10;
tank_depth = 10;
tank_height = 10;

module pot(position, dimensions) {
    diff_position = [for (i = position) i + 1];
        
    diff_dimensions = [
        for (i = [0 : 2])
            if(i == 2) dimensions[i]
            else dimensions[i] - 2
    ];
    
    difference () {
        translate(position) {
            cube(dimensions);
        }
        
        translate(diff_position) {
            cube(diff_dimensions);
        }
    }
}

module tank(position, dimensions) {
    translate([20, 10, 0]) {
        difference () {
            cylinder(10, 10, 10);
            translate([-10, 0, 9]) {
                cube(20, center = true);
            };
            translate ([0, 0, 1]) {
                cylinder(11, 9, 9);
            }
        }
    } 
}

module esp_container() {
    pot([0, pot_depth - 8, 0], [20, 8, 20]);
}

module holes() {
    translate([19.5, 15, 16]) {
        rotate([0, 90, 0]) {
            sphere(1);
        }
    }
    
    translate([19.5, 5, 10]) {
        rotate([0, 90, 0]) {
            sphere(1);
        }   
    }
	
	translate([8.5, 18.5, 15]) {
		cube([2.174, 1.806, 2]);
	}
}

module lid() {
    union() {
        color ("red", 1.0) {
            translate ([0, 12, 30]) {
                cube([20, 8, 1]);
            }
        }
    
        color ("blue", 1.0) {
            translate ([1, 13, 29.5]) {
                cube([18, 6, 1]);
            }
        }
    }
}

module esp_plane() {
    translate([0, 12, 10]) {
		cube([20, 7, 1]);
    }
}

union () {
    difference() {
        tank([pot_width - 0.9, 5, 0], [tank_width, tank_depth, tank_height]);
        holes();
    }
    
    difference() {
        esp_container();
        holes();
    }
    
    difference() {
        pot([0, 0, 0], [pot_width, pot_depth, pot_height]);
        holes();
    }
	
	difference() {
        esp_plane();
        holes();
    }
}

lid();

 
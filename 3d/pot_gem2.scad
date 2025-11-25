// ==============================================================================
// PROGETTO: All-in-One Smart Vase (ESP32 IoT)
// VERSIONE: 1.2.0 (Raised Electronics Floor)
// ==============================================================================

// --- PARAMETRI GENERALI ---
$fn = 60;
wall_thick = 3.0; 
tolerance = 0.5; 

// --- DIMENSIONI VASO ---
vase_width = 200;
vase_depth = 200;
vase_height = 180;
corner_radius = 10;

// --- DIMENSIONI ELETTRONICA / COMPARTI ANTERIORI ---
oled_width = 27;  
oled_height = 27; 
oled_screen_w = 23; 
oled_screen_h = 12; 
esp32_bay_depth = 40; 

// --- CONFIGURAZIONE NUOVA: PAVIMENTO ELETTRONICA ---
// Alziamo il fondo del vano elettronica a 80mm da terra
// Questo riduce la distanza dai sensori e dal display
electronics_floor_z = 80; 

inner_corner_radius = 6;

// --- CONFIGURAZIONE RENDERING ---
show_main_body = 1;
show_drainage_tray = 1;
show_lid = 0; 

// ==============================================================================
// LOGICA DI COSTRUZIONE
// ==============================================================================

module lid_generic(w, d) {
    lid_h = 2;
    // Raggio leggermente ridotto per tolleranza
    lid_r = max(1, inner_corner_radius - tolerance); 
    
    union() {
        rounded_cube([w, d, lid_h], lid_r);
        // Maniglietta
        translate([w/2, d/2, lid_h])
            cylinder(h=5, r1=4, r2=6);
    }
}

module rounded_cube(size, r) {
    hull() {
        translate([r, r, 0]) cylinder(h=size[2], r=r);
        translate([size[0]-r, r, 0]) cylinder(h=size[2], r=r);
        translate([size[0]-r, size[1]-r, 0]) cylinder(h=size[2], r=r);
        translate([r, size[1]-r, 0]) cylinder(h=size[2], r=r);
    }
}

module smart_vase_final() {
    
    water_tank_width = (vase_width / 2) - wall_thick;
    electronics_width = (vase_width / 2) - wall_thick;
    
    front_compartment_depth = esp32_bay_depth; 
    
    soil_depth = vase_depth - front_compartment_depth - (wall_thick * 3);
    tray_height = 20;
    floor_z = tray_height + wall_thick + 2; // Pavimento standard (Acqua/Suolo)

    difference() {
        // --- POSITIVO: Guscio Esterno ---
        rounded_cube([vase_width, vase_depth, vase_height], corner_radius);

        // --- NEGATIVO: Comparto SUOLO (A) ---
        translate([wall_thick, front_compartment_depth + wall_thick*2, floor_z])
            rounded_cube([
                vase_width - wall_thick*2, 
                soil_depth, 
                vase_height 
            ], 5);

        // --- NEGATIVO: Comparto ACQUA (B) ---
        translate([wall_thick, wall_thick, floor_z])
            rounded_cube([
                water_tank_width - wall_thick, 
                front_compartment_depth, 
                vase_height
            ], inner_corner_radius);

        // --- NEGATIVO: Comparto ELETTRONICA (C) ---
        // FIX: Ora inizia molto più in alto (electronics_floor_z)
        translate([water_tank_width + wall_thick*2, wall_thick, electronics_floor_z])
            rounded_cube([
                electronics_width - wall_thick, 
                front_compartment_depth, 
                vase_height // Taglia fino in cima
            ], inner_corner_radius);

        // --- NEGATIVO: Vano Vassoio Drenaggio (D) ---
        translate([wall_thick, front_compartment_depth + wall_thick*2, wall_thick])
            rounded_cube([
                vase_width - wall_thick*2, 
                soil_depth + 10, 
                tray_height
            ], inner_corner_radius);
            
        // --- DETTAGLI FUNZIONALI ---
        
        // 1. Fori di drenaggio
        for(x = [20 : 20 : vase_width-20]) {
            for(y = [front_compartment_depth + 30 : 20 : vase_depth-20]) {
                translate([x, y, floor_z - 5])
                    cylinder(h=10, r=2.5); 
            }
        }

        // 2. Finestra OLED
        translate([water_tank_width + wall_thick*2 + (electronics_width/2), -1, vase_height - 40]) {
            cube([oled_screen_w, 10, oled_screen_h], center=true);
            translate([0, 3, 0])
                cube([oled_width, 5, oled_height], center=true);
        }
        
        // 3. Passaggi Cavi (Cavidotti interni)
        // Elettronica -> Suolo (per sensori)
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) - 15, front_compartment_depth - 5, vase_height - 25])
            rotate([-90, 0, 0]) 
            cylinder(h=25, r=4); 

        // Elettronica -> Acqua
        // FIX: Alzato per allinearsi col nuovo pavimento elettronica
        translate([water_tank_width + wall_thick/2 + 1, front_compartment_depth/2, electronics_floor_z + 50])
            rotate([0, 90, 0])
            cylinder(h=10, r=3, center=true);
            
        // 4. Foro USB 
        // FIX: Alzato per entrare nel nuovo vano (altrimenti bucherebbe il pieno)
        translate([vase_width - 10, front_compartment_depth/2, electronics_floor_z + 15])
            rotate([0, 90, 0])
            cylinder(h=20, r=5); 
            
        // 5. Foro Tubo Acqua (Elettronica -> Suolo)
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) + 15, front_compartment_depth - 5, vase_height - 25])
            rotate([-90, 0, 0])
            cylinder(h=25, r=5); 
    }
}

module drainage_tray() {
    front_compartment_depth = esp32_bay_depth; 
    
    tray_w = vase_width - wall_thick*2 - tolerance;
    soil_depth_actual = vase_depth - front_compartment_depth - (wall_thick * 2); 
    tray_d = soil_depth_actual - 5; 
    tray_h = 20 - tolerance; 

    difference() {
        cube([tray_w, tray_d, tray_h]);
        translate([wall_thick, wall_thick, wall_thick])
            cube([tray_w - wall_thick*2, tray_d - wall_thick*2, tray_h + 10]);
    }
    
    translate([tray_w/2, 0, tray_h/2]) {
        difference() {
            union() {
                translate([0, -2, 0]) cube([30, 4, tray_h], center=true);
                rotate([90,0,0]) cylinder(h=2, r=8);
            }
            rotate([90,0,0]) cylinder(h=10, r=4, center=true);
        }
    }
}

module electronics_lid() {
    water_tank_width = (vase_width / 2) - wall_thick;
    electronics_width = (vase_width / 2) - wall_thick;
    front_compartment_depth = esp32_bay_depth; 
    
    cube([electronics_width - wall_thick - tolerance, front_compartment_depth - tolerance, 2]);
}

// ultrasound sensor
module us_support() {
    width = 45;
    depth = 40;
    height = 5;
    
    holes_radius = 10;
	
	union() {
		translate ([100, 0.5, 110]) {
			// vertical holder
			translate([-depth, 0, 0]) {
				rotate([0, 0, 90]) {
					cube([width, height- 3, depth - 30]);
				}
			}
		
			difference() {
				// main body
				rotate([0, 0, 90]) {
					cube([width, depth, height]);
				}
			
				// eye holes
				translate ([-20, 0, 0]) {
					translate ([0, 13, 0]) {
						sphere(holes_radius);
					}
            
					translate ([0, 33, 0]) {
						sphere(holes_radius);
					}
				}
			}
		}
	}
}

// ==============================================================================
// GENERAZIONE SCENA
// ==============================================================================

if (show_main_body) {
    color("Teal", 0.8) 
	union() {
		smart_vase_final();
		us_support();
	}
}

if (show_drainage_tray) {
    front_compartment_depth = esp32_bay_depth; 
    color("Silver")
    translate([wall_thick + tolerance/2, front_compartment_depth + wall_thick*2 + 2, wall_thick])
        drainage_tray();
}

if (show_lid) {
    water_tank_width = (vase_width / 2) - wall_thick;
    electronics_width = (vase_width / 2) - wall_thick;
    
    // Dimensioni coperchi (spazio interno - tolleranza)
    lid_w_water = water_tank_width - wall_thick - tolerance;
    lid_w_elec = electronics_width - wall_thick - tolerance;
    lid_d = esp32_bay_depth - tolerance;
    
    color("DarkSlateGray") {
        // Coperchio ACQUA
        translate([wall_thick + tolerance/2, wall_thick + tolerance/2, vase_height])
            lid_generic(lid_w_water, lid_d);
            
        // Coperchio ELETTRONICA
        translate([water_tank_width + wall_thick*2 + tolerance/2, wall_thick + tolerance/2, vase_height])
            lid_generic(lid_w_elec, lid_d);
    }
}
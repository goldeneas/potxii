// ==============================================================================
// PROGETTO: All-in-One Smart Vase (ESP32 IoT)
// VERSIONE: 1.4.0 (Water Level Sensor Correction)
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
oled_width = 24;  
oled_height = 16; 
oled_screen_w = oled_width; 
oled_screen_h = oled_height; 

esp32_bay_depth = 100; 

// --- CONFIGURAZIONE NUOVA: PAVIMENTO ELETTRONICA ---
electronics_floor_z = 80; 

inner_corner_radius = 6;

// --- CONFIGURAZIONE RENDERING ---
show_main_body = 1;
show_drainage_tray = 1;
show_lid = 0; 
show_sensor = 1; 

// ==============================================================================
// LOGICA DI COSTRUZIONE
// ==============================================================================

module lid_generic(w, d) {
    lid_h = 2;
    lid_r = max(1, inner_corner_radius - tolerance); 
    
    union() {
        rounded_cube([w, d, lid_h], lid_r);
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
    floor_z = tray_height + wall_thick + 2; 

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
        translate([water_tank_width + wall_thick*2, wall_thick, electronics_floor_z])
            rounded_cube([
                electronics_width - wall_thick, 
                front_compartment_depth, 
                vase_height 
            ], inner_corner_radius);

        // --- NEGATIVO: Vano Vassoio Drenaggio (D) ---
        translate([wall_thick, front_compartment_depth + wall_thick*2, wall_thick])
            rounded_cube([
                vase_width - wall_thick*2, 
                soil_depth + 20, 
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
        
        // 3. Passaggi Cavi
        // Elettronica -> Suolo
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) - 15, front_compartment_depth - 5, vase_height - 25])
            rotate([-90, 0, 0]) 
            cylinder(h=25, r=10); 

        // Elettronica -> Acqua (Sensore Livello / Pompa)
        // Questo foro collega la parte alta del serbatoio con la parte alta dell'elettronica
        translate([water_tank_width + wall_thick*1.5, front_compartment_depth/2, vase_height - 20])
            rotate([0, 90, 0])
            cylinder(h=wall_thick*4, r=10, center=true);
            
        // 4. Foro USB 
        translate([vase_width - 10, front_compartment_depth/2, electronics_floor_z + 15])
            rotate([0, 90, 0])
            cylinder(h=20, r=10); 
            
        // 5. Foro Tubo Acqua
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) + 15, front_compartment_depth - 5, vase_height - 25])
            rotate([-90, 0, 0])
            cylinder(h=25, r=10);
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

module us_support() {
    // Dimensioni standard HC-SR04 approssimative
    us_pcb_w = 45; 
    us_pcb_h = 20;
    
    holder_w = esp32_bay_depth;
    holder_d = 10; 
    holder_h = 40; // Leggermente più compatto
    
    holes_radius = 8.2;
	
	rotate([90, 0, 90]) {
		translate([-37.5, 30, -17]) {
			translate([0, -10, holder_h - 5]) {
				cube([esp32_bay_depth, 10, 5]);
			}

			difference() {
				// Corpo principale
				cube([holder_w, holder_d, holder_h]);
				
				// Scasso PCB
				translate([(holder_w - us_pcb_w)/2, 2, (holder_h - us_pcb_h)/2 + 2])
					cube([us_pcb_w, holder_d, us_pcb_h]);
					
				// Fori occhi (passanti)
				translate([holder_w/2, -1, (holder_h/2)]) {
					translate([-13, 0, 0]) rotate([-90,0,0]) cylinder(h=holder_d+2, r=holes_radius);
					translate([13, 0, 0]) rotate([-90,0,0]) cylinder(h=holder_d+2, r=holes_radius);
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
    smart_vase_final();
}

if (show_sensor) {
    // LOGICA DI POSIZIONAMENTO CORRETTA PER LIVELLO ACQUA
    // Deve stare sopra il comparto ACQUA, puntando GIÙ (-Z)
    
    water_tank_w = (vase_width / 2) - wall_thick;
    
    // Posizione X: Centrato nel comparto acqua
    sens_x = wall_thick + (water_tank_w/2) - (55/2); // 55 è width del supporto
    
    // Posizione Y: Centrato in profondità
    sens_y = wall_thick + (esp32_bay_depth/2) - (25/2); // 25 è (ora) height del supporto che diventa profondità ruotato
    
    // Posizione Z: In cima al vaso, appena sotto il bordo
    sens_z = vase_height;

    color("Gold")
    translate([sens_x + 55, sens_y, sens_z - 20]) // Aggiustamenti fini per rotazione
        rotate([0, 180, 0]) // Capovolto a testa in giù (cavi in alto, occhi in basso)
        us_support();
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
    lid_w_water = water_tank_width - wall_thick - tolerance;
    lid_w_elec = electronics_width - wall_thick - tolerance;
    lid_d = esp32_bay_depth - tolerance;
    
    color("DarkSlateGray") {
        translate([wall_thick + tolerance/2, wall_thick + tolerance/2, vase_height])
            lid_generic(lid_w_water, lid_d);
            
        translate([water_tank_width + wall_thick*2 + tolerance/2, wall_thick + tolerance/2, vase_height])
            lid_generic(lid_w_elec, lid_d);
    }
}
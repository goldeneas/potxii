// ==============================================================================
// PROGETTO: All-in-One Smart Vase (ESP32 IoT)
// VERSIONE: 1.1.0
// MATERIALE CONSIGLIATO: PETG o ASA (Impermeabile, resistente UV)
// NOTE DI STAMPA: 
// - Pareti: Almeno 3 perimetri per impermeabilità.
// - Infill: 20% Gyroid.
// - Supporti: Minimi necessari solo per la finestra OLED o i passaggi cavi.
// ==============================================================================

// --- PARAMETRI GENERALI ---
$fn = 60; // Risoluzione curve (aumentare per export finale)
wall_thick = 3.0; // Spessore pareti (robusto per tenuta stagna)
tolerance = 0.5;  // Tolleranza aumentata per scorrimento vassoio

// --- DIMENSIONI VASO ---
vase_width = 200;
vase_depth = 200;
vase_height = 180;
corner_radius = 10;

// --- DIMENSIONI ELETTRONICA ---
oled_width = 27;  // Larghezza modulo OLED 0.96
oled_height = 27; // Altezza modulo OLED (approssimativa del PCB)
oled_screen_w = 23; // Larghezza solo schermo
oled_screen_h = 12; // Altezza solo schermo
esp32_bay_depth = 30; // Profondità vano elettronica

// --- CONFIGURAZIONE RENDERING ---
// Imposta a 1 per vedere il vaso, 0 per nasconderlo
show_main_body = 1;
// Imposta a 1 per vedere il vassoio di drenaggio, 0 per nasconderlo
show_drainage_tray = 1;
// Imposta a 1 per vedere il coperchio elettronica (da stampare piatto), 0 nascondi
show_lid = 0; 


// ==============================================================================
// LOGICA DI COSTRUZIONE
// ==============================================================================

module rounded_cube(size, r) {
    hull() {
        translate([r, r, 0]) cylinder(h=size[2], r=r);
        translate([size[0]-r, r, 0]) cylinder(h=size[2], r=r);
        translate([size[0]-r, size[1]-r, 0]) cylinder(h=size[2], r=r);
        translate([r, size[1]-r, 0]) cylinder(h=size[2], r=r);
    }
}

module main_body() {
    // Modulo placeholder, la logica vera è in smart_vase_final
}

// Ricostruzione con layout a blocchi per massima chiarezza
module smart_vase_final() {
    
    water_tank_width = (vase_width / 2) - wall_thick;
    electronics_width = (vase_width / 2) - wall_thick;
    front_compartment_depth = 40; 
    soil_depth = vase_depth - front_compartment_depth - (wall_thick * 3);
    tray_height = 20;
    floor_z = tray_height + wall_thick + 2; // Altezza pavimento comparti superiori

    difference() {
        // --- POSITIVO: Guscio Esterno ---
        rounded_cube([vase_width, vase_depth, vase_height], corner_radius);

        // --- NEGATIVO: Comparto SUOLO (A) ---
        // Occupa la parte posteriore
        translate([wall_thick, front_compartment_depth + wall_thick*2, floor_z])
            rounded_cube([
                vase_width - wall_thick*2, 
                soil_depth, 
                vase_height // Va fino in cima
            ], 5);

        // --- NEGATIVO: Comparto ACQUA (B) ---
        // Anteriore Sinistro
        translate([wall_thick, wall_thick, floor_z])
            cube([
                water_tank_width - wall_thick, 
                front_compartment_depth, 
                vase_height
            ]);

        // --- NEGATIVO: Comparto ELETTRONICA (C) ---
        // Anteriore Destro
        translate([water_tank_width + wall_thick*2, wall_thick, floor_z])
            cube([
                electronics_width - wall_thick, 
                front_compartment_depth, 
                vase_height
            ]);

        // --- NEGATIVO: Vano Vassoio Drenaggio (D) ---
        // Scavo passante sul fondo (solo posteriore sotto il suolo)
        translate([wall_thick, front_compartment_depth + wall_thick*2, wall_thick])
            cube([
                vase_width - wall_thick*2, 
                soil_depth + 10, // Un po' più lungo per estrazione
                tray_height
            ]);
            
        // --- DETTAGLI FUNZIONALI ---
        
        // 1. Fori di drenaggio (Suolo -> Vassoio)
        for(x = [20 : 20 : vase_width-20]) {
            for(y = [front_compartment_depth + 30 : 20 : vase_depth-20]) {
                translate([x, y, floor_z - 5])
                    cylinder(h=10, r=2.5); // Fori aumentati a 5mm per evitare intasamenti
            }
        }

        // 2. Finestra OLED (Nel comparto Elettronica)
        translate([water_tank_width + wall_thick*2 + (electronics_width/2), -1, vase_height - 40]) {
            // Foro schermo passante
            cube([oled_screen_w, 10, oled_screen_h], center=true);
            // Scasso interno per il PCB (non passante)
            translate([0, 3, 0])
                cube([oled_width, 5, oled_height], center=true);
        }
        
        // 3. Passaggi Cavi (Cavidotti interni)
        // Elettronica -> Suolo (per sensori)
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) - 15, front_compartment_depth - 5, vase_height - 25])
            rotate([-90, 0, 0])
            cylinder(h=20, r=4); // Foro 8mm

        // Elettronica -> Acqua (per pompa o cavi)
        // Foro nel muro divisorio centrale
        translate([water_tank_width + wall_thick/2 + 1, front_compartment_depth/2, 40])
            rotate([0, 90, 0])
            cylinder(h=10, r=3, center=true);
            
        // 4. Foro USB (lato elettronica o fondo)
        translate([vase_width - 10, front_compartment_depth/2, floor_z + 10])
            rotate([0, 90, 0])
            cylinder(h=20, r=5); // Accesso cavo alimentazione 
            
        // 5. NUOVO: Foro Tubo Acqua (Elettronica -> Suolo)
        // Richiesto dall'utente. Attenzione: sigillare bene se si usa pompa interna.
        translate([water_tank_width + wall_thick*2 + (electronics_width/2) + 15, front_compartment_depth - 5, vase_height - 25])
            rotate([90, 0, 0])
            cylinder(h=20, r=5); // Foro 10mm per tubo standard silicone 6-8mm
    }
}

module drainage_tray() {
    front_compartment_depth = 40; 
    tray_w = vase_width - wall_thick*2 - tolerance;
    // Calcoliamo la profondità esatta dello scavo meno la tolleranza
    soil_depth_actual = vase_depth - front_compartment_depth - (wall_thick * 2); 
    tray_d = soil_depth_actual - 5; // Leggermente più corto dello scasso per non sporgere troppo
    tray_h = 20 - tolerance; // Altezza scavo meno tolleranza

    difference() {
        // Corpo vassoio
        cube([tray_w, tray_d, tray_h]);
        // Scavo interno vassoio (contenitore acqua)
        translate([wall_thick, wall_thick, wall_thick])
            cube([tray_w - wall_thick*2, tray_d - wall_thick*2, tray_h + 10]);
    }
    
    // Maniglia estrazione migliorata
    translate([tray_w/2, 0, tray_h/2]) {
        difference() {
            union() {
                translate([0, -2, 0]) cube([30, 4, tray_h], center=true);
                rotate([90,0,0]) cylinder(h=2, r=8);
            }
            // Foro per dito per tirare meglio
            rotate([90,0,0]) cylinder(h=10, r=4, center=true);
        }
    }
}

module electronics_lid() {
    water_tank_width = (vase_width / 2) - wall_thick;
    electronics_width = (vase_width / 2) - wall_thick;
    front_compartment_depth = 40; 
    
    cube([electronics_width - wall_thick - tolerance, front_compartment_depth - tolerance, 2]);
}

// ==============================================================================
// GENERAZIONE SCENA
// ==============================================================================

if (show_main_body) {
    color("Teal", 0.8) 
    smart_vase_final();
}

if (show_drainage_tray) {
    front_compartment_depth = 40; 
    // Posizioniamo il vassoio nel suo alloggiamento
    color("Silver")
    translate([wall_thick + tolerance/2, front_compartment_depth + wall_thick*2 + 2, wall_thick])
        drainage_tray();
}

if (show_lid) {
    water_tank_width = (vase_width / 2) - wall_thick;
    color("DarkSlateGray")
    translate([water_tank_width + wall_thick*2 + tolerance/2, wall_thick + tolerance/2, vase_height])
        electronics_lid();
}
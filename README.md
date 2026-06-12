# ME433 HW15 - Haptic Paddle, mechanical first draft
Shreeniket Bendre

Five printable parts, generated parametrically from `haptic_paddle.py`
(CadQuery). STLs are ready to slice; STEP files import into Onshape,
Fusion, or SolidWorks if you want to edit visually.

## Parts
| File | What it is | Hardware it touches |
|---|---|---|
| paddle_arm | Lever arm, horn interface at one end, load cell clamp at the other | servo horn + 2 wood screws, 2x 4-40 screws + nuts |
| magnet_cap | Press-fits into the arm boss bore, covers the horn machine screw, holds the AS5600 magnet on the rotation axis | 6 x 2.5 mm diametric magnet (glue) |
| thimble_clamp | Clamps the free end of the load cell, finger ring | 1x 8-32 screw + nut |
| base_plate | Servo drops into the cutout, flange bolts down with the rubber dampers | 4x 8-32 |
| as5600_bracket | Column + cantilever holding the AS5600 board chip-down over the magnet | 2x M3 to plate, 2x M3 into standoffs |

## MEASURE BEFORE PRINTING (calipers, 5 minutes, saves 3 reprints)
Every one of these is a named parameter at the top of haptic_paddle.py:
1. Load cell: width, height, hole positions from the end, and hole size.
   Defaults assume a TAL221-style 45 x 10 x 6 mm mini cell.
2. Servo: body cutout length/width, flange hole spacing (dx, dy),
   and shaft offset from body center. Defaults are standard-size class.
3. Horn: diameter, thickness, wood-screw hole radius. Round horn assumed.
4. Magnet: diameter and thickness. Pocket has +0.25 mm glue clearance.
5. AS5600 board: mounting hole spacing (pcb_hole_dx). Defaults to 18 mm.
6. magnet_top_z: you can only measure this after the servo, horn, arm,
   and cap are assembled on the plate. Print the bracket LAST, after
   measuring, so the chip-to-magnet air gap lands at 1 to 2 mm.

## Print settings
PLA, 0.2 mm layers, 3 perimeters, 40 percent infill, no supports needed.
Orientations: arm and thimble flat with hex pockets facing UP. Cap with
magnet pocket UP (it bridges the screw bore internally, that is fine).
Plate flat. Bracket lying on its SIDE with a brim, not standing.

## Assembly order and the professor's gotchas
1. Servo into plate with dampers and 8-32s. Horn on spline, machine screw.
2. Arm onto horn: the horn nests in the recess under the boss. The wood
   screws WILL be too long (prof's lesson). Run them in from the top and
   check the tips do not protrude past the horn; add washers under the
   heads or trim the screws. Mind the pinch point while the servo moves.
3. Press the magnet_cap into the boss bore (9.4 into 9.5: FDM holes print
   slightly undersized, so this should be a firm press fit; sand the cap
   OD lightly if too tight). Glue the magnet in its pocket.
4. Load cell under the arm pad, 2x 4-40 up through the cell into the hex
   nut pockets on top. Thimble on the other end with the 8-32 the same way.
   Keep the load direction tangential to the single-screw clamp.
5. Measure magnet_top_z, set it in the script, regenerate, print bracket,
   bolt it down, mount the AS5600 chip-side DOWN on the standoffs.

## Known first-draft weaknesses (expect to iterate, like the prof says)
- The bracket cantilever is unsupported plastic about 50 mm long; if the
  sensor reading is noisy from vibration, add a rib or a second column.
- The thimble ring is a closed circle, ID 19 mm. Measure your finger.
- Backlash: the servo gear train has about a degree of slop (prof's
  lesson 6); the AS5600 reads the OUTPUT side of that, which is the
  point of mounting the encoder on the horn axis instead of trusting
  the servo's internal pot.

## Regenerating
pip install cadquery
python3 haptic_paddle.py
STLs land in stl/, STEPs in step/.

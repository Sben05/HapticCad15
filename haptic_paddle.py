"""
ME433 HW15 - Haptic Paddle mechanical parts (first draft)
Shreeniket Bendre

Parametric model in CadQuery. Edit the parameters, rerun, reprint.
ALL dimensions marked MEASURE must be verified with calipers on YOUR
hardware before printing. Defaults assume:
  - standard-size hobby servo (Futaba S3003 / MG996R class)
  - TAL221-style mini bar load cell (45 x 10 x 6 mm)
  - GY-AS5600 breakout (~22 x 22 mm) with 6 x 2.5 mm diametric magnet
Units: mm
"""
import cadquery as cq
import os

# ----------------- screws and nuts -----------------
d_440_clr   = 3.0    # 4-40 clearance hole
af_440_nut  = 6.6    # 4-40 nut pocket across flats (nut is 6.35)
t_440_nut   = 2.7
d_832_clr   = 4.5    # 8-32 clearance hole
af_832_nut  = 9.0    # 8-32 nut pocket across flats (nut is 8.73)
t_832_nut   = 3.6
d_wood_clr  = 2.4    # MEASURE: servo horn wood screws
d_m3_clr    = 3.4
d_m3_tap    = 2.7    # M3 self-tap into plastic

# ----------------- load cell (MEASURE) -----------------
lc_w        = 10.0   # MEASURE width
lc_h        = 6.0    # MEASURE height
lc_hole_a   = 4.5    # MEASURE: 1st hole center from cell end
lc_hole_b   = 10.5   # MEASURE: 2nd hole center from cell end

# ----------------- servo + horn (MEASURE) -----------------
servo_body_l   = 41.2   # MEASURE: cutout length (body + 0.6 clearance)
servo_body_w   = 20.8   # MEASURE: cutout width
servo_hole_dx  = 49.5   # MEASURE: flange hole spacing, long axis
servo_hole_dy  = 10.0   # MEASURE: flange hole spacing, short axis
servo_shaft_off= 9.8    # MEASURE: shaft center to body center, long axis
horn_d         = 21.4   # MEASURE: round horn diameter + 0.4
horn_t         = 2.2    # MEASURE: horn thickness
horn_screw_r   = 7.5    # MEASURE: radius of horn wood-screw holes
magnet_d       = 6.25   # MEASURE: magnet diameter + 0.25 (glue gap)
magnet_t       = 2.5    # MEASURE
horn_screwhead_d = 6.3  # MEASURE: horn center machine screw head + clr

# ----------------- AS5600 board (MEASURE) -----------------
pcb_w       = 22.0
pcb_hole_dx = 18.0   # MEASURE: distance between the 2 mounting holes
pcb_t       = 1.7
air_gap     = 1.5    # magnet face to chip face (AS5600 wants 0.5-3)
magnet_top_z= 45.0   # MEASURE AFTER ASSEMBLY: magnet top above base plate

# ----------------- arm -----------------
arm_len     = 70.0   # shaft axis to start of load cell pad
arm_w       = 14.0
arm_t       = 6.0
boss_d      = 26.0
boss_h      = 8.0
pad_l       = 18.0
pad_w       = lc_w + 8.0

out = {}

# ============================================================
# PART 1: paddle arm
# horn recess on BOTTOM of boss; nut pockets on TOP of pad.
# Print top-side up: every pocket faces up, no supports.
# ============================================================
arm = (cq.Workplane("XY")
       .box(arm_len + pad_l, arm_w, arm_t,
            centered=(False, True, False)))
arm = arm.union(
    cq.Workplane("XY").cylinder(boss_h, boss_d/2,
        centered=(True, True, False)))
# pad block at far end
arm = arm.union(
    cq.Workplane("XY").transformed(offset=(arm_len, 0, 0))
      .box(pad_l, pad_w, arm_t, centered=(False, True, False)))
# horn recess from bottom + center hole + wood screw holes
arm = (arm.faces("<Z").workplane(origin=(0,0,0))
       .hole(horn_d, horn_t))
# 9.5 dia center bore: clears horn machine screw head, magnet cap press-fits here
arm = arm.cut(cq.Workplane("XY").cylinder(boss_h, 4.75,
        centered=(True, True, False)))
for sy in (+1, -1):
    arm = arm.cut(cq.Workplane("XY")
                  .transformed(offset=(0, sy*horn_screw_r, 0))
                  .cylinder(boss_h, d_wood_clr/2, centered=(True, True, False)))
# load cell holes + hex nut pockets (pockets on top)
for hx in (arm_len + pad_l - lc_hole_a, arm_len + pad_l - lc_hole_b):
    arm = arm.cut(cq.Workplane("XY")
                  .transformed(offset=(hx, 0, 0))
                  .cylinder(arm_t, d_440_clr/2, centered=(True, True, False)))
    arm = arm.cut(cq.Workplane("XY")
                  .workplane(offset=arm_t - t_440_nut)
                  .transformed(offset=(hx, 0, 0))
                  .polygon(6, af_440_nut/0.866025).extrude(t_440_nut))
# shallow registration channel for the cell on the bottom of the pad
arm = arm.cut(cq.Workplane("XY")
              .transformed(offset=(arm_len + 2, 0, 0))
              .box(pad_l - 2 + 0.01, lc_w + 0.5, 1.0,
                   centered=(False, True, False)))
out["paddle_arm"] = arm

# ============================================================
# PART 2: magnet cap (press-fits into arm boss center bore,
# covers the horn machine screw head, holds magnet on axis)
# ============================================================
cap = (cq.Workplane("XY").cylinder(8.0, 9.4/2, centered=(True, True, False)))
cap = cap.cut(cq.Workplane("XY")
              .cylinder(2.9, horn_screwhead_d/2, centered=(True, True, False)))
cap = cap.cut(cq.Workplane("XY").workplane(offset=8.0 - (magnet_t + 0.3))
              .circle(magnet_d/2).extrude(magnet_t + 0.3))
out["magnet_cap"] = cap

# ============================================================
# PART 3: thimble clamp (one 8-32 + nut, finger ring)
# ============================================================
th_pad_l = 16.0
thim = (cq.Workplane("XY")
        .box(th_pad_l, pad_w, 5.0, centered=(False, True, False)))
hx = th_pad_l - 6.0
thim = thim.cut(cq.Workplane("XY").transformed(offset=(hx, 0, 0))
                .cylinder(5.0, d_832_clr/2, centered=(True, True, False)))
thim = thim.cut(cq.Workplane("XY").workplane(offset=5.0 - t_832_nut)
                .transformed(offset=(hx, 0, 0))
                .polygon(6, af_832_nut/0.866025).extrude(t_832_nut))
thim = thim.cut(cq.Workplane("XY")
                .box(th_pad_l - 2, lc_w + 0.5, 1.0,
                     centered=(False, True, False)))
# bridge + finger ring (ID 19) standing on the pad plane
ring_cx = th_pad_l + 4 + 12.5
thim = thim.union(cq.Workplane("XY")
                  .transformed(offset=(th_pad_l - 0.01, 0, 0))
                  .box(6, 12, 5, centered=(False, True, False)))
ring = (cq.Workplane("XY").transformed(offset=(ring_cx, 0, 0))
        .cylinder(14, 12.5, centered=(True, True, False)))
ring = ring.cut(cq.Workplane("XY").transformed(offset=(ring_cx, 0, 0))
                .cylinder(14, 9.5, centered=(True, True, False)))
thim = thim.union(ring)
out["thimble_clamp"] = thim

# ============================================================
# PART 4: base plate
# Shaft axis at local (0,0). Servo body center at +servo_shaft_off.
# ============================================================
bp = (cq.Workplane("XY")
      .box(120, 70, 5, centered=(False, True, False))
      .translate((-58, 0, 0)))
# servo cutout
bp = bp.cut(cq.Workplane("XY")
            .transformed(offset=(servo_shaft_off, 0, 0))
            .box(servo_body_l, servo_body_w, 5, centered=(True, True, False)))
# servo flange holes (8-32 + rubber dampers)
for sx in (+1, -1):
    for sy in (+1, -1):
        bp = bp.cut(cq.Workplane("XY")
                    .transformed(offset=(servo_shaft_off + sx*servo_hole_dx/2,
                                         sy*servo_hole_dy/2, 0))
                    .cylinder(5, d_832_clr/2, centered=(True, True, False)))
# AS5600 bracket mounting holes (M3 + nuts underneath)
for bx in (35.5, 56.5):
    bp = bp.cut(cq.Workplane("XY").transformed(offset=(bx, 0, 0))
                .cylinder(5, d_m3_clr/2, centered=(True, True, False)))
# corner table-mount holes
for cx in (-52, 56):
    for cy in (-29, 29):
        bp = bp.cut(cq.Workplane("XY").transformed(offset=(cx, cy, 0))
                    .cylinder(5, d_832_clr/2, centered=(True, True, False)))
out["base_plate"] = bp

# ============================================================
# PART 5: AS5600 bracket (foot + column + cantilever over axis)
# ============================================================
pcb_bottom_z = magnet_top_z + air_gap
standoff_h   = 3.0
plate_t      = 5.0
plate_bot_z  = pcb_bottom_z + pcb_t + standoff_h
plate_top_z  = plate_bot_z + plate_t

br = (cq.Workplane("XY")
      .box(26, 16, 5, centered=(False, True, False)).translate((33, 0, 0)))
for bx in (35.5, 56.5):
    br = br.cut(cq.Workplane("XY").transformed(offset=(bx, 0, 0))
                .cylinder(5, d_m3_clr/2, centered=(True, True, False)))
br = br.union(cq.Workplane("XY")
              .box(14, 14, plate_top_z, centered=(False, True, False))
              .translate((40, 0, 0)))
br = br.union(cq.Workplane("XY")
              .box(55, 18, plate_t, centered=(False, True, False))
              .translate((-13, 0, plate_bot_z)))
# chip window over the axis
br = br.cut(cq.Workplane("XY").transformed(offset=(0, 0, plate_bot_z))
            .box(13, 13, plate_t, centered=(True, True, False)))
# PCB standoffs with M3 self-tap holes
for sx in (-pcb_hole_dx/2, +pcb_hole_dx/2):
    br = br.union(cq.Workplane("XY")
                  .transformed(offset=(sx, 0, plate_bot_z - standoff_h))
                  .cylinder(standoff_h, 3.0, centered=(True, True, False)))
    br = br.cut(cq.Workplane("XY")
                .transformed(offset=(sx, 0, plate_bot_z - standoff_h))
                .cylinder(standoff_h + 6, d_m3_tap/2,
                          centered=(True, True, False)))
out["as5600_bracket"] = br

# ============================================================
# export
# ============================================================
os.makedirs("/home/claude/hw15/stl", exist_ok=True)
os.makedirs("/home/claude/hw15/step", exist_ok=True)
for name, part in out.items():
    cq.exporters.export(part, f"/home/claude/hw15/stl/{name}.stl",
                        tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(part, f"/home/claude/hw15/step/{name}.step")
    print("exported", name)

"""EEVEE look development for the walkthrough (applied to a COPY of the approved model; geometry and materials untouched).

Why the changes: EEVEE has no path-traced bounce light and lights every surface with the world, so the Cycles setup
(sky world, 188 lamps with shadows) renders blue, flat and slow. These settings keep the approved materials and lamps
and only adjust world strength, lamp shadows/intensity and EEVEE quality options so the frames read like the Cycles renders.
"""
import bpy


def setup_eevee(scene, samples=16, res=(1280, 720), exposure=0.0, fast_gi=True, shadows="key"):
    sc = scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    ee = sc.eevee
    ee.taa_render_samples = samples
    ee.use_shadows = True if hasattr(ee, "use_shadows") else None
    if hasattr(ee, "use_raytracing"):
        ee.use_raytracing = True
    if hasattr(ee, "ray_tracing_method"):
        ee.ray_tracing_method = "SCREEN"
    rto = getattr(ee, "ray_tracing_options", None)
    if rto is not None:
        for k, v in (("resolution_scale", "2"), ("use_denoise", True), ("trace_max_roughness", 0.5)):
            if hasattr(rto, k):
                try:
                    setattr(rto, k, v)
                except Exception:  # noqa: BLE001
                    pass
    if hasattr(ee, "fast_gi_method"):
        ee.fast_gi_method = "GLOBAL_ILLUMINATION"
    if hasattr(ee, "use_fast_gi"):
        ee.use_fast_gi = fast_gi
    for k, v in (("fast_gi_distance", 3.0), ("fast_gi_resolution", "2"), ("fast_gi_step_count", 6), ("horizon_quality", 0.5)):
        if hasattr(ee, k):
            try:
                setattr(ee, k, v)
            except Exception:  # noqa: BLE001
                pass
    if hasattr(ee, "shadow_pool_size"):
        ee.shadow_pool_size = "1024"
    if hasattr(ee, "use_gtao"):
        ee.use_gtao = True
    # world: keep the sky for the windows but stop it from flooding the interior with blue ambient light
    w = sc.world
    if w and w.use_nodes:
        for n in w.node_tree.nodes:
            if n.type == "BACKGROUND":
                n.inputs["Strength"].default_value = min(n.inputs["Strength"].default_value, 0.08)
    # lamps: shadows only on the strong ones (shadow pool overflow otherwise); small lamps stay unshadowed fills
    n_sh = 0
    for ld in bpy.data.lights:
        strong = ld.energy >= 60 or ld.type == "SUN"
        if shadows == "none":
            ld.use_shadow = False
        elif shadows == "key":
            ld.use_shadow = bool(strong)
        n_sh += int(ld.use_shadow)
    sc.view_settings.exposure = exposure
    return n_sh

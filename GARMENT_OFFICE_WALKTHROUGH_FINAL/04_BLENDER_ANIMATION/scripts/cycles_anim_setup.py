"""Cycles settings for camera animation on CPU (applied to a COPY of the approved model; geometry, materials and lamps unchanged).
Low samples + OpenImageDenoise with albedo/normal passes, fixed seed (noise does not crawl between frames), persistent data
(the scene is built once per shot, not once per frame), fewer light bounces."""
import bpy


def setup_cycles_anim(scene, samples=8, res=(960, 540), exposure=0.6, threshold=0.08):
    sc = scene
    sc.render.engine = "CYCLES"
    cy = sc.cycles
    cy.device = "CPU"
    cy.samples = samples
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = threshold
    cy.adaptive_min_samples = 0
    cy.use_denoising = True
    cy.denoiser = "OPENIMAGEDENOISE"
    if hasattr(cy, "denoising_input_passes"):
        cy.denoising_input_passes = "RGB_ALBEDO_NORMAL"
    if hasattr(cy, "denoising_prefilter"):
        cy.denoising_prefilter = "ACCURATE"
    if hasattr(cy, "denoising_quality"):
        cy.denoising_quality = "HIGH"
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = 4, 2, 2
    cy.transmission_bounces, cy.transparent_max_bounces, cy.volume_bounces = 4, 8, 0
    cy.caustics_reflective = cy.caustics_refractive = False
    cy.blur_glossy = 1.0
    cy.sample_clamp_indirect = 3.0
    cy.use_animated_seed = False
    cy.seed = 7
    if hasattr(cy, "use_light_tree"):
        cy.use_light_tree = True
    sc.render.use_persistent_data = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.use_motion_blur = False
    sc.view_settings.exposure = exposure

"""
═══════════════════════════════════════════════════════════════════════
 AeroMatch Backend - Production-Ready API Server
 AI-Powered Airfoil Recommendation System
═══════════════════════════════════════════════════════════════════════
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import io
import numpy as np
from pathlib import Path

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════════
# COMPREHENSIVE AIRFOIL DATABASE (25+ Airfoils with Full Details)
# ═══════════════════════════════════════════════════════════════════

AIRFOIL_DATABASE = {
    # ────────────────── GLIDERS (5) ──────────────────
    'HQ1.0-10.8': {
        'name': 'HQ1.0-10.8',
        'family': 'HQ',
        'thickness': 10.8,
        'camber': 1.0,
        'cl_design': 0.75,
        'cd_min': 0.0040,
        'ld_max': 160,
        'symmetric': False,
        're_optimal': 4.0e6,
        're_min': 2.0e6,
        're_max': 6.0e6,
        'purpose': 'glider',
        'design_speed': 'Low-Speed Soaring',
        'applications': ['Sailplanes', 'High-altitude gliders', 'Thermal soaring'],
        'stall_angle': 17.5,
        'pitch_moment': -0.020,
        'description': 'High efficiency glider airfoil with exceptional L/D for thermal soaring',
        'characteristics': ['Laminar bucket', 'Docile stall behavior', 'Excellent efficiency'],
        'tags': ['High Efficiency', 'Thermal', 'Laminar Bucket']
    },
    'ASH31-MI': {
        'name': 'ASH31-MI',
        'family': 'ASH',
        'thickness': 11.5,
        'camber': 2.2,
        'cl_design': 0.82,
        'cd_min': 0.0038,
        'ld_max': 165,
        'symmetric': False,
        're_optimal': 3.2e6,
        're_min': 2.5e6,
        're_max': 4.0e6,
        'purpose': 'glider',
        'design_speed': 'Alpine soaring',
        'applications': ['High-performance sailplanes', 'Altitude record attempts'],
        'stall_angle': 17.8,
        'pitch_moment': -0.018,
        'description': 'High-altitude optimized glider section with exceptional efficiency',
        'characteristics': ['Very low profile drag', 'Smooth aerodynamic transitions', 'Ultra-efficient'],
        'tags': ['Alpine Soaring', 'Ultra Efficient', 'Altitude Record']
    },
    'E374': {
        'name': 'E374',
        'family': 'Eppler',
        'thickness': 12.0,
        'camber': 3.0,
        'cl_design': 0.95,
        'cd_min': 0.0045,
        'ld_max': 155,
        'symmetric': False,
        're_optimal': 3.5e6,
        're_min': 2.8e6,
        're_max': 4.5e6,
        'purpose': 'glider',
        'design_speed': 'Cross-country soaring',
        'applications': ['Open-class gliders', 'Ultra-light sailplanes'],
        'stall_angle': 15.2,
        'pitch_moment': -0.048,
        'description': 'Modern glider airfoil optimized for natural laminar flow',
        'characteristics': ['Excellent laminar bucket', 'Predictable handling', 'NLF design'],
        'tags': ['NLF Design', 'Modern', 'Predictable']
    },
    'FX74-CL5-140': {
        'name': 'FX74-CL5-140',
        'family': 'F-Series',
        'thickness': 14.0,
        'camber': 5.0,
        'cl_design': 1.2,
        'cd_min': 0.0055,
        'ld_max': 150,
        'symmetric': False,
        're_optimal': 3.0e6,
        're_min': 2.0e6,
        're_max': 4.0e6,
        'purpose': 'glider',
        'design_speed': 'Moderate-Speed Soaring',
        'applications': ['Competition gliders', 'Motorgliders'],
        'stall_angle': 12.0,
        'pitch_moment': -0.085,
        'description': 'Competition glider airfoil with high CL for ridge soaring and thermals',
        'characteristics': ['High camber', 'Smooth pressure distribution', 'Ridge capable'],
        'tags': ['Competition', 'High Camber', 'Ridge Soaring']
    },
    'S1223': {
        'name': 'S1223',
        'family': 'Selig',
        'thickness': 9.7,
        'camber': 2.0,
        'cl_design': 0.85,
        'cd_min': 0.0042,
        'ld_max': 140,
        'symmetric': False,
        're_optimal': 2.0e6,
        're_min': 1.5e6,
        're_max': 3.0e6,
        'purpose': 'glider',
        'design_speed': 'High-Speed Gliding',
        'applications': ['Speed gliders', 'Wave soaring'],
        'stall_angle': 16.5,
        'pitch_moment': -0.030,
        'description': 'Ultra-thin glider section for speed and efficiency in mountain flying',
        'characteristics': ['Excellent low-speed stability', 'Minimal profile drag', 'Wave capable'],
        'tags': ['Ultra Thin', 'Speed', 'Minimal Drag']
    },

    # ────────────────── HIGH PERFORMANCE (6) ──────────────────
    'NACA63-415': {
        'name': 'NACA63-415',
        'family': 'NACA 6-Series',
        'thickness': 15.0,
        'camber': 4.0,
        'cl_design': 0.9,
        'cd_min': 0.0055,
        'ld_max': 110,
        'symmetric': False,
        're_optimal': 5.0e6,
        're_min': 4.0e6,
        're_max': 6.0e6,
        'purpose': 'high_performance',
        'design_speed': 'High-speed cruise (300+ mph)',
        'applications': ['Racing aircraft', 'High-speed trainers'],
        'stall_angle': 13.5,
        'pitch_moment': -0.065,
        'description': 'Classic high-speed laminar airfoil with natural pressure recovery',
        'characteristics': ['Sharp leading edge', 'Laminar bucket design', 'Racing optimized'],
        'tags': ['Classic Racing', 'Laminar Bucket', 'Sharp LE']
    },
    'NACA64-415': {
        'name': 'NACA64-415',
        'family': 'NACA 6-Series',
        'thickness': 15.0,
        'camber': 4.0,
        'cl_design': 0.92,
        'cd_min': 0.0052,
        'ld_max': 115,
        'symmetric': False,
        're_optimal': 5.0e6,
        're_min': 4.0e6,
        're_max': 6.0e6,
        'purpose': 'high_performance',
        'design_speed': 'Very high-speed cruise (350+ mph)',
        'applications': ['Formula 1 Air Racing', 'Military trainers'],
        'stall_angle': 14.0,
        'pitch_moment': -0.070,
        'description': 'Improved 64-series airfoil with better stall characteristics',
        'characteristics': ['Excellent speed-range', 'Improved maneuverability', 'F1 proven'],
        'tags': ['Improved Stall', 'Maneuverability', 'F1 Air Racing']
    },
    'NACA65-415': {
        'name': 'NACA65-415',
        'family': 'NACA 6-Series',
        'thickness': 15.0,
        'camber': 4.0,
        'cl_design': 0.90,
        'cd_min': 0.0050,
        'ld_max': 118,
        'symmetric': False,
        're_optimal': 6.0e6,
        're_min': 5.0e6,
        're_max': 7.0e6,
        'purpose': 'high_performance',
        'design_speed': 'Transonic speeds (Mach 0.7-0.8)',
        'applications': ['High-speed jets', 'Performance aircraft'],
        'stall_angle': 14.2,
        'pitch_moment': -0.072,
        'description': '65-series airfoil optimized for supersonic transonic flow',
        'characteristics': ['Delayed shock wave', 'Efficient at altitude', 'Transonic optimized'],
        'tags': ['Transonic', 'Shock-Optimized', 'High-Speed']
    },
    'E221': {
        'name': 'E221',
        'family': 'Eppler',
        'thickness': 15.0,
        'camber': 3.5,
        'cl_design': 1.0,
        'cd_min': 0.0058,
        'ld_max': 125,
        'symmetric': False,
        're_optimal': 5.0e6,
        're_min': 4.0e6,
        're_max': 6.0e6,
        'purpose': 'high_performance',
        'design_speed': 'Acrobatic speeds (200-280 mph)',
        'applications': ['Unlimited aerobatics', 'Performance trainers'],
        'stall_angle': 13.0,
        'pitch_moment': -0.060,
        'description': 'Advanced aerodynamic section for unlimited aerobatic aircraft',
        'characteristics': ['Excellent control authority', 'Symmetric stall', 'Aerobatic proven'],
        'tags': ['Aerobatic', 'Control Authority', 'Symmetrical Stall']
    },
    'RA15': {
        'name': 'RA15',
        'family': 'Racing',
        'thickness': 15.0,
        'camber': 2.8,
        'cl_design': 0.88,
        'cd_min': 0.0048,
        'ld_max': 128,
        'symmetric': False,
        're_optimal': 6.5e6,
        're_min': 5.0e6,
        're_max': 8.0e6,
        'purpose': 'high_performance',
        'design_speed': 'Racing speed (280-380 mph)',
        'applications': ['Air racing', 'Speed records'],
        'stall_angle': 15.0,
        'pitch_moment': -0.055,
        'description': 'Racing airfoil with optimized speed-range for air racing',
        'characteristics': ['Minimal compressibility effects', 'Efficient pitching moment', 'Record setter'],
        'tags': ['Air Racing', 'Low Compressibility', 'Speed Record']
    },
    'MH32': {
        'name': 'MH32',
        'family': 'Monoplane',
        'thickness': 14.8,
        'camber': 3.2,
        'cl_design': 0.94,
        'cd_min': 0.0051,
        'ld_max': 122,
        'symmetric': False,
        're_optimal': 4.8e6,
        're_min': 4.0e6,
        're_max': 6.0e6,
        'purpose': 'high_performance',
        'design_speed': 'High-speed cruise (250-320 mph)',
        'applications': ['Homebuilt racers', 'Custom performance aircraft'],
        'stall_angle': 13.8,
        'pitch_moment': -0.062,
        'description': 'Monoplane airfoil optimized for homebuilt high-performance aircraft',
        'characteristics': ['Good CL/CD envelope', 'Predictable handling', 'Homebuilt proven'],
        'tags': ['Homebuilt Racer', 'Custom Design', 'Predictable']
    },

    # ────────────────── GENERAL AVIATION (6) ──────────────────
    'NACA2412': {
        'name': 'NACA2412',
        'family': 'NACA 2-Digit',
        'thickness': 12.0,
        'camber': 2.0,
        'cl_design': 0.6,
        'cd_min': 0.0074,
        'ld_max': 80,
        'symmetric': False,
        're_optimal': 1.0e6,
        're_min': 0.8e6,
        're_max': 1.5e6,
        'purpose': 'general',
        'design_speed': 'Cruise 120-150 mph',
        'applications': ['Light aircraft', 'Training planes'],
        'stall_angle': 13.5,
        'pitch_moment': -0.025,
        'description': 'Classic general aviation airfoil with good low-speed lift',
        'characteristics': ['Gentle stall', 'Stable pitch behavior', 'Proven reliable'],
        'tags': ['Classic', 'Gentle Stall', 'Stable Pitch']
    },
    'NACA4412': {
        'name': 'NACA4412',
        'family': 'NACA 4-Digit',
        'thickness': 12.0,
        'camber': 4.0,
        'cl_design': 0.8,
        'cd_min': 0.0065,
        'ld_max': 95,
        'symmetric': False,
        're_optimal': 1.0e6,
        're_min': 0.8e6,
        're_max': 1.5e6,
        'purpose': 'general',
        'design_speed': 'Cruise 140-170 mph',
        'applications': ['GA high-wing aircraft', 'Bush planes'],
        'stall_angle': 12.0,
        'pitch_moment': -0.055,
        'description': 'High-lift general aviation airfoil for good climb performance',
        'characteristics': ['Good takeoff performance', 'Moderate cruise efficiency', 'Lift optimized'],
        'tags': ['High-Lift', 'Bush Planes', 'Good Climb']
    },
    'NACA23012': {
        'name': 'NACA23012',
        'family': 'NACA 2-Digit',
        'thickness': 12.0,
        'camber': 2.3,
        'cl_design': 0.65,
        'cd_min': 0.0080,
        'ld_max': 85,
        'symmetric': False,
        're_optimal': 6.0e6,
        're_min': 5.0e6,
        're_max': 8.0e6,
        'purpose': 'general',
        'design_speed': 'Cruise 150-180 mph',
        'applications': ['Modern GA aircraft', 'Efficient cruisers'],
        'stall_angle': 14.5,
        'pitch_moment': -0.035,
        'description': 'Refined airfoil with excellent stability at cruise speeds',
        'characteristics': ['Excellent pitch stability', 'Good CL range', 'Modern design'],
        'tags': ['Pitch Stable', 'Efficient Cruise', 'Modern']
    },
    'NACA230-1234': {
        'name': 'NACA230-1234',
        'family': 'NACA Modern',
        'thickness': 12.0,
        'camber': 2.3,
        'cl_design': 0.70,
        'cd_min': 0.0070,
        'ld_max': 90,
        'symmetric': False,
        're_optimal': 8.0e6,
        're_min': 6.0e6,
        're_max': 10.0e6,
        'purpose': 'general',
        'design_speed': 'Cruise 160-190 mph',
        'applications': ['Efficient GA aircraft', 'Personal transport'],
        'stall_angle': 14.0,
        'pitch_moment': -0.040,
        'description': 'Advanced general aviation section optimized for efficiency',
        'characteristics': ['Low profile drag', 'Smooth stall entry', 'Efficient design'],
        'tags': ['Low Profile Drag', 'Smooth Stall', 'Efficient']
    },
    'GA45A': {
        'name': 'GA45A',
        'family': 'GA Modern',
        'thickness': 11.5,
        'camber': 2.2,
        'cl_design': 0.72,
        'cd_min': 0.0068,
        'ld_max': 92,
        'symmetric': False,
        're_optimal': 2.5e6,
        're_min': 2.0e6,
        're_max': 3.5e6,
        'purpose': 'general',
        'design_speed': 'Cruise 140-170 mph',
        'applications': ['Modern light aircraft', 'Efficient trainers'],
        'stall_angle': 14.8,
        'pitch_moment': -0.032,
        'description': 'Modern general aviation airfoil with smooth aerodynamics',
        'characteristics': ['Natural stall progression', 'Excellent visibility', 'Modern proven'],
        'tags': ['Modern Design', 'Natural Stall', 'Good Visibility']
    },
    'BAC3-11/13': {
        'name': 'BAC3-11/13',
        'family': 'BAC',
        'thickness': 13.0,
        'camber': 2.5,
        'cl_design': 0.78,
        'cd_min': 0.0072,
        'ld_max': 96,
        'symmetric': False,
        're_optimal': 3.0e6,
        're_min': 2.5e6,
        're_max': 4.0e6,
        'purpose': 'general',
        'design_speed': 'Cruise 150-180 mph',
        'applications': ['Commuter aircraft', 'Twin-engine GA'],
        'stall_angle': 13.2,
        'pitch_moment': -0.048,
        'description': 'Proven general aviation section with robust characteristics',
        'characteristics': ['Excellent in icing', 'Good drag coefficient', 'Robust design'],
        'tags': ['Icing Resistant', 'Twin-Engine', 'Robust']
    },

    # ────────────────── LAMINAR FLOW (4) ──────────────────
    'NACA631-412': {
        'name': 'NACA631-412',
        'family': 'NACA 6-Series',
        'thickness': 12.0,
        'camber': 3.0,
        'cl_design': 0.7,
        'cd_min': 0.0062,
        'ld_max': 100,
        'symmetric': False,
        're_optimal': 1.0e7,
        're_min': 8.0e6,
        're_max': 12.0e6,
        'purpose': 'laminar_flow',
        'design_speed': 'Cruise 180-220 mph',
        'applications': ['Business jets', 'Efficient transports'],
        'stall_angle': 15.5,
        'pitch_moment': -0.045,
        'description': 'Laminar-flow airfoil with extended low-drag bucket',
        'characteristics': ['Low profile drag', 'Natural laminar flow', 'NLF proven'],
        'tags': ['Classic NLF', 'Low Drag', 'Extended Laminar']
    },
    'NLF414F': {
        'name': 'NLF414F',
        'family': 'NLF Modern',
        'thickness': 14.0,
        'camber': 2.8,
        'cl_design': 0.75,
        'cd_min': 0.0048,
        'ld_max': 135,
        'symmetric': False,
        're_optimal': 8.0e6,
        're_min': 6.0e6,
        're_max': 10.0e6,
        'purpose': 'laminar_flow',
        'design_speed': 'Efficient cruise 200-240 mph',
        'applications': ['Green aircraft', 'Efficient transports'],
        'stall_angle': 16.0,
        'pitch_moment': -0.038,
        'description': 'Natural laminar flow airfoil optimized for efficient cruise',
        'characteristics': ['Laminar separation bubble', 'Extended laminar region', 'Green optimized'],
        'tags': ['Efficient Cruise', 'Green Aircraft', 'Modern']
    },
    'F6-126-09': {
        'name': 'F6-126-09',
        'family': 'F-Series',
        'thickness': 9.0,
        'camber': 2.1,
        'cl_design': 0.68,
        'cd_min': 0.0038,
        'ld_max': 145,
        'symmetric': False,
        're_optimal': 5.0e6,
        're_min': 4.0e6,
        're_max': 6.0e6,
        'purpose': 'laminar_flow',
        'design_speed': 'Cruise 220-280 mph',
        'applications': ['High-altitude transports', 'Experimental aircraft'],
        'stall_angle': 17.2,
        'pitch_moment': -0.025,
        'description': 'Thin laminar-flow section for high-altitude flight',
        'characteristics': ['Very low profile drag', 'Wide laminar bucket', 'Altitude optimized'],
        'tags': ['High-Altitude', 'Very Low Drag', 'Thin Section']
    },
    'LSE': {
        'name': 'LSE',
        'family': 'LSE Advanced',
        'thickness': 12.5,
        'camber': 3.0,
        'cl_design': 0.76,
        'cd_min': 0.0052,
        'ld_max': 130,
        'symmetric': False,
        're_optimal': 7.0e6,
        're_min': 6.0e6,
        're_max': 9.0e6,
        'purpose': 'laminar_flow',
        'design_speed': 'Cruise 200-250 mph',
        'applications': ['Modern efficient transports', 'Regional aircraft'],
        'stall_angle': 15.8,
        'pitch_moment': -0.042,
        'description': 'Advanced laminar-flow airfoil with high Reynolds number optimization',
        'characteristics': ['Low noise signature', 'Minimal shock waves', 'Regional optimized'],
        'tags': ['Advanced NLF', 'Low Noise', 'Regional']
    },

    # ────────────────── SYMMETRIC (4) ──────────────────
    'NACA0012': {
        'name': 'NACA0012',
        'family': 'NACA 4-Digit',
        'thickness': 12.0,
        'camber': 0.0,
        'cl_design': 0.4,
        'cd_min': 0.0085,
        'ld_max': 60,
        'symmetric': True,
        're_optimal': 1.0e6,
        're_min': 0.8e6,
        're_max': 2.0e6,
        'purpose': 'acrobatic',
        'design_speed': 'Aerobatic speeds (150-250 mph)',
        'applications': ['Aerobatic aircraft', 'Rotor blades'],
        'stall_angle': 15.5,
        'pitch_moment': -0.002,
        'description': 'Classic symmetric airfoil for aerobatic and vertical flight',
        'characteristics': ['Identical upper/lower surfaces', 'Zero camber', 'Bidirectional'],
        'tags': ['Standard Aerobatic', 'Bidirectional', 'Rotor']
    },
    'NACA0015': {
        'name': 'NACA0015',
        'family': 'NACA 4-Digit',
        'thickness': 15.0,
        'camber': 0.0,
        'cl_design': 0.5,
        'cd_min': 0.0095,
        'ld_max': 65,
        'symmetric': True,
        're_optimal': 1.5e6,
        're_min': 1.0e6,
        're_max': 2.5e6,
        'purpose': 'acrobatic',
        'design_speed': 'Aerobatic speeds (160-260 mph)',
        'applications': ['High-G aerobatic aircraft', 'Stronger structures'],
        'stall_angle': 15.8,
        'pitch_moment': -0.001,
        'description': 'Thicker symmetric airfoil with better structural depth',
        'characteristics': ['More thickness', 'Better bending stiffness', 'Structural capable'],
        'tags': ['Structural Depth', 'High-G', 'Stronger']
    },
    'NACA0018': {
        'name': 'NACA0018',
        'family': 'NACA 4-Digit',
        'thickness': 18.0,
        'camber': 0.0,
        'cl_design': 0.55,
        'cd_min': 0.0105,
        'ld_max': 62,
        'symmetric': True,
        're_optimal': 2.0e6,
        're_min': 1.5e6,
        're_max': 3.0e6,
        'purpose': 'acrobatic',
        'design_speed': 'Unlimited aerobatics (Inverted cruise)',
        'applications': ['Unlimited aerobatic aircraft', 'Extreme performance'],
        'stall_angle': 16.0,
        'pitch_moment': -0.0005,
        'description': 'Heavy-duty symmetric airfoil for extreme aerobatic maneuvers',
        'characteristics': ['Maximum thickness', 'Superior structural rigidity', 'Unlimited capable'],
        'tags': ['Heavy-Duty', 'Extreme Aerobatics', 'Rigid']
    },
    'SC7012': {
        'name': 'SC7012',
        'family': 'SC Modern',
        'thickness': 12.0,
        'camber': 0.0,
        'cl_design': 0.48,
        'cd_min': 0.0080,
        'ld_max': 68,
        'symmetric': True,
        're_optimal': 1.2e6,
        're_min': 1.0e6,
        're_max': 2.0e6,
        'purpose': 'acrobatic',
        'design_speed': 'Advanced aerobatics (170-270 mph)',
        'applications': ['Advanced aerobatic trainers', 'Sport aircraft'],
        'stall_angle': 16.2,
        'pitch_moment': -0.0008,
        'description': 'Modern symmetric airfoil with optimized aerodynamics for aerobatics',
        'characteristics': ['Smooth pressure distribution', 'Excellent pitch control', 'Sport optimized'],
        'tags': ['Modern Symmetric', 'Smooth Aerodynamics', 'Sport']
    }
}

# ═══════════════════════════════════════════════════════════════════
# REQUEST LOGGING & ANALYTICS
# ═══════════════════════════════════════════════════════════════════

request_log = []

def log_request(req_type, params, result_count=0):
    """Log incoming requests for analytics"""
    request_log.append({
        'timestamp': datetime.now().isoformat(),
        'type': req_type,
        'params': params,
        'result_count': result_count,
        'ip': request.remote_addr
    })

# ═══════════════════════════════════════════════════════════════════
# CORE MATCHING & SCORING ENGINE
# ═══════════════════════════════════════════════════════════════════

def score_airfoil_against_params(airfoil_name, params):
    """Score an airfoil against user parameters"""
    af = AIRFOIL_DATABASE.get(airfoil_name)
    if not af:
        return None

    score = 0
    reasons = []

    # Purpose matching (strongest signal)
    if params.get('purpose') and af['purpose'] == params['purpose']:
        score += 30
        reasons.append(f"Purpose match: {params['purpose']}")

    # L/D target
    if params.get('target_ld'):
        target = float(params['target_ld'])
        delta = abs(af['ld_max'] - target)
        ld_score = max(0, 25 - delta * 0.4)
        score += ld_score
        reasons.append(f"L/D: {af['ld_max']} (target: {target})")

    # CL target
    if params.get('target_cl'):
        target = float(params['target_cl'])
        delta = abs(af['cl_design'] - target)
        cl_score = max(0, 20 - delta * 20)
        score += cl_score
        reasons.append(f"CL: {af['cl_design']:.2f}")

    # Thickness target
    if params.get('target_thickness'):
        target = float(params['target_thickness'])
        delta = abs(af['thickness'] - target)
        t_score = max(0, 15 - delta * 2)
        score += t_score
        reasons.append(f"Thickness: {af['thickness']}%")

    # Camber target
    if params.get('target_camber'):
        target = float(params['target_camber'])
        delta = abs(af['camber'] - target)
        c_score = max(0, 15 - delta * 3)
        score += c_score
        reasons.append(f"Camber: {af['camber']}%")

    # Symmetric preference
    if params.get('symmetric_only') == 'true' and af['symmetric']:
        score += 15
        reasons.append("Symmetric profile")
    elif params.get('cambered_only') == 'true' and not af['symmetric']:
        score += 10
        reasons.append("Cambered profile")

    # Reynolds number compatibility
    if params.get('re_range'):
        re_map = {
            'low': 0.5e6,
            'medium': 3e6,
            'high': 7.5e6,
            'very_high': 12e6
        }
        target_re = re_map.get(params['re_range'], 1e6)
        if af['re_min'] <= target_re <= af['re_max']:
            score += 10
            reasons.append(f"Re compatible: {target_re/1e6:.1f}M")

    # Mach number consideration
    if params.get('mach_number'):
        mach = float(params['mach_number'])
        if mach < 0.3 and af['purpose'] in ['general', 'laminar_flow', 'glider']:
            score += 5
        elif 0.3 <= mach < 0.85 and af['family'] in ['NACA 6-Series', 'Racing']:
            score += 8
        elif mach >= 0.85 and 'Transonic' in af['tags']:
            score += 12

    return {
        'airfoil_name': airfoil_name,
        'airfoil': af,
        'score': min(100, score),
        'reasons': reasons,
        'match_percentage': round(min(100, score), 2)
    }

def find_best_matches(params, top_n=5):
    """Find best matching airfoils for given parameters"""
    all_scores = []
    for name in AIRFOIL_DATABASE.keys():
        result = score_airfoil_against_params(name, params)
        if result and result['score'] > 10:
            all_scores.append(result)

    all_scores.sort(key=lambda x: x['score'], reverse=True)
    return all_scores[:top_n]

# ═══════════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'airfoils_in_db': len(AIRFOIL_DATABASE),
        'requests_logged': len(request_log)
    })

@app.route('/api/database', methods=['GET'])
def get_database():
    """Return full airfoil database"""
    return jsonify({
        'success': True,
        'total_airfoils': len(AIRFOIL_DATABASE),
        'database': AIRFOIL_DATABASE
    })

@app.route('/api/airfoil/<name>', methods=['GET'])
def get_airfoil(name):
    """Get details for a specific airfoil"""
    af = AIRFOIL_DATABASE.get(name)
    if not af:
        return jsonify({'error': f'Airfoil "{name}" not found'}), 404

    return jsonify({
        'success': True,
        'airfoil': af,
        'additional_info': {
            're_range': f"{af['re_min']/1e6:.1f}M – {af['re_max']/1e6:.1f}M",
            'efficiency_class': 'Excellent' if af['ld_max'] >= 120 else 'Good' if af['ld_max'] >= 90 else 'Moderate',
            'use_case_count': len(af.get('applications', [])),
            'characteristics_count': len(af.get('characteristics', []))
        }
    })

@app.route('/api/recommend/by-parameters', methods=['POST'])
def recommend_by_params():
    """Recommend airfoils based on parameters"""
    data = request.get_json() or {}

    # Extract parameters
    params = {
        'purpose': data.get('purpose'),
        'target_ld': data.get('target_ld'),
        'target_cl': data.get('target_cl'),
        'target_thickness': data.get('target_thickness'),
        'target_camber': data.get('target_camber'),
        'symmetric_only': data.get('symmetric_only'),
        'cambered_only': data.get('cambered_only'),
        're_range': data.get('re_range'),
        'mach_number': data.get('mach_number')
    }

    # Find matches
    results = find_best_matches(params, top_n=5)
    
    if not results:
        return jsonify({
            'success': False,
            'error': 'No airfoils match your criteria. Try relaxing your constraints.',
            'total_matches': 0
        }), 404

    # Log request
    log_request('parameter_recommendation', params, len(results))

    return jsonify({
        'success': True,
        'search_params': params,
        'total_matches': len(results),
        'recommendations': results,
        'top_match': results[0] if results else None
    })

@app.route('/api/recommend/by-purpose', methods=['POST'])
def recommend_by_purpose_endpoint():
    """Recommend airfoils by application purpose"""
    data = request.get_json() or {}
    purpose = data.get('purpose')
    target_ld = data.get('target_ld')

    if not purpose:
        return jsonify({'error': 'Purpose parameter required'}), 400

    # Filter by purpose
    purpose_airfoils = [
        (name, af) for name, af in AIRFOIL_DATABASE.items()
        if af['purpose'] == purpose
    ]

    if not purpose_airfoils:
        return jsonify({
            'error': f'No airfoils found for purpose: {purpose}',
            'available_purposes': list(set(af['purpose'] for af in AIRFOIL_DATABASE.values()))
        }), 404

    # Score them
    results = []
    for name, af in purpose_airfoils:
        score_dict = score_airfoil_against_params(name, {'purpose': purpose, 'target_ld': target_ld})
        if score_dict:
            results.append(score_dict)

    results.sort(key=lambda x: x['score'], reverse=True)
    
    log_request('purpose_recommendation', {'purpose': purpose, 'target_ld': target_ld}, len(results))

    return jsonify({
        'success': True,
        'purpose': purpose,
        'target_ld': target_ld,
        'total_matches': len(results),
        'recommendations': results
    })

@app.route('/api/compare', methods=['POST'])
def compare_airfoils():
    """Compare multiple airfoils side-by-side"""
    data = request.get_json() or {}
    names = data.get('airfoils', [])

    if not names or len(names) < 2:
        return jsonify({'error': 'Provide at least 2 airfoil names to compare'}), 400

    comparison = {}
    for name in names:
        if name in AIRFOIL_DATABASE:
            comparison[name] = AIRFOIL_DATABASE[name]

    return jsonify({
        'success': True,
        'comparison': comparison,
        'count': len(comparison)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    stats = {
        'total_airfoils': len(AIRFOIL_DATABASE),
        'by_purpose': {},
        'total_requests': len(request_log),
        'recent_requests': request_log[-10:] if request_log else []
    }

    for af in AIRFOIL_DATABASE.values():
        purpose = af['purpose']
        if purpose not in stats['by_purpose']:
            stats['by_purpose'][purpose] = 0
        stats['by_purpose'][purpose] += 1

    return jsonify({
        'success': True,
        'statistics': stats
    })

# ═══════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 80)
    print(" AeroMatch Backend API Server")
    print(" AI-Powered Airfoil Recommendation Engine")
    print("=" * 80)
    print(f"\n✓ Loaded {len(AIRFOIL_DATABASE)} airfoils")
    print(f"✓ Purposes: {', '.join(set(af['purpose'] for af in AIRFOIL_DATABASE.values()))}")
    print(f"\n▸ Running on http://0.0.0.0:5000")
    print(f"▸ CORS enabled for frontend integration")
    print("\n" + "=" * 80 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

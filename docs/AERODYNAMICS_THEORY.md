# Aerodynamic Theory — AeroMatch Knowledge Base

> This document provides the theoretical foundation behind AeroMatch.
> It explains the aerodynamics concepts that the platform's matching engine is built upon, written for readers who may not have a formal aeronautics background.

---

## Table of Contents

1. [What is an Airfoil?](#1-what-is-an-airfoil)
2. [Anatomy of an Airfoil — Key Geometric Parameters](#2-anatomy-of-an-airfoil--key-geometric-parameters)
3. [Aerodynamic Parameters That Define Performance](#3-aerodynamic-parameters-that-define-performance)
4. [Types of Airfoils and Their Applications](#4-types-of-airfoils-and-their-applications)
5. [The Lift-to-Drag Ratio — Definition and Importance](#5-the-lift-to-drag-ratio--definition-and-importance)
6. [What Is Airfoil Optimization?](#6-what-is-airfoil-optimization)
7. [The Reynolds Number — Why It Matters](#7-the-reynolds-number--why-it-matters)
8. [Stall, the Boundary Layer, and Why Profile Shape Is Critical](#8-stall-the-boundary-layer-and-why-profile-shape-is-critical)
9. [How AeroMatch Uses These Concepts](#9-how-aeromatch-uses-these-concepts)
10. [References](#10-references)

---

## 1. What is an Airfoil?

An **airfoil** (also spelled *aerofoil*) is the cross-sectional shape of a wing, blade, or fin when sliced perpendicular to its span. It is the two-dimensional profile that, when moved through a fluid (air or water), generates the aerodynamic forces that make flight possible.

In practice, real wings are three-dimensional, but airfoil analysis focuses on a two-dimensional section to simplify understanding.

When air flows over an airfoil, it splits at the **leading edge**, travels along the upper and lower surfaces, and rejoins at the **trailing edge**. Because the upper surface is typically more curved than the lower surface, air must travel faster over the top. Lift is generated due to a combination of pressure differences and the downward deflection of airflow. While Bernoulli’s principle explains the relationship between velocity and pressure, a complete explanation also involves Newton’s laws and flow circulation around the airfoil.

The shape of the airfoil — how thick it is, how curved, where the thickest point sits — determines almost everything about how a wing behaves: how much lift it generates, how much drag it incurs, at what angle it stalls, and how it performs across different speeds.

---

## 2. Anatomy of an Airfoil — Key Geometric Parameters

Every airfoil can be fully described by a small set of geometric parameters. Understanding these is essential to understanding AeroMatch's database and scoring engine.

### 2.1 Chord Line and Chord Length (*c*)

The **chord line** is a straight line drawn from the leading edge to the trailing edge. Its length, the **chord length** *c*, is the reference dimension against which all other dimensions are expressed as percentages. For example, "12% thickness" means the maximum thickness is 12% of the chord length.

### 2.2 Thickness (*t/c*)

**Thickness** is the maximum perpendicular distance between the upper and lower surfaces, expressed as a percentage of chord. It is one of the most influential geometric parameters, but its effect must be considered alongside camber and operating conditions.

- **Thin profiles (t/c < 9%):** Low drag at high speeds; used in supersonic and transonic aircraft. Very sensitive to angle of attack; narrow operating envelope.
- **Medium profiles (t/c 9–15%):** The workhorse range. Good balance of lift capacity, drag, and structural depth. Used in general aviation, UAVs, and most competition sailplanes.
- **Thick profiles (t/c > 18%):** High structural depth (useful for fitting spars and fuel tanks), gentle stall behaviour, but higher drag. Used at the root sections of large wings and in wind turbine blades.

The NACA four-digit designation encodes thickness directly: **NACA 2412** has a maximum thickness of **12%** chord.

### 2.3 Camber and Camber Line

**Camber** is the maximum perpendicular distance between the chord line and the **mean camber line** — the curve equidistant between the upper and lower surfaces — expressed as a percentage of chord.

- A **zero-camber** (symmetric) profile has the camber line coinciding with the chord line. It generates zero lift at zero angle of attack.
- A **positively cambered** profile curves upward. It generates lift even at zero angle of attack, meaning the wing can fly "flatter" for a given airspeed.

For NACA four-digit airfoils, the first digit encodes camber: **NACA 2412** has **2%** maximum camber.

### 2.4 Position of Maximum Thickness and Maximum Camber

Where along the chord the maximum thickness and maximum camber occur has a significant effect on performance:

| Parameter Position Along Chord | Typical Location (% of chord) |                           Aerodynamic Effect                             |
|--------------------------------|-------------------------------|--------------------------------------------------------------------------|
| Thickness peak (forward)       | 25–30%                        | Higher maximum lift, gentler stall, increased drag                       |
| Thickness peak (mid)           | 35–40%                        | Balanced performance; most commonly used configuration                   |
| Thickness peak (aft)           | 45–50%                        | Extended laminar flow, lower drag in design range, but sharper stall     |
| Camber peak (forward)          | 30–40%                        | Higher lift at lower angles of attack, increased pitching moment         |
| Camber peak (aft)              | 50–60%                        | Reduced drag at cruise, improved efficiency in laminar-flow airfoils     |

The positioning of thickness and camber significantly influences pressure distribution, boundary layer behavior, and overall aerodynamic efficiency.

For NACA four-digit airfoils, the second digit gives the position of maximum camber in tenths of chord: **NACA 2412** has maximum camber at **40%** chord (digit = 4, position = 4/10 = 40%).

### 2.5 Leading Edge Radius

The **leading edge radius** describes how blunt or sharp the nose of the airfoil is. A larger radius gives gentler stall behaviour (the flow separates more gradually) but increases drag. A sharp leading edge (as in supersonic profiles) minimises wave drag but stalls abruptly and severely.

### 2.6 Trailing Edge Angle

The **trailing edge angle** affects the pressure recovery along the aft portion of the airfoil. A blunt trailing edge improves lift but increases drag. Most practical airfoils taper to a near-point.

---

## 3. Aerodynamic Parameters That Define Performance

Geometry creates shape; aerodynamic parameters describe how that shape *performs* in actual flow conditions.

### 3.1 Lift Coefficient (*C*_L)

The **lift coefficient** is a dimensionless number that quantifies the lift force generated relative to the dynamic pressure and reference area:

```
         L
C_L = --------
       q · S

where  L = lift force (N)
       q = dynamic pressure = ½ρV²  (Pa)
       S = wing reference area (m²)
```

*C_L* depends on angle of attack, airfoil shape, and Reynolds number. A higher *C_L* means more lift for the same speed and wing area — desirable for slow-flying aircraft (gliders, STOL aircraft) but less important for fast ones.

**Typical values:**

| Flight Condition             | Typical C_L Range|
|------------------------------|------------------|
| Cruise (general aviation)    | 0.3 – 0.6        |
| Cruise (glider)              | 0.7 – 1.0        |
| Low-speed / high-lift        | 1.2 – 1.8        |
| Near stall (maximum C_L)     | 1.4 – 2.2        |

### 3.2 Drag Coefficient (*C*_D)

The **drag coefficient** quantifies the aerodynamic resistance:

```
         D
C_D = --------
       q · S
```

For a 2-D airfoil section, drag comes from two sources:

- **Pressure drag (form drag):** Caused by the asymmetric pressure distribution around the body. Depends heavily on thickness and angle of attack.
- **Skin friction drag:** Caused by viscous shear stress on the surface. Depends on surface finish, Reynolds number, and whether the boundary layer is laminar or turbulent.

In finite wings, an additional component called induced drag arises due to wingtip vortices, though this is not captured in two-dimensional airfoil analysis.

Laminar-flow airfoils (NACA 6-series, Eppler, Wortmann FX) are designed to keep the boundary layer laminar over a large portion of the chord, dramatically reducing skin friction drag — but only within a narrow "drag bucket" of angles of attack.

### 3.3 Pitching Moment Coefficient (*C*_M)

The **pitching moment coefficient** quantifies the tendency of the airfoil to rotate nose-up or nose-down about the aerodynamic centre. A large negative *C*_M (strong nose-down tendency) means the horizontal tail must produce a downward force to maintain trim, which is effectively additional drag. Reflexed camber lines and certain 5-digit NACA profiles are designed to minimise *C*_M.

### 3.4 Maximum Angle of Attack and Stall Angle

The **stall angle** (or critical angle of attack) is the angle at which flow separates from the upper surface and lift collapses. Beyond this angle, drag rises sharply and lift drops. Thicker airfoils with rounded leading edges generally have higher stall angles and gentler stall characteristics than thin, sharp-nosed profiles.

---

## 4. Types of Airfoils and Their Applications

Airfoils are not one-size-fits-all. Different applications impose fundamentally different requirements, and the airfoil family chosen must match those requirements.

### 4.1 Symmetric Airfoils

A **symmetric airfoil** has zero camber — the upper and lower surfaces are mirror images of each other.

**Key properties:**
- Generates zero lift at zero angle of attack
- Generates equal lift in both directions (upward or downward) when the angle of attack is reversed
- Pitching moment is effectively zero at all angles
- Typically lower maximum lift coefficient than cambered profiles

**Where they are used:**

|                Application              |                           Reason                             |
|-----------------------------------------|--------------------------------------------------------------|
| Aerobatic aircraft                      | Performs equally well in upright and inverted flight         |
| Helicopter rotor blades                 | Blade pitch varies cyclically in both directions             |
| Aircraft tail surfaces                  | Must generate upward or downward force for trim              |
| Supersonic aircraft                     | Thin symmetric profiles reduce wave drag                     |
| Wind turbine blades (pitch-controlled)  | Operate effectively across positive and negative angles      |

**Common examples:** NACA 0012, NACA 0015, NACA 0018, NACA 64A010

### 4.2 Cambered Airfoils

A **cambered airfoil** has a curved mean camber line, so the upper surface bulges more than the lower. This asymmetry means the airfoil generates lift at zero angle of attack, which is almost always desirable for a fixed-wing aircraft cruising in level flight.

**Key properties:**
- Higher maximum lift coefficient than a symmetric profile of similar thickness
- Generates lift with a smaller pitch angle, reducing fuselage drag
- Has a non-zero pitching moment (usually nose-down, i.e. negative *C*_M)
- Generally better L/D at the design lift coefficient

**Sub-categories and their uses:**

|      Sub-type       |                   Characteristics                    |           Typical Applications            |
|---------------------|------------------------------------------------------|-------------------------------------------|
| Low camber (1–3%)   | Moderate lift, low pitching moment                   | General aviation, trainers, UAVs          |
| Medium camber (3–5%)| Higher lift, efficient at moderate speeds            | Gliders, RC aircraft, sailplanes          |
| High camber (5–9%)  | Very high lift at low speeds, larger pitching moment | Slow UAVs, STOL aircraft, model aircraft  |
| Reflexed camber     | Near-zero pitching moment                            | Flying wings, tailless aircraft           |
| Laminar-flow        | Aft-loaded camber, low drag in narrow range          | High-performance gliders, transports      |

**Common examples:** NACA 2412, NACA 4412, Eppler 387, FX 63-137, Selig S1223, Clark Y

### 4.3 Laminar-Flow Airfoils

**Laminar-flow airfoils** (primarily the NACA 6-series and later families like Wortmann FX, Eppler, and Selig) are designed to keep the boundary layer laminar as far back as possible — typically to 40–60% chord. The result is dramatically lower skin friction drag within a specific range of lift coefficients (the "drag bucket"), making them highly efficient at their design point.

**Trade-off:** Outside the drag bucket, drag rises sharply. Laminar flow is also easily disrupted by surface contamination (rain, insects), so laminar-flow airfoils are more sensitive to real-world conditions than classical profiles.

### 4.4 Supercritical Airfoils

Developed for transonic transport aircraft, **supercritical airfoils** have a flattened upper surface that delays the onset of shock waves and reduces wave drag near Mach 1. They are not relevant to subsonic aircraft but are standard on all modern jet airliners.

### 4.5 Thick Root vs. Thin Tip Profiles

In a real wing, the airfoil section changes along the span. The **root section** (inboard) is thick (18–30%) to accommodate structural spars, landing gear bays, and fuel tanks. The **tip section** is thin (8–12%) to minimise induced drag and improve aileron effectiveness. The transition between them is carefully designed to maintain acceptable stall characteristics across the span.

---

## 5. The Lift-to-Drag Ratio — Definition and Importance

The **lift-to-drag ratio** (L/D), also written as *C*_L/*C*_D at a given angle of attack, is one of the most important measures of aerodynamic efficiency for an airfoil or complete aircraft. It quantifies how much useful force (lift) is obtained per unit of wasted force (drag).

```
        L     C_L
L/D = ─── = ─────
        D     C_D
```

### 5.1 Physical Meaning

Think of L/D as the "aerodynamic efficiency" of the profile. An L/D of 40 means the wing generates 40 N of lift for every 1 N of drag — or equivalently, the aircraft can glide 40 metres forward for every 1 metre it descends in still air.

### 5.2 Why L/D Matters

| Application Context    |                What L/D Influences                |
|------------------------|---------------------------------------------------|
| Unpowered gliders      | Determines glide range directly                   |
| Powered aircraft       | Reduces thrust required for steady flight         |
| Fuel efficiency        | Directly impacts range and endurance              |
| Wind turbines          | Affects power extraction efficiency               |
| UAVs / drones          | Determines endurance and operational range        |

### 5.3 Typical L/D Values

|           Aircraft / Application        | Typical Maximum L/D |
|-----------------------------------------|---------------------|
| Flat plate                              | 4 – 8               |
| Light aircraft (e.g., Cessna 172)       | 9 – 11              |
| Commercial airliner                     | 14 – 18             |
| High-performance glider                 | 40 – 70             |
| Competition sailplane                   | ~65                 |
| Large bird (e.g., albatross)            | ~20                 |
| Wind turbine blade section              | 80 – 120            |

### 5.4 The Polar Curve

The relationship between *C*_L and *C*_D at all angles of attack is called the **polar curve** (or drag polar). The maximum L/D occurs at the point on the polar where a straight line from the origin is tangent to the curve. The shape of the polar is the definitive performance fingerprint of an airfoil.

AeroMatch links directly to the polar diagrams for every matched profile on airfoiltools.com, allowing users to see the full operating envelope beyond the single design-point values shown in the database.

---

## 6. What Is Airfoil Optimization?

**Airfoil optimization** is the process of finding or modifying an airfoil shape to achieve the best possible performance for a specified set of operating conditions and constraints. It is one of the most computationally intensive tasks in aeronautical engineering.

### 6.1 What "Optimal" Means Depends on the Mission

There is no universally "best" airfoil — optimality is always relative to a specific mission. Compare:

| Mission Type          | Optimization Objective              | Key Constraint                      |
|-----------------------|-------------------------------------|-------------------------------------|
| Competition glider    | Maximize L/D at cruise C_L          | Minimum thickness for structure     |
| Racing aircraft       | Minimize drag at high speed         | Sufficient lift for takeoff/landing |
| STOL aircraft         | Maximize maximum lift coefficient   | Stable low-speed handling           |
| Wind turbine          | Maximize torque output              | Structural strength and fatigue life|
| Supersonic aircraft   | Minimize wave drag                  | Adequate maneuverability            |

### 6.2 The Parameters That Can Be Changed

Optimization works by varying the airfoil's geometric parameters (or directly the surface coordinates) and evaluating the aerodynamic performance at each step:

**Geometric variables (what gets changed):**
- Maximum thickness and its chordwise position
- Maximum camber magnitude and its chordwise position
- Leading edge radius
- Trailing edge thickness and angle
- Detailed shape of the camber line (especially for laminar-flow designs)

**Performance objectives (what gets measured):**
- Maximise L/D at the design lift coefficient
- Minimise *C*_D over a range of *C*_L values (drag bucket width)
- Maximise *C*_L max (highest possible lift before stall)
- Minimise *C*_M (pitching moment, for trim drag)
- Delay stall onset angle
- Maintain laminar flow to a target chordwise position

**Constraints (what must not be violated):**
- Minimum thickness (structural)
- Maximum pitching moment (tail sizing)
- Acceptable stall characteristics (gradual, not abrupt)
- Manufacturing constraints (smooth, producible surface)
- Reynolds number range (the profile must work at the actual flight speed)

### 6.3 Classical vs. Computational Optimization

**Classical approach (pre-1970s):** NACA and other institutions systematically tested hundreds of geometric variations in wind tunnels and catalogued the results. The NACA 4-digit, 5-digit, and 6-series families emerged from this empirical approach. Designers then picked the best-available profile from the catalogue.

**Computational approach (modern):** Optimization algorithms (gradient descent, genetic algorithms, adjoint methods) directly search the geometric parameter space, evaluating thousands of candidate shapes using panel methods (XFOIL), RANS CFD solvers, or surrogate models. This produces airfoils precisely tailored to the mission — but requires significant computational expertise.

**AeroMatch's approach:** A curated database of proven airfoils from both classical and modern families, matched to user requirements via a weighted scoring engine. This occupies the practical middle ground: faster than computational optimization, smarter than manual catalogue browsing.

### 6.4 The Multi-Disciplinary Challenge

In practice, the aerodynamicist never optimizes the airfoil in isolation. The wing must also satisfy:

- **Structural requirements:** Thick enough for spars, ribs, and sufficient second moment of area to resist bending.
- **Manufacturing requirements:** The surface must be achievable with available fabrication methods (composites, aluminium, foam-and-glass).
- **Handling qualities:** The stall must be gradual and recoverable; the aircraft must be stable.
- **Systems integration:** The wing must accommodate fuel, landing gear, actuators, and control surfaces.

This is why the field is called **multidisciplinary design optimization (MDO)** — and why AeroMatch is framed as a *multidisciplinary* project.

---

## 7. The Reynolds Number — Why It Matters

The **Reynolds number** (*Re*) is a dimensionless ratio of inertial to viscous forces in a fluid flow. For an airfoil it is defined as:

```
        ρ · V · c
Re = ─────────────
           μ

where  ρ = air density (kg/m³)
       V = freestream velocity (m/s)
       c = chord length (m)
       μ = dynamic viscosity of air (Pa·s ≈ 1.789 × 10⁻⁵ at sea level)
```

### 7.1 Why It Fundamentally Changes Airfoil Behaviour

The same airfoil shape can behave *completely differently* at different Reynolds numbers. This is one of the most counter-intuitive facts in aerodynamics:

| Reynolds Number Range     | Flow Regime                  |                 Practical Implications                    |
|---------------------------|------------------------------|-----------------------------------------------------------|
| < 10,000                  | Viscous-dominated            | Very low lift; flight is difficult                        |
| 10,000 – 100,000          | Transitional                 | Sensitive to disturbances; unstable behavior              |
| 100,000 – 500,000         | Low Reynolds number          | Requires specialized airfoils (UAVs, RC aircraft)         |
| 500,000 – 3,000,000       | Medium Reynolds number       | Typical for general aviation and gliders                  |
| 3,000,000 – 10,000,000    | High Reynolds number         | Suitable for transport aircraft and efficient designs     |
| > 10,000,000              | Very high Reynolds number    | Fully turbulent flow; large-scale aircraft                |

These ranges are approximate and may overlap depending on operating conditions and surface characteristics.

### 7.2 Practical Consequences

An airfoil optimized for a full-scale glider (*Re* ≈ 3,000,000) will typically perform very poorly on a 1-metre-chord RC model (*Re* ≈ 200,000). The Eppler and Selig SD/SA series were specifically designed for the low-*Re* range precisely because the classical NACA families do not work well there.

AeroMatch stores the minimum and maximum Reynolds number for each profile and applies a compatibility penalty when the user's operating regime falls outside this range.

---

## 8. Stall, the Boundary Layer, and Why Profile Shape Is Critical

### 8.1 The Boundary Layer

When air flows over a surface, viscosity causes the velocity to drop from the freestream value to zero at the wall. The thin layer where this transition occurs is the **boundary layer**. Its behaviour — specifically whether it remains **laminar** (smooth, layered) or transitions to **turbulent** (chaotic, energetic) — determines a significant fraction of the airfoil's drag.

- **Laminar boundary layer:** Lower skin friction, but easily separated by adverse pressure gradients. Associated with low drag in the design range.
- **Turbulent boundary layer:** Higher skin friction, but more resistant to separation (it can "climb" adverse pressure gradients that would detach a laminar layer).

### 8.2 How Stall Occurs

As angle of attack increases, the adverse pressure gradient on the upper surface strengthens. Eventually the boundary layer can no longer maintain attached flow and **separates** from the surface. The upper surface pressure suction collapses, lift drops sharply, and drag rises dramatically. This is **stall**.

Three main stall types exist:

| Stall Type           | Associated Profile Feature     |             Characteristics             |
|----------------------|--------------------------------|-----------------------------------------|
| Trailing-edge stall  | Thick airfoils (t/c > 12%)     | Gradual separation, provides warning    |
| Leading-edge stall   | Thin airfoils (t/c 6–12%)      | Sudden separation, minimal warning      |
| Thin-airfoil stall   | Very thin airfoils (t/c < 6%)  | Early separation but delayed full stall |

Thicker airfoils with larger leading-edge radii tend to exhibit trailing-edge stall, which gives the pilot warning buffet before full stall. This is why trainer aircraft use relatively thick, rounded airfoils.

### 8.3 The Laminar Separation Bubble

At low Reynolds numbers (particularly 50,000–500,000), laminar flow separates near the leading edge, forms a short recirculating bubble, and then reattaches as turbulent flow. This **laminar separation bubble** can burst catastrophically at the wrong angle of attack, causing sudden and severe stall — a major concern for model aircraft and small UAVs.

---

## 9. How AeroMatch Uses These Concepts

AeroMatch translates the aerodynamic theory above into a practical matching engine. Here is how each concept maps to the system:

| Aerodynamic Concept     |                                    AeroMatch Implementation                                              |
|-------------------------|----------------------------------------------------------------------------------------------------------|
| Thickness (t/c)         | Stored per airfoil; used as a primary geometric filter and scoring parameter                             |
| Camber                  | Stored per airfoil; used to distinguish symmetric vs. cambered profiles and influence lift behavior      |
| Application / Purpose   | Mapped to predefined categories (e.g., glider, UAV, trainer) to prioritize relevant airfoils             |
| Lift-to-Drag Ratio (L/D)| Compared against user-defined target; higher weight in scoring for efficiency-driven missions            |
| Design Lift Coefficient | Matched to user input where applicable to ensure performance near operating conditions                   |
| Reynolds Number         | Each airfoil includes a valid operating range; mismatch results in a scoring penalty                     |
| Stall Characteristics   | Inferred from thickness, camber, and airfoil family to approximate stall behavior                        |
| Laminar Flow Behavior   | Tagged airfoils receive a scoring bonus when low-drag or laminar performance is desired                  |
| Mach Number Effects     | Thin profiles preferred at higher Mach; thicker profiles penalized in transonic conditions               |
| Profile Visualization   | Airfoil geometry rendered using parametric equations (e.g., NACA 4-digit formulation)                    |

The scoring engine does not perform aerodynamic simulation — it matches against curated, pre-validated data. This is a deliberate design choice: the goal is fast, explainable shortlisting, not numerical accuracy. The user is always directed to airfoiltools.com polar data and CFD validation for final design confirmation. This approach ensures that aerodynamic theory is translated into practical, explainable recommendations rather than purely data-driven outputs.

---

## 10. References

1. **Abbott, I. H., and von Doenhoff, A. E.** *Theory of Wing Sections.* Dover Publications, New York, 1959. — The definitive reference on NACA airfoil families.

2. **Anderson, J. D.** *Introduction to Flight.* 8th ed., McGraw-Hill, 2015. — Accessible treatment of lift, drag, Reynolds number, and the boundary layer.

3. **Selig, M. S. et al.** *Summary of Low-Speed Airfoil Data, Vols. 1–4.* SoarTech Publications, 1989–1996. — The primary source for the Selig, Eppler, and Wortmann profiles in the AeroMatch database.

4. **Drela, M.** "XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils." *Low Reynolds Number Aerodynamics,* Lecture Notes in Engineering, vol. 54, Springer, 1989.

5. **Jacobs, E. N., Ward, K. E., and Pinkerton, R. M.** "The Characteristics of 78 Related Airfoil Sections from Tests in the Variable-Density Wind Tunnel." NACA Report 460, 1933.

6. **Lissaman, P. B. S.** "Low-Reynolds-Number Airfoils." *Annual Review of Fluid Mechanics,* vol. 15, 1983, pp. 223–239. — Essential reading for the low-Re regime (UAVs, RC models).

7. **Sheldahl, R. E., and Klimas, P. C.** *Aerodynamic Characteristics of Seven Symmetrical Airfoil Sections Through 180-Degree Angle of Attack for Use in Aerodynamic Analysis of Vertical Axis Wind Turbines.* Sandia National Laboratories Report SAND80-2114, 1981.

---

*This document is part of the AeroMatch project — an AI-assisted airfoil selection and matching platform.

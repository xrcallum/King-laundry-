# Laundrylegends — Immersive 3D Web Architecture Blueprint

**Prepared:** 19 September 2026 · **Owner:** Callum Page · **Venture:** Laundrylegends
**Concept:** Home-laundry landing page (`site/laundry-australia/home-laundry.html`, commit `30ea2f6`) rebuilt as a gesture-driven WebGL experience. Stack: React Three Fiber over the existing copy inventory. Brand locked: `#EE6E1F` / `#194B9E` / `#000` · Anton 400 / Yellowtail / Poppins.
**Vibe:** Kinetic laundry-fresh — playful physics (steam, suds, tumbling fabric), bold Anton type over a black hero field, orange energy accents.
**Go-live gate:** all Section-7 blockers in `LAUNDRYLEGENDS-HANDOFF.md` still apply (competitor CTAs, fake contacts, competitor pricing, client trademarks). This blueprint changes rendering, not that gate.

---

## 1. Structural Content & Semantic Wireframe Matrix

| Component/View | Responsive Layout System | DOM & Component Hierarchy | Priority (1–5) | Technical Next Step |
|---|---|---|---|---|
| `GlobalCanvas` | Fixed fullscreen: `inset-0 z-0`; DOM scroller drives scene via scroll offset; Mobile+Desktop identical canvas, DPR clamp `[1,2]` | `main > Canvas.webgl(fixed) + div#scroll-root(relative z-10)` | 5 | `<Canvas gl={{antialias:true,powerPreference:'high-performance'}} dpr={[1,2]} camera={{fov:35,position:[0,0,8]}}>` + `<ScrollControls pages={9} damping={0.18}>` |
| `Header_HUD` | Sticky top, flex row, `h-[68px]`; brand lockup left, burger right; unchanged 390px-first | `header[role=banner] > a.brand(LAUNDRY★/LEGENDS + script tag) + button.hamburger[aria-expanded]` | 5 | Port existing header verbatim into HUD layer; wire burger to `uiStore.menuOpen` → `<MenuOverlay>` (fixes handoff task "no menu markup") |
| `Hero3D` | Mobile: 1-col, type stacked over canvas hero zone; ≥640px: type scales per handoff clamp table, iron mesh right-offset `x:+1.2` | `section.hero > h1(.home+.laundry+.script-sub) + a.btn-pill-outline + [3D: IronMesh+SteamField]` | 5 | Replace inline iron SVG with `IronMesh` group at `[0.8,-0.6,0]`; keep h1 in DOM (SEO/a11y), `mix-blend-mode:normal` over black |
| `LifeShort` | Centred col, `max-w-[340px]` body; sparkle SVGs → 3D sparkle sprites parallaxed | `section > h2#life-busy-h + p.subline + p.body + SparkleSprites×2` | 3 | GSAP ScrollTrigger `SplitText` word-reveal on h2; sparkles as `<Billboard>` planes, `depthWrite:false` |
| `Cards3D` (dark + white) | 1-col stack, `gap-6`, radius 26px; cards tilt in 3D on pointer | `div.simplify + div.love` (DOM cards, CSS `transform-style:preserve-3d`) | 3 | Keep as DOM (text-heavy); add `@use-gesture` hover tilt `rotateX/Y ±6°`, `perspective:1200px` on parent |
| `ProcessRail` | Mobile: vertical card stack; Desktop: horizontal scroll-jacked rail, 4 stations pinned 100vh each | `section#process > h2 + 4×article.step-card + [3D: BasketMesh, VanMesh, WasherMesh, IronFlatMesh]` | 4 | Each step's 120px SVG → low-poly mesh; `ScrollTrigger.pin` section, camera dollies `z:8→4` per station |
| `PricingBags` | 1-col; bags illustration → interactive 3D bag lineup; price card + T&Cs stay DOM | `section#pricing > h2 + hr.rule + [3D: BagsGroup×4] + div.price-card + .ironing-block + .tc-block` | 4 | Extrude bag silhouettes (`ExtrudeGeometry`, depth 0.3); labels as `<Text>` (drei/troika) using Anton woff2 |
| `CTA_Banner` | Full-width orange card, centred; pulses on viewport entry | `div.cta-banner#pickup > h2 + a.btn-pill-outline` | 5 | CTA `href` = **Laundrylegends booking URL (Blocker #2 — do not ship competitor link)**; GSAP `scale:1→1.03` yoyo on enter |
| `ClientsCarousel` | Horizontal drag/scroll-snap, `snap-x proximity`, tiles 120×84 | `section.wash > h2 + p.lead + div.clients > 5×div.client>.placeholder` | 2 | Keep dashed placeholders (Blocker #1); add `@use-gesture` drag w/ inertia; no 3D needed |
| `Footer_Clouds` | Blue block, 1-col; scallop SVG → animated cloud shader strip | `footer[role=contentinfo] > brand + a.order-btn + 2×(h4+address) + phones + p.legal + CloudShaderStrip` | 3 | Replace static clouds SVG with 60px-tall shader plane (Table 3); DOM fallback keeps existing SVG |
| `MailPill` + `MenuOverlay` | Fixed `left-4 bottom-[18px] z-50`; overlay: fullscreen black, `z-45` | `button#mailPill + nav#site-menu[hidden]` | 2 | Wire pill to real capture form or remove (Blocker #7); overlay `clip-path:circle()` GSAP expand from burger |

Priority = build order: 5 first (canvas, header, hero, CTA), then 4 (process, pricing), then 3, then 2.

---

## 2. Advanced Typography & Disruptive Design Tokens

| System Level | Real Font Pairing | Fluid Scale / Responsive CSS | Production Tailwind Strings | Anti-Aliasing & Rendering Rule |
|---|---|---|---|---|
| H1-Display ("HOME/LAUNDRY") | **Anton 400** (brand-locked; single weight — never set 900) | HOME `clamp(3rem,17vw,6rem)`; LAUNDRY `clamp(4.375rem,22vw,9.5rem)`; `leading-[0.86] tracking-[0.005em]` uppercase | `font-anton uppercase leading-[0.86] tracking-[0.005em] text-[clamp(4.375rem,22vw,9.5rem)]` | `text-white antialiased [text-rendering:optimizeLegibility]`; over moving steam: `will-change-transform`, NO blend mode (contrast on black) |
| Hero-Sub / Script accents | **Yellowtail 400** | `clamp(2.125rem,11vw,4rem)`, `leading-none`, right-aligned | `font-yellowtail text-right leading-none text-[clamp(2.125rem,11vw,4rem)]` | `subpixel-antialiased` (script hairlines die under grayscale AA); `drop-shadow-[0_2px_12px_rgba(0,0,0,.4)]` when over particles |
| Section H2 | Anton 400 | `clamp(1.75rem,8.5vw,2.75rem)` → `3.5rem` ≥640px; `leading-[0.9]` | `font-anton uppercase text-center leading-[0.9] text-[clamp(1.75rem,8.5vw,2.75rem)] sm:text-[3.5rem]` | `text-black`; on entry-animated splits add `[backface-visibility:hidden]` to kill shimmer |
| Card H3 / Nav-Links | Anton 400 / Poppins 500 | H3 `2.125rem leading-[0.95] tracking-[0.02em]`; nav `1.125rem tracking-wide` | `font-anton uppercase text-[2.125rem] leading-[0.95] tracking-[0.02em]` · `font-poppins font-medium text-lg tracking-wide` | Menu overlay links over canvas: `backdrop-blur-sm bg-black/70` panel, never raw text over live GL |
| Body / Mono-Telemetry | **Poppins 300–700** / (telemetry: Poppins 400 `tabular-nums`) | Body `1.03125rem/1.5`; prices `font-medium whitespace-nowrap`; loader % `text-sm tabular-nums` | `font-poppins text-[16.5px] leading-normal` · `tabular-nums text-sm text-white/70` | HUD text over GL: parent `pointer-events-none`, text nodes `pointer-events-auto`; `-webkit-font-smoothing:antialiased` |
| WebGL-3D-Text (bag labels, floating "FRESH") | Anton woff2 via troika `<Text>` | worldSize 0.4–0.9; `letterSpacing:0.02`; `anchorX:'center'` | n/a (GL) — `<Text font="/fonts/anton.woff2" fontSize={0.6} color="#111">` | troika SDF = resolution-independent; set `material.toneMapped=false` so `#EE6E1F` stays brand-exact |

Google Fonts URL unchanged from handoff §3. Self-host Anton woff2 additionally for troika (GL can't consume the CSS API).

---

## 3. 3D Scene Architecture & WebGL Performance Matrix

| 3D Element/Mesh | Geometry & Material Spec | Camera & Lighting Vectors | Physics / Math Loop | GPU Optimisation Engine |
|---|---|---|---|---|
| `IronMesh` (hero) | Lathe+extrude combo ≤6k tris; `MeshPhysicalMaterial{color:#f5f5f5,metalness:0.85,roughness:0.25,clearcoat:0.6}`; soleplate emissive `#EE6E1F ×0.3` | Cam `[0,0,8]→lookAt[0,0,0]` fov35; key `DirectionalLight [4,6,5] i=2.2 shadow.mapSize=1024`; rim `PointLight [-3,2,-2] #EE6E1F i=1.4`; amb 0.35 | Idle float: `pos.y = -0.6 + sin(t*0.8)*0.06`; `rot.z = sin(t*0.5)*0.03`; pointer parallax `rot.y += (mouseX*0.25 - rot.y)*0.08` | Single merged geometry = 1 draw call; `castShadow` only on iron; shadows off <768px |
| `SteamField` | `InstancedMesh` plane ×400, 8×8 alpha-atlas smoke texture; `AdditiveBlending, depthWrite:false, opacity:0.35` | Unlit (basic material) | Per frame: `y += v*dt; scale += 0.15*dt; opacity = 0.35*(1-y/3)`; respawn at soleplate when `y>3`; curl offset `x += sin(y*2+seed)*0.002` | 1 draw call via instancing; texture atlas kills per-particle binds; `frustumCulled:false` (always hero-visible) |
| `SudsParticles` (ambient bg) | `Points` ×1500, `PointsMaterial{size:0.04,color:#fff,transparent,opacity:0.5}` sphere-sprite tex | Unlit | `pos.y += 0.05*dt; pos.x += sin(t+phase)*0.001`; wrap at bounds ±6; scroll-velocity coupling: `vy += scrollVel*0.002` | GPU points = 1 draw call; positions in `BufferAttribute`, updated via shader `uTime` uniform not CPU loop |
| `VanMesh` / `BasketMesh` / `WasherMesh` / `IronFlatMesh` (process stations) | Each ≤3k tris, flat-shaded `MeshToonMaterial` 3-step gradientMap; palette `#111/#fff/#EE6E1F` matching line-art SVGs | Per-station cam keyframes: st1 `[0,0,6]`, st2 `[2,0.5,5]`, st3 `[-1.5,0,4.5]`, st4 `[0,-0.5,5]`; all `lookAt[0,0,0]`; one shared DirLight | Washer drum: `drum.rot.z += dt*4.2` (station-3 active only); van wheels `rot.z -= dt*6` + body `y = sin(t*9)*0.01` jitter | All 4 in one `<group>`, non-active stations `visible=false` (skips render entirely); shared materials → 4 programs total |
| `BagsGroup` (pricing) | 4× `ExtrudeGeometry` from bag path, depth 0.3, ≤800 tris each; `MeshStandardMaterial{color:#fff,roughness:0.9}` + troika labels | Cam pull-back to `[0,0.4,7]`; soft `RectAreaLight [0,4,3] 6×3 i=3` | Stagger settle on enter: `y: 2→0` spring per bag, delay `i*0.12`; hover: `rot.y → ±0.15` lerp 0.1 | Labels: troika SDF (no canvas textures); bags share 1 material instance; `matrixAutoUpdate=false` after settle |
| `CloudShaderStrip` (footer) | 1 plane 2×0.6 @ footer top edge; custom frag: fbm noise `smoothstep(0.45,0.55,fbm(uv*3+uTime*0.02))`, white on `#194B9E` | Unlit fullbright | `uTime += dt`; drift only — no vertex work | 1 quad, 1 program; `precision mediump`; fallback = existing static clouds SVG when `!WebGL2` |
| `SparkleSprites` | `InstancedMesh` ×12 star-plane, basic mat `#EE6E1F`, `depthTest:false` | Unlit | Twinkle: `scale = base*(0.8+0.2*sin(t*3+seed))`; scroll parallax `y = anchorY + scroll*0.3*depthFactor` | Instanced; `renderOrder=1` over scene, avoids sorting cost |

Global: `renderer.outputColorSpace=SRGBColorSpace`; `ACESFilmicToneMapping` OFF for brand-colour fidelity (`NoToneMapping`); target ≤25 draw calls, ≤60k tris total scene; `useFrame` priority ordering: input(−1) → physics(0) → camera(1).

---

## 4. Gesture Mechanics & Kinetic Interaction Matrix

| Interaction Node | Gesture Trigger | Animation Framework Logic | Kinetic Inertia/Feedback | Library Dependency |
|---|---|---|---|---|
| Page scroll ↔ scene timeline | `wheel/deltaY` + `touchmove` via ScrollControls virtual scroll | drei `<ScrollControls damping={0.18}>`; camera + section states read `scroll.offset` in `useFrame` | Built-in damped lerp: `current += (target-current)*(1-exp(-damping*60*dt))`; `scrollVel = offset-prevOffset` feeds SudsParticles | `@react-three/drei` (ScrollControls/useScroll) |
| `IronMesh` pointer parallax | `pointermove` on window (throttled to rAF, NOT per-event raycast) | Lerp: `rot.y→mouseNDC.x*0.25, rot.x→-mouseNDC.y*0.12`, factor 0.08 | Exponential smoothing gives natural trailing decay; zero on `pointerleave` over 600ms | native + `useFrame` |
| Hero CTA `btn-pill-outline` | `onPointerEnter/Leave`, `onPointerDown` | Framer Motion `whileHover={{scale:1.05}} whileTap={{scale:0.96}} transition={{type:'spring',stiffness:300,damping:20}}` | Spring overshoot = tactile feedback; steam burst event: `steamField.emit(30)` on hover | `framer-motion` |
| `Cards3D` tilt | `onMove` (pointer) mapped to card-local NDC | `useSpring`: `rotateX: py*-6°, rotateY: px*6°`, `{stiffness:150,damping:18}`; reset on leave | Spring return-to-rest; shadow deepens with tilt: `shadow-y = 22+|rot|*4px` | `@use-gesture/react` + `@react-spring/web` |
| `ProcessRail` scroll-jack | ScrollTrigger `pin:true, scrub:0.6, snap:1/3` across 4 stations | GSAP timeline: per station — cam pos tween `power2.inOut` + station mesh `visible` swap + card text `y:24→0 opacity:0→1 stagger:0.08` | `scrub:0.6` = 600ms catch-up inertia; `snap:{snapTo:1/3,duration:{min:0.2,max:0.6},ease:'power1.inOut'}` | `gsap/ScrollTrigger` |
| `ClientsCarousel` drag | `drag` gesture w/ `axis:'x'`, `filterTaps:true`, touch + mouse | `useGesture({onDrag:({offset:[x]})=>api.start({x})})` on track; snap to tile centres on release | Momentum: `v_release*0.95^frame` decay projected to nearest snap point: `target = round((x+v*τ)/w)*w`, τ=325ms iOS-style | `@use-gesture/react` |
| `BagsGroup` hover | `onPointerOver/Out` per bag (raycast throttled: `raycaster.far=12`, layer-masked to bags) | R3F event → spring `rot.y:±0.15, y:+0.08`, `{stiffness:120,damping:14}`; troika label `fillOpacity` 0.85→1 | Spring settle; cursor `pointer` via `useCursor(hovered)` | `@react-three/fiber` events + `@react-spring/three`, drei `useCursor` |
| Burger → `MenuOverlay` | `click`, `aria-expanded` sync (keeps existing a11y contract) | GSAP `clip-path: circle(0% at top-right) → circle(150%)`, 0.5s `expo.out`; links stagger `x:-16 opacity:0`, 0.05s | None (discrete); `Escape` + outside-tap close, focus-trap while open | `gsap` + native |
| `MailPill` | `click` (X zone ≤44px from left edge = dismiss, else open form — preserves existing IIFE contract) | Framer `AnimatePresence` exit `{scale:0.8,opacity:0,y:8}` 0.2s | n/a; dismissal persisted `localStorage['ll-pill']='1'` (try/catch wrapped) | `framer-motion` |
| Reduced motion (all nodes) | `matchMedia('(prefers-reduced-motion:reduce)')` | Kill ScrollTrigger scrub→instant, springs→`immediate:true`, steam rate ×0.3 | Damping bypassed globally via `motionOK` flag in store | native |

---

## 5. State Handling & Client-Side Rendering Matrix

| Section View | Layout Strategy | Global/Local State Architecture | Hydration & Loading UX | Generation Credit-Saving Tip |
|---|---|---|---|---|
| App shell / `GlobalCanvas` | z-schema: canvas `z-0` · scroll content `z-10` · header `z-40` · menu `z-45` · pill `z-50`; content sections `pointer-events-none`, interactive children `-auto` | Zustand `useUIStore{menuOpen,pillDismissed,motionOK,activeSection}` + `useSceneStore{scrollOffset,scrollVel,quality:'hi'|'lo'}`; mouse NDC in `useRef` (never state — no re-renders at 60fps) | Root `<Suspense fallback={<Loader/>}>`; drei `useProgress` → % into branded loader (black bg, Anton "LAUNDRY LEGENDS", orange bar `scaleX:progress`) | One canonical `tokens.ts` (colours/type/radii from handoff §3) imported everywhere — generate once, reference by name in every later prompt |
| Hero | Hero copy = server-rendered DOM (SEO keeps H1); canvas hero zone = first 1.2 scroll pages | Local: steam emit queue `useRef([])`; hover state local `useState` on CTA only | `IronMesh` inline geometry (no GLTF fetch) → paints with first GL frame; steam texture 32KB preloaded via `useTexture.preload` | Build `IronMesh` as parametric code, not a .glb — no asset pipeline, no binary in repo, regen-able from ~40 lines |
| Process rail | Pinned 400vh wrapper; inner `sticky top-0 h-screen`; cards absolute, `gap` n/a (staged) | `activeStation` derived: `Math.floor(offset*sections)` — computed in `useFrame`, written to store only on change (transient update `store.setState`) | Station meshes are code-built toon prims; all mount upfront (≤12k tris), zero streaming needed | 4 station meshes share one `<StationMesh kind=…>` component + data array — 1 component to generate, not 4 |
| Pricing | DOM card grid over canvas window (`div` with `h-[420px]` GL viewport via drei `<View>`); T&Cs plain flow | Bag hover index in local `useState`; price data from `pricing.ts` const (**values = Blocker #5, Max Jones to supply — ship behind `PRICING_CONFIRMED` flag**) | `<View>` shares the one canvas (no 2nd context); Anton woff2 for troika preloaded in `<Loader>` phase | Keep all copy in `content.ts` mirroring handoff §5 inventory — diffable against handoff, and prompts can say "use content.ts" instead of re-pasting strings |
| Clients / Footer | Carousel `overflow-x:hidden` + transform track (gesture-driven, not native scroll); footer standard flow, cloud strip `<View>` 60px | Carousel spring `x` in react-spring ref; no global state | Placeholders = zero assets until Blocker #1 clears; cloud shader lazy: `const Clouds = lazy(()=>import('./Clouds'))` below-fold | Shader as template-literal GLSL in one file; fallback SVG already exists in repo — reference `home-laundry.html:818-832`, don't regenerate |
| Cross-cutting | Single scroll owner (ScrollControls) — no nested scroll containers except carousel track | Quality autoscaler: `useDetectGPU()` tier<2 → `quality:'lo'` (steam×150, no shadows, DPR 1) | `<PerformanceMonitor onDecline={()=>setQuality('lo')}>` runtime downgrade; below-fold sections `content-visibility:auto` in DOM | Generate in this order: tokens→content→shell→hero→sections; each phase compiles standalone, so each LLM pass needs only `tokens.ts`+`content.ts` in context, never the whole app |

---

*All colour, type and copy values trace to `LAUNDRYLEGENDS-HANDOFF.md` (§3, §5) at commit `30ea2f6`. Pricing figures, contact details and client names remain blocked per §7 — this blueprint does not clear them.*
